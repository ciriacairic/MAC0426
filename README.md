# MAC0426 / MAC5760 — Avaliação de Desempenho de SGBDs

Estudo comparativo de desempenho entre PostgreSQL e MySQL usando o banco de dados do StackOverflow (2010).

## Pré-requisitos

- Docker
- Docker Compose

## Configuração inicial

Os scripts SQL não estão no repositório por conta do tamanho (~1.25 GB cada). Baixe, descompacte e coloque nas pastas abaixo:

| Arquivo | Destino |
|---|---|
| `postgresql_script_criacao_bd.sql` | `db/postgres/` |
| `mysql_script_criacao_bd.sql` | `db/mysql/` |

```bash
unzip postgresql_script_criacao_bd.zip -d db/postgres/
unzip mysql_script_criacao_bd.zip -d db/mysql/
```

## Executando o ambiente

```bash
# Sobe PostgreSQL e MySQL (inicializa o BD na primeira vez — pode demorar vários minutos)
docker compose up --build

# Verificar se os bancos estão prontos
docker compose ps
```

## Executando os experimentos

```bash
# Rodar todos os experimentos (todos os cenários, todas as queries, ambos os SGBDs)
docker compose run --rm runner python run_experiments.py

# Rodar apenas um cenário
docker compose run --rm runner python run_experiments.py --scenario btree

# Rodar apenas um SGBD
docker compose run --rm runner python run_experiments.py --sgbd postgresql

# Rodar uma query específica
docker compose run --rm runner python run_experiments.py --query test_select

# Alterar número de execuções e warmup
docker compose run --rm runner python run_experiments.py --runs 30 --warmup 2
```

Os resultados são salvos em `scripts/results/` como CSVs com timestamp no nome.

### Cenários disponíveis

| Cenário | Descrição |
|---|---|
| `no_index` | Nenhum índice além das PKs |
| `btree` | Índices B-tree em atributos não-chave selecionados |
| `hash` | Índices hash (apenas PostgreSQL; MySQL roda equivalente ao `no_index`) |
| `fulltext` | Índices full-text em `Posts.Body` e `Users.AboutMe` |

### Colunas do CSV de saída

| Coluna | Descrição |
|---|---|
| `sgbd` | `postgresql` ou `mysql` |
| `scenario` | Cenário de índice utilizado |
| `query` | Nome da query executada |
| `run` | Número da execução (começa em 1) |
| `time_s` | Tempo de execução em segundos |
| `cpu_percent` | Uso de CPU do container durante a execução (null se Docker indisponível) |
| `mem_mb` | Uso de memória do container em MB (null se Docker indisponível) |

## Estrutura do projeto

```
db/
  postgres/
    init/       # shell wrapper de carga (versionado)
    postgresql_script_criacao_bd.sql  # não versionado, adicionar manualmente
  mysql/
    init/       # shell wrapper de carga (versionado)
    mysql_script_criacao_bd.sql       # não versionado, adicionar manualmente
scripts/
  Dockerfile
  requirements.txt
  run_experiments.py      # orquestra todos os experimentos
  runner/
    config.py             # leitura de variáveis de ambiente
    connections.py        # conexões com PostgreSQL e MySQL
    executor.py           # execução e medição de queries
    metrics.py            # coleta de CPU e RAM via Docker SDK
  queries/
    pk_lookup.py          # queries de busca por chave primária
  scenarios/
    no_index.py           # sem índices extras
    btree.py              # índices B-tree
    hash.py               # índices hash
    fulltext_idx.py       # índices full-text
  results/                # CSVs com tempos de execução (gerado em runtime)
  plots/                  # gráficos gerados (a implementar)
docker-compose.yml
.env                      # credenciais e portas
```
