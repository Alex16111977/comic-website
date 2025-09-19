"""Simple development server with review queue mutation endpoint."""
from __future__ import annotations

import argparse
import json
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from review_queue import ReviewQueueStore


class ReviewQueueRequestHandler(SimpleHTTPRequestHandler):
    """Serve generated assets and handle review queue mutations."""

    queue_store = ReviewQueueStore(config.DATA_DIR / "review_queue.json")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(config.OUTPUT_DIR), **kwargs)

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        """Handle POST requests for review queue actions."""
        if self.path.rstrip("/") == "/api/review-queue/remove":
            self.handle_remove_request()
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Unknown API endpoint")

    def handle_remove_request(self) -> None:
        """Process removal requests from the review queue."""
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        raw_body = b""
        if content_length > 0:
            raw_body = self.rfile.read(content_length)

        payload = self._parse_payload(raw_body)
        if payload is None:
            self._send_json({"success": False, "error": "Invalid JSON payload"}, HTTPStatus.BAD_REQUEST)
            return

        word_id, character_id, phase_id = self._extract_ids(payload)
        removed, remaining = self.queue_store.remove(word_id, character_id, phase_id)

        self._send_json(
            {
                "success": True,
                "removed": removed,
                "remaining": remaining,
            }
        )

    @staticmethod
    def _parse_payload(raw_body: bytes):
        if not raw_body:
            return {}

        try:
            return json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None

    @staticmethod
    def _extract_ids(payload) -> Tuple[str, str, str]:
        if not isinstance(payload, dict):
            return "", "", ""

        return (
            str(payload.get("wordId") or payload.get("word_id") or "").strip(),
            str(payload.get("characterId") or payload.get("character_id") or "").strip(),
            str(payload.get("phaseId") or payload.get("phase_id") or "").strip(),
        )

    def _send_json(self, payload, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args) -> None:  # noqa: A003 - signature required
        message = "%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args)
        print(message, end="")


def parse_args():
    parser = argparse.ArgumentParser(description="Serve generated site with review queue API")
    parser.add_argument("--host", default="127.0.0.1", help="Hostname to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind (default: 8000)")
    return parser.parse_args()


def run_server(host: str, port: int) -> None:
    output_dir = Path(config.OUTPUT_DIR)
    if not output_dir.exists():
        raise SystemExit(
            f"Output directory '{output_dir}' not found. Run 'python main.py' before starting the server."
        )

    server_address = (host, port)
    handler = ReviewQueueRequestHandler

    print(f"[INFO] Serving {output_dir} at http://{host}:{port}")
    print("[INFO] Review queue API available at /api/review-queue/remove")

    with ThreadingHTTPServer(server_address, handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Server stopped by user")


def main() -> None:
    args = parse_args()
    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
