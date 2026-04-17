import time
from typing import Optional

from .metrics import ContainerMetrics

_DML_KEYWORDS = {"INSERT", "UPDATE", "DELETE"}


def _is_dml(sql: str) -> bool:
    return sql.strip().split()[0].upper() in _DML_KEYWORDS


def resolve_sql(query_def: dict, sgbd: str, scenario: str) -> Optional[str]:
    """
    Retorna o SQL para um dado sgbd + cenário.

    query_def["sql"][sgbd] pode ser:
      - uma string simples  → usada para todos os cenários
      - um dict             → chaves são nomes de cenário ou "default"
    Retorna None se o sgbd não está coberto pelo cenário atual.
    """
    sql = query_def["sql"].get(sgbd)
    if sql is None:
        return None
    if isinstance(sql, dict):
        return sql.get(scenario) or sql.get("default")
    return sql


def run_query_batch(
    conn,
    query_def: dict,
    sgbd: str,
    scenario: str,
    runs: int,
    warmup: int,
    metrics: ContainerMetrics,
) -> list[dict]:
    """
    Executa uma query (runs + warmup) vezes e retorna uma lista de dicts com resultados.
    As execuções de warmup rodam mas não são gravadas.
    DML é envolvido em transação com rollback para não alterar o estado do banco.
    """
    sql = resolve_sql(query_def, sgbd, scenario)
    if sql is None:
        return []

    is_dml = _is_dml(sql)
    results = []

    for i in range(1, warmup + runs + 1):
        cursor = conn.cursor()
        try:
            if is_dml:
                if sgbd == "postgresql":
                    cursor.execute("BEGIN")
                else:
                    conn.start_transaction()

            snap_before = metrics.snapshot()
            start       = time.perf_counter()
            cursor.execute(sql)
            elapsed     = time.perf_counter() - start
            snap_after  = metrics.snapshot()

            if is_dml:
                conn.rollback()
        except Exception:
            try:
                conn.rollback()
            except Exception:
                pass
            raise
        finally:
            cursor.close()

        if i > warmup:
            m = ContainerMetrics.delta(snap_before, snap_after)
            results.append({
                "sgbd":        sgbd,
                "scenario":    scenario,
                "query":       query_def["name"],
                "run":         i - warmup,
                "time_s":      round(elapsed, 6),
                "cpu_percent": m["cpu_percent"],
                "mem_mb":      m["mem_mb"],
            })

    return results
