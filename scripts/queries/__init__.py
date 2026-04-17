from .pk_lookup import QUERIES as _PK

ALL_QUERIES: list[dict] = _PK

QUERY_MAP: dict[str, dict] = {q["name"]: q for q in ALL_QUERIES}
