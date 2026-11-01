import json,threading,unittest,urllib.request,urllib.error,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from http.server import ThreadingHTTPServer
from app import Handler,TOKEN
class AppTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler);cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.url='http://127.0.0.1:'+str(cls.server.server_address[1])
 @classmethod
 def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()
 def post(self,path,data,token=TOKEN):
  req=urllib.request.Request(self.url+'/api/'+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json','X-EvidenceBudget-Token':token})
  return json.load(urllib.request.urlopen(req))
 def case(self):return json.load(urllib.request.urlopen(self.url+'/api/examples'))[0]
 def test_home(self):
  with urllib.request.urlopen(self.url) as r:
   self.assertIn('EvidenceBudget',r.read().decode());self.assertEqual(r.headers['X-Frame-Options'],'DENY')
 def test_examples(self):self.assertEqual(len(json.load(urllib.request.urlopen(self.url+'/api/examples'))),6)
 def test_solve(self):self.assertEqual(self.post('solve',{'case':self.case()})['result']['minimum_teacher_minutes_with_student_limit'],160)
 def test_stale_review_and_reapproval(self):
  c=self.case();c['checkpoints'][0]['prompt']='Changed supervised task'
  with self.assertRaises(urllib.error.HTTPError) as e:self.post('solve',{'case':c})
  self.assertEqual(e.exception.code,400)
  c=self.post('approve',{'case':c,'reviewer':'Pilot reviewer'})['case'];self.assertEqual(self.post('solve',{'case':c})['result']['status'],'feasible')
 def test_no_reviewer(self):
  with self.assertRaises(urllib.error.HTTPError) as e:self.post('approve',{'case':self.case(),'reviewer':''})
  self.assertEqual(e.exception.code,400)
 def test_csrf(self):
  with self.assertRaises(urllib.error.HTTPError) as e:self.post('solve',{'case':self.case()},'wrong')
  self.assertEqual(e.exception.code,403)
 def test_validate(self):self.assertTrue(self.post('validate',{'case':self.case()})['valid'])
 def test_invalid_import(self):
  with self.assertRaises(urllib.error.HTTPError) as e:self.post('validate',{'case':{}})
  self.assertEqual(e.exception.code,400)
 def test_no_file_traversal(self):
  with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(self.url+'/../engine.py')
  self.assertEqual(e.exception.code,404)
if __name__=='__main__':unittest.main()
