from support_toolkit import collect, dns_test
def test_dns_shape(): assert "ok" in dns_test("localhost")
def test_collect_shape():
    data=collect()
    assert {"hostname","os","cpu_percent","memory_percent","disks","connectivity"} <= data.keys()
