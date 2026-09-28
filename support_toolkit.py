from __future__ import annotations
import argparse, json, platform, socket, subprocess
from datetime import datetime, timezone
from pathlib import Path
import psutil

def ping(host:str)->bool:
    flag="-n" if platform.system()=="Windows" else "-c"
    try:
        return subprocess.run(["ping",flag,"1",host],capture_output=True,timeout=4).returncode==0
    except (OSError,subprocess.TimeoutExpired):
        return False

def dns_test(host:str="example.com")->dict:
    try:
        return {"host":host,"resolved_ip":socket.gethostbyname(host),"ok":True}
    except socket.gaierror as exc:
        return {"host":host,"ok":False,"error":str(exc)}

def top_processes(limit:int=8)->list[dict]:
    rows=[]
    for p in psutil.process_iter(["pid","name","cpu_percent","memory_percent"]):
        try:
            i=p.info
            rows.append({"pid":i["pid"],"name":i["name"] or "unknown","cpu_percent":round(i["cpu_percent"] or 0,1),"memory_percent":round(i["memory_percent"] or 0,2)})
        except (psutil.NoSuchProcess,psutil.AccessDenied):
            pass
    return sorted(rows,key=lambda x:(x["cpu_percent"],x["memory_percent"]),reverse=True)[:limit]

def collect()->dict:
    disks=[]
    for part in psutil.disk_partitions(all=False):
        try:
            u=psutil.disk_usage(part.mountpoint)
            disks.append({"device":part.device,"mount":part.mountpoint,"total_gb":round(u.total/2**30,1),"free_gb":round(u.free/2**30,1),"used_percent":u.percent})
        except OSError:
            pass
    nets={}
    for name,addrs in psutil.net_if_addrs().items():
        nets[name]=[{"address":a.address,"family":str(a.family)} for a in addrs]
    vm=psutil.virtual_memory()
    return {
      "generated_at":datetime.now(timezone.utc).isoformat(),
      "hostname":socket.gethostname(),
      "os":platform.platform(),
      "boot_time":datetime.fromtimestamp(psutil.boot_time(),timezone.utc).isoformat(),
      "cpu":{"logical":psutil.cpu_count(),"physical":psutil.cpu_count(logical=False),"percent":psutil.cpu_percent(interval=.4)},
      "memory":{"total_gb":round(vm.total/2**30,1),"available_gb":round(vm.available/2**30,1),"percent":vm.percent},
      "disks":disks,
      "network_interfaces":nets,
      "connectivity":{"internet_ip_test":ping("1.1.1.1"),"dns":dns_test()},
      "top_processes":top_processes()
    }

def recommendations(data:dict)->list[str]:
    tips=[]
    if data["cpu"]["percent"]>=90: tips.append("CPU acima de 90 percent no momento da coleta.")
    if data["memory"]["percent"]>=90: tips.append("Memoria acima de 90 percent.")
    for d in data["disks"]:
        if d["used_percent"]>=90: tips.append(f"Disco {d['mount']} acima de 90 percent de uso.")
    if not data["connectivity"]["internet_ip_test"]: tips.append("Falha no teste de conectividade com IP externo.")
    if not data["connectivity"]["dns"]["ok"]: tips.append("Falha na resolucao DNS.")
    if not tips: tips.append("Nenhum alerta basico detectado nesta coleta.")
    return tips

def main():
    ap=argparse.ArgumentParser(description="IT Support diagnostic toolkit")
    ap.add_argument("--report",default="")
    ap.add_argument("--compact",action="store_true")
    args=ap.parse_args()
    data=collect(); data["recommendations"]=recommendations(data)
    print(json.dumps(data,indent=None if args.compact else 2,ensure_ascii=False))
    if args.report:
        p=Path(args.report); p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")

if __name__=="__main__":
    main()
