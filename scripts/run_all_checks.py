"""Chạy kiểm chứng đã lưu và HTTP/browser; không gọi fit, không tuning lại."""
import json,os,subprocess,sys,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 env={**os.environ,'OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'2'}
 commands=[[sys.executable,'scripts/prepare_vnd_audit.py'],[sys.executable,'scripts/export_vnd.py'],[sys.executable,'scripts/prepare_final_report.py'],*[ [sys.executable,'scripts/'+p] for p in ['verify_vnd.py','verify_dynamic.py','verify_training_report.py','verify_round1.py','verify_portable_xgboost.py','verify_completion.py']]]
 results=[];children=[]
 def run(cmd):
  p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True);row={'command':[Path(cmd[0]).name,*cmd[1:]],'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};results.append(row);print(' '.join(cmd[1:]),p.returncode,p.stdout.strip(),flush=True)
  (ROOT/'results/final_test_results.json').write_text(json.dumps({'status':'RUNNING' if p.returncode==0 else 'FAIL','results':results},ensure_ascii=False,indent=2))
  if p.returncode:raise RuntimeError(p.stderr or p.stdout)
 try:
  for cmd in commands:run(cmd)
  with open(ROOT/'results/server_check.log','w') as f:
   children=[subprocess.Popen([sys.executable,'service/predict_service.py'],cwd=ROOT,env=env,stdout=f,stderr=f),subprocess.Popen(['node','server.js'],cwd=ROOT,env=env,stdout=f,stderr=f)]
   for _ in range(120):
    try:
     with urllib.request.urlopen('http://127.0.0.1:3000/api/health',timeout=1) as response:
      if response.status==200:break
    except Exception:time.sleep(.25)
   else:raise RuntimeError('Servers did not become ready')
   for cmd in [['node','scripts/smoke_http.mjs'],['node','scripts/smoke_dynamic_http.mjs'],['node','scripts/browser_check.mjs']]:run(cmd)
 finally:
  for p in children:p.terminate()
  for p in children:p.wait(timeout=15)
 (ROOT/'results/final_test_results.json').write_text(json.dumps({'status':'PASS','results':results,'scope':'CV searches are preserved historical runs; current checks reproduce saved inference, split, source labels, metrics, Id invariance and browser behavior.'},ensure_ascii=False,indent=2))
 print('ALL REQUIRED CHECKS PASS',flush=True)
if __name__=='__main__':main()
