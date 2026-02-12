"""API HTTP mínima (sin dependencias externas) para probar pricing y payload ML.

Ejecución:
    python3 -m src.api
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from src.ml_listing_builder import ListingInput, build_item_payload
from src.pricing import PricingInput, calcular_precio_mercadolibre


HOST = "0.0.0.0"
PORT = 8000


def _json_response(status: int, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    return status, payload


def route_request(method: str, path: str, body: dict[str, Any] | None) -> tuple[int, dict[str, Any]]:
    if method == "GET" and path == "/health":
        return _json_response(200, {"status": "ok"})

    if method == "POST" and path == "/pricing":
        if body is None:
            return _json_response(400, {"error": "Body JSON requerido"})
        try:
            payload = PricingInput(**body)
            result = calcular_precio_mercadolibre(payload)
        except (TypeError, ValueError) as exc:
            return _json_response(400, {"error": str(exc)})
        return _json_response(200, result.__dict__)

    if method == "POST" and path == "/listing-payload":
        if body is None:
            return _json_response(400, {"error": "Body JSON requerido"})

        try:
            price = float(body["price"])
            listing_data = ListingInput(**body["listing"])
            payload = build_item_payload(data=listing_data, price=price)
        except (KeyError, TypeError, ValueError) as exc:
            return _json_response(400, {"error": str(exc)})

        return _json_response(200, payload)

    if method == "POST" and path == "/simular-publicacion":
        if body is None:
            return _json_response(400, {"error": "Body JSON requerido"})

        try:
            pricing_input = PricingInput(**body["pricing"])
            pricing_result = calcular_precio_mercadolibre(pricing_input)
            listing_data = ListingInput(**body["listing"])
            payload = build_item_payload(
                data=listing_data,
                price=pricing_result.precio_venta_recomendado,
            )
        except (KeyError, TypeError, ValueError) as exc:
            return _json_response(400, {"error": str(exc)})

        return _json_response(
            200,
            {
                "pricing": pricing_result.__dict__,
                "listing_payload": payload,
            },
        )

    return _json_response(404, {"error": "Ruta no encontrada"})


class APIHandler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict[str, Any]) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json_body(self) -> dict[str, Any] | None:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length == 0:
            return None
        try:
            raw = self.rfile.read(content_length)
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def do_GET(self) -> None:  # noqa: N802
        status, payload = route_request("GET", self.path, None)
        self._send(status, payload)

    def do_POST(self) -> None:  # noqa: N802
        body = self._read_json_body()
        status, payload = route_request("POST", self.path, body)
        self._send(status, payload)

    def log_message(self, format: str, *args: Any) -> None:
        return


def run_server(host: str = HOST, port: int = PORT) -> None:
    server = ThreadingHTTPServer((host, port), APIHandler)
    print(f"API disponible en http://{host}:{port}")
    print("Endpoints: GET /health, POST /pricing, POST /listing-payload, POST /simular-publicacion")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
