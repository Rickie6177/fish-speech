"""
Simple reverse proxy + static file server for Fish Speech WebUI.
Serves webui.html on port 8181 and proxies /api/* requests to WSL Docker.
"""
import http.server
import subprocess
import urllib.request
import urllib.error
import os
import sys

PORT = 8181
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

def get_wsl_ip():
    """Get WSL2 IP address by reading /etc/resolv.conf via wsl."""
    # Try common WSL2 IP detection methods
    import socket
    
    # Method 1: Try reading from a cached file
    cache_file = os.path.join(STATIC_DIR, ".wsl_ip")
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            ip = f.read().strip()
            if ip:
                return ip
    
    # Method 2: Try subprocess with stdin closed to avoid hanging
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.run(
            ["wsl", "-d", "Ubuntu", "-u", "root", "-e", "hostname", "-I"],
            capture_output=True, timeout=10, startupinfo=si,
            stdin=subprocess.DEVNULL
        )
        raw = result.stdout
        ip = raw.decode("utf-8", errors="ignore").strip().split()[0]
        # Cache it
        with open(cache_file, "w") as f:
            f.write(ip)
        return ip
    except Exception as e:
        print(f"[Warning] Could not detect WSL IP: {e}")
    
    # Method 3: Fallback - try common WSL2 subnet
    for ip in ["172.29.46.18", "172.17.0.1", "127.0.0.1"]:
        try:
            s = socket.create_connection((ip, 8080), timeout=2)
            s.close()
            return ip
        except Exception:
            continue
    return "127.0.0.1"

WSL_IP = get_wsl_ip()
API_BASE = f"http://{WSL_IP}:8080"
print(f"[Proxy] WSL IP detected: {WSL_IP}")
print(f"[Proxy] API target: {API_BASE}")


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith("/v1/"):
            self._proxy("GET")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/v1/"):
            self._proxy("POST")
        else:
            self.send_error(404)

    def do_DELETE(self):
        if self.path.startswith("/v1/"):
            self._proxy("DELETE")
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def _proxy(self, method):
        target_url = API_BASE + self.path
        try:
            # Read request body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

            # Build proxy request
            req = urllib.request.Request(target_url, data=body, method=method)
            # Forward content-type header
            ct = self.headers.get("Content-Type")
            if ct:
                req.add_header("Content-Type", ct)

            # Execute request
            with urllib.request.urlopen(req, timeout=120) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                # Forward response headers
                for key in ["Content-Type", "Content-Disposition"]:
                    val = resp.headers.get(key)
                    if val:
                        self.send_header(key, val)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", len(resp_body))
                self.end_headers()
                self.wfile.write(resp_body)

        except urllib.error.HTTPError as e:
            resp_body = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", e.headers.get("Content-Type", "text/plain"))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", len(resp_body))
            self.end_headers()
            self.wfile.write(resp_body)
        except Exception as e:
            msg = str(e).encode()
            try:
                self.send_response(502)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", len(msg))
                self.end_headers()
                self.wfile.write(msg)
            except Exception:
                pass  # Client already disconnected, ignore broken pipe

    def log_message(self, format, *args):
        # Cleaner log — args[0] may be a str or an HTTPStatus enum, convert safely
        first = str(args[0]) if args else ""
        if "/v1/" in first:
            print(f"[Proxy] {first}")
        elif "favicon" not in first:
            print(f"[Static] {first}")


if __name__ == "__main__":
    print(f"=" * 50)
    print(f"  Fish Speech TTS WebUI")
    print(f"  http://localhost:{PORT}/webui.html")
    print(f"  API proxy -> {API_BASE}")
    print(f"=" * 50)
    server = http.server.HTTPServer(("0.0.0.0", PORT), ProxyHandler)
    try:
        import webbrowser
        webbrowser.open(f"http://localhost:{PORT}/webui.html")
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server] Stopped.")
