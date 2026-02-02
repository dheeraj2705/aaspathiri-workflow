from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def run(host: str = "127.0.0.1", port: int = 5173) -> None:
    web_root = Path(__file__).parent
    handler = SimpleHTTPRequestHandler
    server = ThreadingHTTPServer((host, port), handler)

    print(f"Serving {web_root} at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
