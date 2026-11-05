from types import SimpleNamespace

import support_toolkit as toolkit
from support_toolkit import dns_test, recommendations, top_processes


def sample_report():
    return {
        "cpu": {"percent": 25},
        "memory": {"percent": 40},
        "disks": [{"mount": "C:\\", "used_percent": 50}],
        "connectivity": {
            "internet_ip_test": True,
            "dns": {"ok": True},
        },
    }


def test_dns_shape():
    result = dns_test("localhost")
    assert result["host"] == "localhost"
    assert "ok" in result


def test_recommendations_do_not_flag_normal_values():
    result = recommendations(sample_report())
    assert result == ["Nenhum dos limiares básicos foi ultrapassado nesta coleta."]


def test_recommendations_flag_resource_and_network_conditions():
    report = sample_report()
    report["cpu"]["percent"] = 95
    report["memory"]["percent"] = 96
    report["disks"][0]["used_percent"] = 94
    report["connectivity"]["internet_ip_test"] = False
    report["connectivity"]["dns"]["ok"] = False
    result = recommendations(report)
    assert len(result) == 5
    assert any("CPU" in item for item in result)
    assert any("Memória" in item for item in result)
    assert any("Armazenamento" in item for item in result)
    assert any("ICMP" in item for item in result)
    assert any("DNS" in item for item in result)


def test_top_processes_limit_is_validated():
    try:
        top_processes(0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected invalid process limit to fail")


def test_collect_has_required_sections():
    from support_toolkit import collect
    report = collect()
    assert {
        "generated_at", "hostname", "os", "boot_time", "uptime_seconds",
        "cpu", "memory", "disks", "network_interfaces", "connectivity",
        "top_processes",
    } <= report.keys()
    assert report["uptime_seconds"] >= 0


def test_collect_applies_process_limit_once(monkeypatch):
    calls = []

    monkeypatch.setattr(toolkit.psutil, "disk_partitions", lambda all=False: [])
    monkeypatch.setattr(toolkit.psutil, "net_if_addrs", lambda: {})
    monkeypatch.setattr(
        toolkit.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(total=8 * 2**30, available=4 * 2**30, percent=50),
    )
    monkeypatch.setattr(toolkit.psutil, "boot_time", lambda: 1_700_000_000)
    monkeypatch.setattr(
        toolkit.psutil,
        "cpu_count",
        lambda logical=True: 8 if logical else 4,
    )
    monkeypatch.setattr(toolkit.psutil, "cpu_percent", lambda interval=None: 12.5)
    monkeypatch.setattr(toolkit, "ping", lambda host: True)
    monkeypatch.setattr(
        toolkit,
        "dns_test",
        lambda: {"host": "example.com", "resolved_ip": "192.0.2.1", "ok": True},
    )

    def fake_top_processes(limit=8):
        calls.append(limit)
        return []

    monkeypatch.setattr(toolkit, "top_processes", fake_top_processes)

    report = toolkit.collect(process_limit=3)

    assert report["top_processes"] == []
    assert calls == [3]
