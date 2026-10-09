#!/usr/bin/env python3
"""Local-only reader server; atomic, revision-checked project progress persistence."""
import argparse
import json
import math
import os
import tempfile
import threading
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MAX_BODY = 10 * 1024 * 1024


def normalize_progress(raw, entry_ids, reading_ids):
    if not isinstance(raw, dict):
        raise ValueError('progress must be an object')
    def ids(field):
        value = raw.get(field, [])
        if not isinstance(value, list):
            raise ValueError(f'{field} must be a list')
        return list(dict.fromkeys(x for x in value if isinstance(x, str) and x in entry_ids))
    def mapping(field):
        value = raw.get(field, {})
        if not isinstance(value, dict):
            raise ValueError(f'{field} must be an object')
        return value
    def fraction(value):
        return min(1, max(0, value)) if type(value) in (int, float) and math.isfinite(value) else 0
    def timestamp(value):
        return int(value) if type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 10**15 else 0
    reading = {}
    for key, value in mapping('reading').items():
        if key not in reading_ids or not isinstance(value, dict):
            continue
        reading[key] = {
            'fraction': fraction(value.get('fraction')), 'maxFraction': fraction(value.get('maxFraction')),
            'anchor': str(value.get('anchor', ''))[:100], 'offset': fraction(value.get('offset')),
            'finished': value.get('finished') is True, 'updatedAt': timestamp(value.get('updatedAt')),
        }
    review = {}
    for key, value in mapping('review').items():
        if key in entry_ids and isinstance(value, dict):
            review[key] = {'due': timestamp(value.get('due')), 'interval': min(30, max(0, timestamp(value.get('interval')))),
                           'count': min(10000, timestamp(value.get('count'))), 'rating': 'know' if value.get('rating') == 'know' else 'again'}
    prefs = mapping('prefs')
    return {
        'learned': ids('learned'), 'saved': ids('saved'), 'passed': ids('passed'), 'mistakes': ids('mistakes'),
        'last': raw.get('last') if isinstance(raw.get('last'), str) and raw['last'] in entry_ids else None,
        'lastRead': raw.get('lastRead') if isinstance(raw.get('lastRead'), str) and raw['lastRead'] in reading_ids else None,
        'notes': {k: v[:5000] for k, v in mapping('notes').items() if k in entry_ids and isinstance(v, str)},
        'reading': reading, 'review': review,
        'prefs': {'fontSize': 'large' if prefs.get('fontSize') == 'large' else 'normal', 'focus': prefs.get('focus') is True,
                  'language': prefs.get('language') if prefs.get('language') in ('zh', 'en', 'bi') else 'zh'},
    }


class Conflict(Exception):
    pass


class ProgressStore:
    def __init__(self, data_dir, book):
        self.directory = Path(data_dir)
        self.path = self.directory / 'progress.json'
        self.backup = self.directory / 'progress.previous.json'
        self.lock = threading.RLock()
        self.entries = {e['id'] for e in book['entries']}
        self.sections = set(book['readingOrder'])

    def read(self):
        with self.lock:
            if not self.path.exists():
                return {'format': 2, 'revision': 0, 'updatedAt': None, 'exists': False,
                        'progress': normalize_progress({}, self.entries, self.sections)}
            # Corrupt or unknown-format files are never silently replaced.
            data = json.loads(self.path.read_text(encoding='utf-8'))
            if data.get('format') != 2 or type(data.get('revision')) is not int or data['revision'] < 1:
                raise ValueError('Invalid progress file. Restore progress.previous.json or import a backup.')
            return {**data, 'exists': True, 'progress': normalize_progress(data['progress'], self.entries, self.sections)}

    def _atomic(self, path, text):
        fd, temporary = tempfile.mkstemp(dir=self.directory, prefix='.progress-', suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as output:
                output.write(text); output.flush(); os.fsync(output.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def write(self, raw, revision):
        normalized = normalize_progress(raw, self.entries, self.sections)
        with self.lock:
            current = self.read()
            if type(revision) is not int or revision != current['revision']:
                raise Conflict('Project progress changed in another tab. Reload before saving.')
            self.directory.mkdir(parents=True, exist_ok=True)
            result = {'format': 2, 'revision': revision + 1, 'updatedAt': datetime.now(timezone.utc).isoformat(), 'progress': normalized}
            if current['exists']:
                self._atomic(self.backup, self.path.read_text(encoding='utf-8'))
            self._atomic(self.path, json.dumps(result, ensure_ascii=False, indent=2) + '\n')
            return {**result, 'exists': True}


def handler_for(site_dir, store):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(site_dir), **kwargs)

        def json_response(self, status, data):
            body = json.dumps(data, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers(); self.wfile.write(body)

        def trusted(self, write=False):
            port = self.server.server_port
            hosts = {f'127.0.0.1:{port}', f'localhost:{port}'}
            if self.headers.get('Host') not in hosts:
                return False
            if write:
                origin = self.headers.get('Origin')
                if origin is not None and origin not in {f'http://{h}' for h in hosts}:
                    return False
                if self.headers.get('Sec-Fetch-Site') == 'cross-site':
                    return False
                if self.headers.get('X-Local-Progress') != '1':
                    return False
            return True

        def do_GET(self):
            if not self.trusted():
                return self.json_response(403, {'error': 'Local host only'})
            if urlsplit(self.path).path == '/runtime-config.json':
                return self.json_response(200, {'progressMode': 'project'})
            if urlsplit(self.path).path == '/api/progress':
                try:
                    return self.json_response(200, {**store.read(), 'storagePath': 'learning-data/progress.json'})
                except (OSError, ValueError, KeyError):
                    return self.json_response(500, {'error': '项目进度文件无法读取，原文件未修改。请检查或恢复备份。'})
            if urlsplit(self.path).path.startswith('/api/'):
                return self.json_response(404, {'error': 'Unknown API'})
            return super().do_GET()

        def do_HEAD(self):
            if not self.trusted():
                self.send_error(403); return
            super().do_HEAD()

        def do_PUT(self):
            if not self.trusted(write=True):
                return self.json_response(403, {'error': 'Same-origin local client required'})
            if urlsplit(self.path).path != '/api/progress':
                return self.json_response(404, {'error': 'Unknown API'})
            if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
                return self.json_response(415, {'error': 'JSON required'})
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= MAX_BODY:
                    return self.json_response(413, {'error': '记录过大，请导出备份后精简笔记。'})
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict) or 'progress' not in body or 'revision' not in body:
                    raise ValueError('Missing progress or revision')
                result = store.write(body['progress'], body['revision'])
                return self.json_response(200, {**result, 'storagePath': 'learning-data/progress.json'})
            except Conflict:
                return self.json_response(409, {'error': '另一个页面已修改项目记录。请先导出本机草稿，再载入项目记录。'})
            except (ValueError, KeyError, TypeError):
                return self.json_response(400, {'error': '记录格式无效，项目原文件未修改。'})
            except OSError:
                return self.json_response(500, {'error': '无法写入项目目录，请检查空间和权限。'})

        def list_directory(self, path):
            self.send_error(404); return None

        def end_headers(self):
            self.send_header('X-Content-Type-Options', 'nosniff')
            if not self.path.startswith('/api/'):
                self.send_header('Cache-Control', 'no-cache')
            super().end_headers()

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=4173)
    parser.add_argument('--data-dir', type=Path, default=ROOT / 'learning-data')
    args = parser.parse_args()
    site = ROOT / 'build/web'
    if not (site / 'book.json').exists():
        parser.error('Run make web first')
    book = json.loads((site / 'book.json').read_text())
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_for(site, ProgressStore(args.data_dir, book)))
    print(f'Reader: http://127.0.0.1:{server.server_port}', flush=True)
    print(f'Progress: {args.data_dir / "progress.json"}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
