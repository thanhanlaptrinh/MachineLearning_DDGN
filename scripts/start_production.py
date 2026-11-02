"""Production process supervisor: Express listens on PORT, Flask is internal."""
import os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
children=[]
def stop(*_):
 for p in children:
  if p.poll() is None:p.terminate()
def main():
 signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
 try:
  children.extend([subprocess.Popen([sys.executable,'service/predict_service.py'],cwd=ROOT),subprocess.Popen(['node','server.js'],cwd=ROOT)])
  while all(p.poll() is None for p in children):time.sleep(.5)
 finally:
  stop()
  for p in children:
   try:p.wait(timeout=10)
   except subprocess.TimeoutExpired:p.kill()
if __name__=='__main__':main()
