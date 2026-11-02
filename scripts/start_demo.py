"""Chạy Flask + Express bằng đúng Python hiện tại; Ctrl+C dừng cả hai."""
from pathlib import Path
import argparse,os,shutil,socket,subprocess,sys,time,urllib.request,webbrowser
ROOT=Path(__file__).resolve().parents[1]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--no-browser',action='store_true');args=parser.parse_args()
 node=shutil.which('node')
 if not node: raise SystemExit('Chưa có Node.js trong PATH.')
 if not (ROOT/'node_modules/express').exists():raise SystemExit('Chưa cài thư viện Node: chạy npm ci trước.')
 for port in (3000,5001):
  with socket.socket() as sock:
   if sock.connect_ex(('127.0.0.1',port))==0:raise SystemExit(f'Cổng {port} đang được dùng. Dừng cửa sổ demo cũ rồi thử lại.')
 env={**os.environ,'PORT':'3000','FLASK_PORT':'5001','PREDICT_SERVICE_URL':'http://127.0.0.1:5001'}
 children=[]
 try:
  children.append(subprocess.Popen([sys.executable,'service/predict_service.py'],cwd=ROOT,env=env))
  children.append(subprocess.Popen([node,'server.js'],cwd=ROOT,env=env))
  for _ in range(120):
   if any(p.poll() is not None for p in children):raise RuntimeError('Một server đã dừng. Xem lỗi ở phía trên.')
   try:
    with urllib.request.urlopen('http://127.0.0.1:3000/api/health',timeout=1) as res:
     if res.status==200:break
   except Exception:time.sleep(.5)
  else:raise RuntimeError('Server chưa sẵn sàng sau thời gian chờ.')
  print('Demo sẵn sàng: http://localhost:3000/#/data\nNhấn Ctrl+C để dừng.',flush=True)
  if not args.no_browser:webbrowser.open('http://localhost:3000/#/data')
  while all(p.poll() is None for p in children):time.sleep(.5)
 except KeyboardInterrupt:pass
 finally:
  for p in children:
   if p.poll() is None:p.terminate()
  for p in children:
   try:p.wait(timeout=5)
   except subprocess.TimeoutExpired:p.kill()
if __name__=='__main__':main()
