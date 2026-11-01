"""Local teacher interface. Run python app.py then open http://127.0.0.1:8765."""
import argparse,hashlib,json,secrets,webbrowser
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from engine import solve,validate,fingerprint,ValidationError
ROOT=Path(__file__).resolve().parent
TOKEN=secrets.token_urlsafe(32)
def case_fingerprint(case):
 raw=json.dumps(case,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
 return hashlib.sha256(raw).hexdigest()
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def send(self,status,data,mime='application/json'):
  raw=data.encode() if isinstance(data,str) else json.dumps(data,ensure_ascii=False,allow_nan=False).encode()
  self.send_response(status);self.send_header('Content-Type',mime+'; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('X-Frame-Options','DENY');self.end_headers();self.wfile.write(raw)
 def do_GET(self):
  path=urlparse(self.path).path
  if path=='/':self.send(200,(ROOT/'interface.html').read_text().replace('__TOKEN__',TOKEN),'text/html')
  elif path=='/api/examples':self.send(200,[json.loads(p.read_text()) for p in sorted((ROOT/'examples').glob('case_*.json'))])
  else:self.send(404,{'error':'Not found'})
 def do_POST(self):
  if self.headers.get('X-EvidenceBudget-Token')!=TOKEN:return self.send(403,{'error':'Reload the app before submitting.'})
  if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.send(415,{'error':'JSON required'})
  try:
   n=int(self.headers.get('Content-Length',0))
   if not 0<n<=1000000:return self.send(413,{'error':'Input must be below 1 MB'})
   payload=json.loads(self.rfile.read(n));case=payload['case']
   if self.path=='/api/approve':
    reviewer=payload.get('reviewer','').strip()
    if not reviewer:raise ValidationError('Enter your reviewer name or identifier')
    for cp in case['checkpoints']:
     cp['approval']={'status':'teacher_approved','reviewer':reviewer,'fingerprint':fingerprint(cp)}
    validate(case)
    review_confirmation={'status':'confirmed','reviewer':reviewer,'confirmed_at':datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z'),'case_fingerprint':case_fingerprint(case)}
    return self.send(200,{'case':case,'review_confirmation':review_confirmation})
   if self.path=='/api/validate':
    validate(case);return self.send(200,{'valid':True})
   if self.path=='/api/solve':return self.send(200,{'result':solve(case)})
   return self.send(404,{'error':'Not found'})
  except (ValueError,TypeError,KeyError,AttributeError,ValidationError) as e:self.send(400,{'error':str(e)})
def main():
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8765);p.add_argument('--no-browser',action='store_true');p.add_argument('--host',default='127.0.0.1');a=p.parse_args()
 server=ThreadingHTTPServer((a.host,a.port),Handler);url=f'http://127.0.0.1:{a.port}'
 print('EvidenceBudget teacher interface: '+url+'\nKeep this window open. Press Ctrl+C to stop.')
 if not a.no_browser:webbrowser.open(url)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close()
if __name__=='__main__':main()
