from typing import Optional

try:
    import docker as docker_sdk
    _docker_available = True
except ImportError:
    _docker_available = False


class ContainerMetrics:
    """Coleta stats de CPU e RAM de um container Docker pelo nome do serviço no Compose."""

    def __init__(self, service_name: str):
        self.container = None
        if not _docker_available:
            return
        try:
            client = docker_sdk.from_env()
            containers = client.containers.list(
                filters={"label": f"com.docker.compose.service={service_name}"}
            )
            if containers:
                self.container = containers[0]
        except Exception:
            pass

    def snapshot(self) -> Optional[dict]:
        """Tira um snapshot pontual das stats. Retorna None se indisponível."""
        if not self.container:
            return None
        try:
            s = self.container.stats(stream=False)
            return {
                "cpu_total":  s["cpu_stats"]["cpu_usage"]["total_usage"],
                "cpu_system": s["cpu_stats"].get("system_cpu_usage", 0),
                "mem_bytes":  s["memory_stats"].get("usage", 0),
            }
        except Exception:
            return None

    @staticmethod
    def delta(before: Optional[dict], after: Optional[dict]) -> dict:
        """Calcula CPU % e memória (MB) a partir de dois snapshots."""
        if not before or not after:
            return {"cpu_percent": None, "mem_mb": None}

        cpu_delta    = after["cpu_total"]  - before["cpu_total"]
        system_delta = after["cpu_system"] - before["cpu_system"]
        cpu_pct = round((cpu_delta / system_delta) * 100, 4) if system_delta > 0 else 0.0
        mem_mb  = round(after["mem_bytes"] / (1024 * 1024), 2)

        return {"cpu_percent": cpu_pct, "mem_mb": mem_mb}
