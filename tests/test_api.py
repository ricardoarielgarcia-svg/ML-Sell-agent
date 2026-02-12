from src.api import route_request


def test_health_endpoint():
    status, payload = route_request("GET", "/health", None)
    assert status == 200
    assert payload["status"] == "ok"


def test_simular_publicacion_endpoint():
    body = {
        "pricing": {
            "costo_producto": 100,
            "costo_envio": 10,
            "costo_empaque": 5,
            "costo_fijo_operativo": 5,
            "porcentaje_comision_ml": 0.1,
            "porcentaje_impuestos": 0.05,
            "margen_deseado_sobre_costo": 0.25,
        },
        "listing": {
            "title": "Producto Demo",
            "category_id": "MLA3697",
            "available_quantity": 3,
            "buying_mode": "buy_it_now",
            "condition": "new",
            "listing_type_id": "gold_special",
            "description_plain": "Descripción demo",
            "currency_id": "ARS",
        },
    }

    status, payload = route_request("POST", "/simular-publicacion", body)

    assert status == 200
    assert payload["pricing"]["precio_venta_recomendado"] == 176.47
    assert payload["listing_payload"]["price"] == 176.47


def test_pricing_validation_error():
    status, payload = route_request("POST", "/pricing", {"costo_producto": 0})
    assert status == 400
    assert "error" in payload
