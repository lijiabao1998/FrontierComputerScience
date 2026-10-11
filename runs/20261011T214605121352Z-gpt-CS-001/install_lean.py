"""User-authorized official side-by-side tool installation; no research."""
from pathlib import Path
import ctypes,datetime as dt,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"installation";OUT.mkdir(exist_ok=True)
ELAN=Path(r"C:\Users\Leon1\.elan")
TARGET=ELAN/"toolchains/leanprover--lean4---v4.18.0"
OLD=[ELAN/"settings.toml"]
for ver in ["v4.33.1","v4.34.0-rc2"]:
 for exe in ["lean.exe","lake.exe"]:
  OLD.append(ELAN/"toolchains"/("leanprover--lean4---"+ver)/"bin"/exe)
def snapshot():
 return {str(p):{"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in OLD}
before=snapshot()
(OUT/"BEFORE.json").write_text(json.dumps(before,indent=2)+"\n",encoding="utf-8")
k=ctypes.WinDLL("kernel32",use_last_error=True)
k.GetCurrentProcess.restype=ctypes.c_void_p
k.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
if not k.SetProcessAffinityMask(k.GetCurrentProcess(),1):raise ctypes.WinError(ctypes.get_last_error())
command=[str(ELAN/"bin/elan.exe"),"toolchain","install","leanprover/lean4:v4.18.0"]
started=dt.datetime.now(dt.timezone.utc)
launch={"started_at":started.isoformat(),"command":command,"cwd":str(ROOT),"affinity_mask":1,"scientific_execution":False,"timeout_seconds":1200,"official_release":"https://github.com/leanprover/lean4/releases/tag/v4.18.0","default_or_override_change_requested":False}
(OUT/"launch.json").write_text(json.dumps(launch,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"installation":"STARTED","started_at":launch["started_at"],"command":command}),flush=True)
with (OUT/"stdout.txt").open("xb") as out,(OUT/"stderr.txt").open("xb") as err:
 try:
  result=subprocess.run(command,cwd=ROOT,stdout=out,stderr=err,timeout=1200)
  code=result.returncode;timed_out=False
 except subprocess.TimeoutExpired:
  code=None;timed_out=True
after=snapshot()
(OUT/"AFTER.json").write_text(json.dumps(after,indent=2)+"\n",encoding="utf-8")
versions=[]
if code==0 and (TARGET/"bin/lean.exe").exists() and (TARGET/"bin/lake.exe").exists():
 for exe in ["lean","lake"]:
  cmd=[str(TARGET/"bin"/(exe+".exe")),"--version"]
  p=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
  (OUT/(exe+"-version.stdout.txt")).write_bytes(p.stdout)
  (OUT/(exe+"-version.stderr.txt")).write_bytes(p.stderr)
  versions.append({"command":cmd,"exit_code":p.returncode,"stdout":p.stdout.decode("utf-8",errors="replace"),"stderr":p.stderr.decode("utf-8",errors="replace"),"sha256":hashlib.sha256(Path(cmd[0]).read_bytes()).hexdigest()})
obj={"finished_at":dt.datetime.now(dt.timezone.utc).isoformat(),"install_exit_code":code,"timed_out":timed_out,"old_settings_and_binaries_unchanged":before==after,"target":str(TARGET),"versions":versions,"scientific_execution":False}
obj["status"]="INSTALLATION_PASS" if code==0 and before==after and len(versions)==2 and all(x["exit_code"]==0 for x in versions) and "version 4.18.0," in versions[0]["stdout"] and "Lean version 4.18.0" in versions[1]["stdout"] else "INSTALLATION_FAILED"
(OUT/"RESULT.json").write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")
print(json.dumps(obj),flush=True)
sys.exit(0 if obj["status"]=="INSTALLATION_PASS" else 1)

