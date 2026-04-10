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

> **Ainda não implementado.**

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
  queries/      # scripts por categoria de operação (não implementado)
  results/      # CSVs com tempos de execução (não implementado)
  plots/        # gráficos gerados (não implementado)
docker-compose.yml
.env
```
