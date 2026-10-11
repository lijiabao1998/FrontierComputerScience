"""New isolated pinned source only; capture failures and preserve original repos."""
from pathlib import Path
import ctypes,datetime as dt,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent;OUT=ROOT/"evidence/source-commands";OUT.mkdir(parents=True,exist_ok=True)
k=ctypes.WinDLL("kernel32",use_last_error=True);k.GetCurrentProcess.restype=ctypes.c_void_p;k.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
if not k.SetProcessAffinityMask(k.GetCurrentProcess(),1):raise ctypes.WinError(ctypes.get_last_error())
ENV=dict(os.environ,GIT_TERMINAL_PROMPT="0",GCM_INTERACTIVE="Never")
REPO=ROOT/"FrontierComputerScience";HEAD="8e21cd467c8aeae3c56f44c95e7f6df7103ec403"
def cmd(label,args,timeout=120):
 path=OUT/label;start=dt.datetime.now(dt.timezone.utc);code=None;timeout_hit=False
 with path.with_suffix(".stdout.txt").open("xb") as out,path.with_suffix(".stderr.txt").open("xb") as err:
  try:code=subprocess.run(args,env=ENV,stdout=out,stderr=err,timeout=timeout).returncode
  except subprocess.TimeoutExpired:timeout_hit=True
 record={"command":args,"started_at":start.isoformat(),"finished_at":dt.datetime.now(dt.timezone.utc).isoformat(),"exit_code":code,"timeout":timeout_hit,"scientific_execution":False,"cpu_affinity_mask":1}
 path.with_suffix(".json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8");print(json.dumps(record),flush=True)
 if code!=0 or timeout_hit:raise RuntimeError(label+" failed; raw outputs retained")
 return path.with_suffix(".stdout.txt").read_text(encoding="utf-8")
git=["git","-c","core.longpaths=true","-c","pack.threads=1","-c","credential.interactive=false","-c","core.askPass=","-c","credential.modalPrompt=false"]
if REPO.exists():raise RuntimeError("Isolated clone path already exists; do not overwrite")
cmd("CS-clone",git+["clone","--filter=blob:none","--no-checkout","https://github.com/lijiabao1998/FrontierComputerScience.git",str(REPO)])
cmd("CS-checkout",git+["-C",str(REPO),"checkout","-b","gpt/CS-001-kernel-independent-20261011",HEAD])
actual=cmd("CS-head",git+["-C",str(REPO),"rev-parse","HEAD"]).strip()
assert actual==HEAD
assert not cmd("CS-status",git+["-C",str(REPO),"status","--porcelain"]).strip()
cmd("CS-remote-refs",git+["-C",str(REPO),"ls-remote","--heads","origin","main","codex/CS-001-lean-baseline-20261009t103941763440z","gpt/CS-001-kernel-independent-20261011"])
print(json.dumps({"source_head":actual,"working_tree_clean":True,"scientific_execution":"NOT_RUN"}))

