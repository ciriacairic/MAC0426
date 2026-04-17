#!/usr/bin/env python3
"""
Runner de benchmark para PostgreSQL vs MySQL (dataset StackOverflow 2010).

Exemplos de uso:
  # Rodar tudo (todos os cenários, todas as queries, ambos os SGBDs)
  python run_experiments.py

  # Rodar apenas o cenário btree no PostgreSQL
  python run_experiments.py --scenario btree --sgbd postgresql

  # Rodar uma única query em todos os cenários
  python run_experiments.py --query pk_single

  # 30 execuções, sem warmup
  python run_experiments.py --runs 30 --warmup 0
"""

import argparse
import csv
import os
import sys
from datetime import datetime

from runner.connections import CONNECTORS
from runner.executor    import resolve_sql, run_query_batch
from runner.metrics     import ContainerMetrics
from queries            import ALL_QUERIES, QUERY_MAP
from scenarios          import SCENARIOS, apply_scenario

# Mapeia nome do SGBD → nome do serviço no Docker Compose (usado para métricas do container)
_SGBD_SERVICE = {
    "postgresql": "postgres",
    "mysql":      "mysql",
}

CSV_FIELDS = ["sgbd", "scenario", "query", "run", "time_s", "cpu_percent", "mem_mb"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa experimentos de benchmark (PostgreSQL vs MySQL)"
    )
    parser.add_argument(
        "--scenario", default="all",
        choices=["all"] + list(SCENARIOS.keys()),
        help="Cenário a executar (padrão: all)",
    )
    parser.add_argument(
        "--query", default="all",
        help="Nome da query a executar, ou 'all' (padrão: all)",
    )
    parser.add_argument(
        "--runs", type=int, default=20,
        help="Número de execuções medidas por query (padrão: 20)",
    )
    parser.add_argument(
        "--warmup", type=int, default=1,
        help="Execuções de warmup (não gravadas) (padrão: 1)",
    )
    parser.add_argument(
        "--sgbd", default="all",
        choices=["all", "postgresql", "mysql"],
        help="Qual SGBD executar (padrão: all)",
    )
    parser.add_argument(
        "--output", default="results",
        help="Diretório de saída para os CSVs (padrão: results/)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    scenarios = list(SCENARIOS.keys()) if args.scenario == "all" else [args.scenario]
    sgbds     = ["postgresql", "mysql"] if args.sgbd == "all"     else [args.sgbd]

    if args.query == "all":
        queries = ALL_QUERIES
    elif args.query in QUERY_MAP:
        queries = [QUERY_MAP[args.query]]
    else:
        print(f"Unknown query '{args.query}'. Available: {', '.join(QUERY_MAP)}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)
    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(args.output, f"results_{timestamp}.csv")

    print("=" * 60)
    print(f"Output file : {output_file}")
    print(f"SGBDs       : {sgbds}")
    print(f"Scenarios   : {scenarios}")
    print(f"Queries     : {len(queries)}")
    print(f"Runs        : {args.runs}  (+{args.warmup} warmup)")
    print("=" * 60)

    with open(output_file, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()

        for sgbd in sgbds:
            print(f"\n{'─' * 60}")
            print(f"  SGBD: {sgbd.upper()}")
            print(f"{'─' * 60}")

            conn    = CONNECTORS[sgbd]()
            metrics = ContainerMetrics(_SGBD_SERVICE[sgbd])

            if metrics.container is None:
                print(f"  [INFO] Socket Docker indisponível — cpu_percent/mem_mb serão null")

            for scenario in scenarios:
                print(f"\n  [scenario] {scenario}")
                apply_scenario(conn, scenario, sgbd)

                for query_def in queries:
                    sql = resolve_sql(query_def, sgbd, scenario)
                    if sql is None:
                        continue

                    print(f"    {query_def['name']: <35}", end="", flush=True)
                    try:
                        results = run_query_batch(
                            conn, query_def, sgbd, scenario,
                            runs=args.runs, warmup=args.warmup,
                            metrics=metrics,
                        )
                    except Exception as exc:
                        print(f"ERROR: {exc}")
                        continue

                    writer.writerows(results)
                    csv_file.flush()

                    if results:
                        times = [r["time_s"] for r in results]
                        avg   = sum(times) / len(times)
                        std   = (sum((t - avg) ** 2 for t in times) / len(times)) ** 0.5
                        print(f"avg={avg:.4f}s  std={std:.4f}s")
                    else:
                        print("skipped")

            conn.close()

    print(f"\n{'=' * 60}")
    print(f"Done. Results saved to {output_file}")


if __name__ == "__main__":
    main()
