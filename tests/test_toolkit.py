from support_toolkit import collect,dns_test,recommendations

def test_dns_shape():
    assert "ok" in dns_test("localhost")

def test_collect_shape():
    data=collect()
    assert {"hostname","os","cpu","memory","disks","connectivity","top_processes"} <= data.keys()

def test_recommendations_returns_list():
    assert isinstance(recommendations(collect()),list)
