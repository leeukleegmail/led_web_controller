#!/usr/bin/env python3
"""Reusable local web UI preview server.

Serve a project's static files and mock simple POST endpoints so a browser UI can
be previewed on a desktop without the target device being connected.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


@dataclass
class PreviewState:
    color: str = '#ffffff'
    party_mode: bool = False
    party_speed: int = 7

    def handle_post(self, path: str, body: str) -> str:
        body = body.strip()

        if path == '/set_color':
            if body.startswith('#') and len(body) == 7:
                self.color = body
            print('Preview color -> %s' % self.color)
            return 'Color set'

        if path == '/set_mode':
            mode_value = body.lower()
            self.party_mode = mode_value in ('party=on', 'party=true', 'party=1', 'on', 'true', '1')
            print('Preview party mode -> %s' % ('on' if self.party_mode else 'off'))
            return 'Party mode on' if self.party_mode else 'Party mode off'

        if path == '/set_party_speed':
            try:
                speed = int(body)
            except ValueError:
                speed = self.party_speed

            self.party_speed = min(10, max(1, speed))
            print('Preview party speed -> %d' % self.party_speed)
            return 'Party speed set'

        print('Preview POST %s -> %s' % (path, body))
        return 'OK'

    def as_dict(self) -> dict:
        return {
            'color': self.color,
            'party_mode': self.party_mode,
            'party_speed': self.party_speed,
        }


def build_handler(root: Path, index_file: str, pin: str, pin_disabled: bool, state: PreviewState):
    class PreviewHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(root), **kwargs)

        def _send_text(self, body: str, content_type: str = 'text/plain; charset=utf-8', status: int = 200):
            data = body.encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            request_path = self.path.split('?', 1)[0]

            if request_path == '/__preview/state':
                self._send_text(json.dumps(state.as_dict(), indent=2), 'application/json; charset=utf-8')
                return

            if request_path in ('/', '/%s' % index_file):
                index_path = root / index_file
                try:
                    html = index_path.read_text(encoding='utf-8')
                except OSError:
                    self._send_text('Missing %s' % index_file, status=404)
                    return

                html = html.replace("let PIN = '0000';", "let PIN = %s;" % json.dumps(pin))
                html = html.replace('let PIN_DISABLED = false;', 'let PIN_DISABLED = %s;' % str(pin_disabled).lower())
                self._send_text(html, 'text/html; charset=utf-8')
                return

            super().do_GET()

        def do_POST(self):
            request_path = self.path.split('?', 1)[0]
            length = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(length).decode('utf-8', 'ignore') if length else ''
            response = state.handle_post(request_path, body)
            self._send_text(response)

    return PreviewHandler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Preview a web UI locally with mocked device endpoints.')
    parser.add_argument('--root', default='.', help='Project folder to serve (default: current directory)')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind (default: 8000)')
    parser.add_argument('--index', default='index.html', help='Index file to serve (default: index.html)')
    parser.add_argument('--pin', default='0000', help='PIN to inject into the served page (default: 0000)')
    parser.add_argument('--pin-disabled', action='store_true', help='Skip the PIN prompt in preview mode')
    return parser.parse_args()


def main():
    args = parse_args()
    root = Path(args.root).resolve()
    state = PreviewState()
    handler = build_handler(root, args.index, args.pin, args.pin_disabled, state)
    server = ThreadingHTTPServer((args.host, args.port), handler)

    print('Preview server running at http://%s:%d' % (args.host, args.port))
    print('Serving files from %s' % root)
    print('Press Ctrl+C to stop.')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nPreview server stopped.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
