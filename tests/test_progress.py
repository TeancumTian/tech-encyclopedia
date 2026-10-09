"""Disk persistence and real local HTTP boundary tests; no user progress is touched."""
import concurrent.futures
import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path
from http.server import ThreadingHTTPServer
from scripts.serve_web import ProgressStore, Conflict, handler_for

BOOK = {'entries': [{'id': 'logic-gate'}, {'id': 'bit-byte'}], 'readingOrder': ['entry/logic-gate', 'document/howto']}


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = ProgressStore(Path(self.temp.name)/'data', BOOK)
    def tearDown(self):
        self.temp.cleanup()
    def test_save_survives_store_restart_and_keeps_previous_version(self):
        saved = self.store.write({'notes': {'logic-gate': '自己的理解'}, 'reading': {'entry/logic-gate': {'fraction': .58, 'anchor': 'how', 'finished': True}}, 'lastRead': 'entry/logic-gate'}, 0)
        self.assertEqual(saved['revision'], 1)
        second = ProgressStore(self.store.directory, BOOK)
        self.assertEqual(second.read()['progress']['notes']['logic-gate'], '自己的理解')
        self.assertEqual(second.read()['progress']['reading']['entry/logic-gate']['fraction'], .58)
        second.write({'saved': ['bit-byte']}, 1)
        self.assertEqual(json.loads(second.backup.read_text())['progress']['notes']['logic-gate'], '自己的理解')
        self.assertFalse(list(second.directory.glob('*.tmp')))
    def test_stale_revision_does_not_overwrite_newer_notes(self):
        self.store.write({'notes': {'logic-gate': 'new'}}, 0)
        with self.assertRaises(Conflict): self.store.write({'notes': {'logic-gate': 'stale'}}, 0)
        self.assertEqual(self.store.read()['progress']['notes']['logic-gate'], 'new')
    def test_concurrent_writers_cannot_both_win(self):
        def attempt(i):
            try: self.store.write({'notes': {'logic-gate': str(i)}}, 0); return True
            except Conflict: return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sum(pool.map(attempt, [1, 2])), 1)
    def test_corrupt_file_is_preserved(self):
        self.store.directory.mkdir(); self.store.path.write_text('{broken')
        with self.assertRaises(ValueError): self.store.write({}, 0)
        self.assertEqual(self.store.path.read_text(), '{broken')
    def test_unknown_ids_and_invalid_values_cannot_enter_disk(self):
        result = self.store.write({'saved': ['logic-gate', 'missing', 'logic-gate'], 'notes': {'missing': 'x', 'bit-byte': 5}, 'reading': {'document/howto': {'fraction': 9, 'offset': -2}, 'bad': {}}, 'review': {'logic-gate': {'due': -1, 'interval': 100}}}, 0)['progress']
        self.assertEqual(result['saved'], ['logic-gate']); self.assertEqual(result['notes'], {})
        self.assertEqual(result['reading']['document/howto']['fraction'], 1)
        self.assertEqual(result['reading']['document/howto']['offset'], 0)
        self.assertNotIn('bad', result['reading'])
    def test_record_reset_is_explicit_and_backed_up(self):
        self.store.write({'notes': {'logic-gate': 'keep a backup'}}, 0)
        self.store.write({}, 1)
        self.assertEqual(self.store.read()['progress']['notes'], {})
        self.assertEqual(json.loads(self.store.backup.read_text())['progress']['notes']['logic-gate'], 'keep a backup')


class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.site = Path(self.temp.name)/'site'; self.site.mkdir(); (self.site/'index.html').write_text('<h1>Reader</h1>')
        self.store = ProgressStore(Path(self.temp.name)/'private-data', BOOK)
        handler = handler_for(self.site, self.store)
        handler.log_message = lambda *args: None
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True); self.thread.start()
    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(); self.temp.cleanup()
    def request(self, method='GET', path='/api/progress', data=None, headers=None):
        connection=http.client.HTTPConnection('127.0.0.1', self.server.server_port)
        body=json.dumps(data) if data is not None else None
        standard={'Content-Type':'application/json','X-Local-Progress':'1'} if method=='PUT' else {}
        connection.request(method,path,body,{**standard,**(headers or {})})
        response=connection.getresponse(); result=(response.status,response.read()); connection.close(); return result
    def test_http_get_put_read_and_conflict(self):
        self.assertEqual(json.loads(self.request(path='/runtime-config.json')[1]), {'progressMode': 'project'})
        status, body=self.request(); self.assertEqual(status,200); self.assertFalse(json.loads(body)['exists'])
        status,_=self.request('PUT',data={'revision':0,'progress':{'notes':{'bit-byte':'记住了'}}}); self.assertEqual(status,200)
        self.assertEqual(json.loads(self.request()[1])['progress']['notes']['bit-byte'],'记住了')
        self.assertEqual(self.request('PUT',data={'revision':0,'progress':{}})[0],409)
        self.assertEqual(self.request(path='/private-data/progress.json')[0],404)
    def test_cross_site_host_and_malformed_writes_rejected(self):
        self.assertEqual(self.request(headers={'Host':'evil.example'})[0],403)
        self.assertEqual(self.request('PUT',data={'revision':0,'progress':{}},headers={'Origin':'https://evil.example'})[0],403)
        self.assertEqual(self.request('PUT',data={'revision':0,'progress':{}},headers={'X-Local-Progress':''})[0],403)
        self.assertEqual(self.request('PUT',data={'revision':0,'progress':{}},headers={'Content-Type':'text/plain'})[0],415)
        self.assertEqual(self.request('PUT',data=[])[0],400)
        self.assertFalse(self.store.path.exists())


if __name__ == '__main__': unittest.main()
