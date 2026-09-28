from support_toolkit import dns_test, collect
def test_dns_shape():
    assert "ok" in dns_test("localhost")
def test_collect_shape():
    data=collect()
    assert {"hostname","os","cpu_percent","memory_percent","disks","connectivity"} <= data.keys()
