from __future__ import annotations
import argparse, json, platform, shutil, socket, subprocess
from datetime import datetime, timezone
from pathlib import Path
import psutil

def ping(host: str) -> bool:
    flag = "-n" if platform.system() == "Windows" else "-c"
    try:
        return subprocess.run(["ping", flag, "1", host], capture_output=True, timeout=4).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False

def dns_test(host: str = "example.com") -> dict:
    try:
        return {"host": host, "resolved_ip": socket.gethostbyname(host), "ok": True}
    except socket.gaierror as exc:
        return {"host": host, "ok": False, "error": str(exc)}

def collect() -> dict:
    disks=[]
    for p in psutil.disk_partitions(all=False):
        try:
            u=psutil.disk_usage(p.mountpoint)
            disks.append({"device":p.device,"mount":p.mountpoint,"total_gb":round(u.total/2**30,1),"used_percent":u.percent})
        except OSError: pass
    nets={name:[{"address":a.address,"family":str(a.family)} for a in addrs] for name,addrs in psutil.net_if_addrs().items()}
    return {
      "generated_at":datetime.now(timezone.utc).isoformat(),
      "hostname":socket.gethostname(),"os":platform.platform(),
      "cpu_percent":psutil.cpu_percent(interval=.4),
      "memory_percent":psutil.virtual_memory().percent,
      "disks":disks,"network_interfaces":nets,
      "connectivity":{"gateway_test":ping("1.1.1.1"),"dns":dns_test()}
    }

def main():
    ap=argparse.ArgumentParser(description="IT Support diagnostic toolkit")
    ap.add_argument("--report", default="")
    args=ap.parse_args()
    data=collect()
    print(json.dumps(data,indent=2,ensure_ascii=False))
    if args.report:
        p=Path(args.report); p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")

if __name__=="__main__": main()
