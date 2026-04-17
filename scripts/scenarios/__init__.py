from . import no_index, btree, fulltext_idx

SCENARIOS: dict = {
    "no_index": no_index,
    "btree":    btree,
    "fulltext": fulltext_idx,
}


def apply_scenario(conn, scenario_name: str, sgbd: str) -> None:
    """
    Coloca o banco em estado limpo para o cenário dado:
      1. Remove todos os índices gerenciados (ignora erros para índices inexistentes).
      2. Cria os índices definidos pelo cenário.
    """
    cursor = conn.cursor()
    try:
        # -- Teardown: remove todos os índices gerenciados de todos os cenários --
        for module in SCENARIOS.values():
            for sql in module.TEARDOWN.get(sgbd, []):
                try:
                    cursor.execute(sql)
                except Exception:
                    pass  # índice provavelmente ainda não existe

        # -- Setup: cria os índices do cenário atual --
        for sql in SCENARIOS[scenario_name].SETUP.get(sgbd, []):
            try:
                cursor.execute(sql)
            except Exception as exc:
                print(f"  [AVISO] falha ao criar índice ({sgbd}/{scenario_name}): {exc}")
    finally:
        cursor.close()

    print(f"  [setup] {sgbd}: scenario '{scenario_name}' ready")
