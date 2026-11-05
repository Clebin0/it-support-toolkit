from __future__ import annotations

import argparse
import json
import platform
import socket
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psutil


def ping(host: str, timeout: int = 4) -> bool:
    """Run one ICMP probe without invoking a shell."""
    flag = "-n" if platform.system() == "Windows" else "-c"
    wait_flag = "-w" if platform.system() == "Windows" else "-W"
    wait_value = str(timeout * 1000 if platform.system() == "Windows" else timeout)
    try:
        result = subprocess.run(
            ["ping", flag, "1", wait_flag, wait_value, host],
            capture_output=True,
            timeout=timeout + 1,
            check=False,
        )
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def dns_test(host: str = "example.com") -> dict[str, Any]:
    try:
        return {"host": host, "resolved_ip": socket.gethostbyname(host), "ok": True}
    except (socket.gaierror, OSError) as exc:
        return {"host": host, "ok": False, "error": type(exc).__name__}


def top_processes(limit: int = 8) -> list[dict[str, Any]]:
    if not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50")

    rows: list[dict[str, Any]] = []
    # Prime CPU counters before sampling so values are comparable.
    processes = list(psutil.process_iter(["pid", "name", "memory_percent"]))
    for process in processes:
        try:
            process.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(0.15)
    for process in processes:
        try:
            info = process.as_dict(attrs=["pid", "name", "memory_percent"])
            cpu = process.cpu_percent(interval=None)
            rows.append(
                {
                    "pid": info["pid"],
                    "name": info["name"] or "unknown",
                    "cpu_percent": round(cpu, 1),
                    "memory_percent": round(info["memory_percent"] or 0, 2),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return sorted(
        rows,
        key=lambda row: (row["cpu_percent"], row["memory_percent"]),
        reverse=True,
    )[:limit]


def collect(process_limit: int = 8) -> dict[str, Any]:
    disks = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append(
                {
                    "device": part.device,
                    "mount": part.mountpoint,
                    "filesystem": part.fstype,
                    "total_gb": round(usage.total / 2**30, 1),
                    "free_gb": round(usage.free / 2**30, 1),
                    "used_percent": usage.percent,
                }
            )
        except (OSError, PermissionError):
            continue

    interfaces = {}
    for name, addresses in psutil.net_if_addrs().items():
        interfaces[name] = [
            {"address": address.address, "family": str(address.family)}
            for address in addresses
        ]

    memory = psutil.virtual_memory()
    boot_time = psutil.boot_time()
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "os": platform.platform(),
        "boot_time": datetime.fromtimestamp(boot_time, timezone.utc).isoformat(),
        "uptime_seconds": max(0, int(time.time() - boot_time)),
        "cpu": {
            "logical": psutil.cpu_count(),
            "physical": psutil.cpu_count(logical=False),
            "percent": psutil.cpu_percent(interval=0.4),
        },
        "memory": {
            "total_gb": round(memory.total / 2**30, 1),
            "available_gb": round(memory.available / 2**30, 1),
            "percent": memory.percent,
        },
        "disks": disks,
        "network_interfaces": interfaces,
        "connectivity": {
            "internet_ip_test": ping("1.1.1.1"),
            "dns": dns_test(),
        },
        "top_processes": top_processes(process_limit),
    }


def recommendations(data: dict[str, Any]) -> list[str]:
    tips = []
    if data["cpu"]["percent"] >= 90:
        tips.append("CPU acima de 90% no instante da coleta.")
    if data["memory"]["percent"] >= 90:
        tips.append("Memória acima de 90% do total.")
    for disk in data["disks"]:
        if disk["used_percent"] >= 90:
            tips.append(
                f"Armazenamento em {disk['mount']} acima de 90% de utilização."
            )
    if not data["connectivity"]["internet_ip_test"]:
        tips.append("O teste ICMP para 1.1.1.1 não recebeu resposta.")
    if not data["connectivity"]["dns"]["ok"]:
        tips.append("A resolução DNS do nome de teste falhou.")
    if not tips:
        tips.append("Nenhum dos limiares básicos foi ultrapassado nesta coleta.")
    return tips


def build_report(process_limit: int = 8) -> dict[str, Any]:
    report = collect(process_limit)
    report["recommendations"] = recommendations(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Coleta somente leitura para diagnóstico de suporte e infraestrutura."
    )
    parser.add_argument("--report", default="", help="Caminho para salvar o JSON.")
    parser.add_argument(
        "--compact", action="store_true", help="Imprime JSON sem indentação."
    )
    parser.add_argument(
        "--top-processes",
        type=int,
        default=8,
        choices=range(1, 51),
        metavar="1-50",
        help="Quantidade de processos exibidos (padrão: 8).",
    )
    args = parser.parse_args()

    report = build_report(args.top_processes)
    output = json.dumps(
        report,
        indent=None if args.compact else 2,
        ensure_ascii=False,
    )
    print(output)

    if args.report:
        destination = Path(args.report)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(output + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
