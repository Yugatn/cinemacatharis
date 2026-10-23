"""Minimal JSON HTTP integration endpoint. Development use only; deploy behind auth, TLS and limits."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from .policy import analyze_document

MAX_BYTES = 1_000_000

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/v1/analyze":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", "-1"))
            if size < 0 or size > MAX_BYTES:
                self.send_error(413)
                return
            payload = json.loads(self.rfile.read(size))
            output = json.dumps(analyze_document(payload), ensure_ascii=False).encode()
            self.send_response(200)
        except (ValueError, TypeError, KeyError) as exc:
            output = json.dumps({"error": str(exc)}).encode()
            self.send_response(400)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(output)))
        self.end_headers()
        self.wfile.write(output)

def main():
    # Loopback by default: no authentication or rate limiting in this demo server.
    print("Cinema Catharsis development API on http://127.0.0.1:8765")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()

if __name__ == "__main__":
    main()
