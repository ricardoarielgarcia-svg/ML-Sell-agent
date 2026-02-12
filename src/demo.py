"""Demo ejecutable para ver el sistema funcionando en local.

Uso:
    python3 -m src.demo
"""

from __future__ import annotations

from src.ml_listing_builder import ListingInput, build_item_payload
from src.pricing import PricingInput, calcular_precio_mercadolibre


def main() -> None:
    pricing_input = PricingInput(
        costo_producto=10000,
        costo_envio=1200,
        costo_empaque=300,
        costo_fijo_operativo=500,
        porcentaje_comision_ml=0.17,
        porcentaje_impuestos=0.03,
        margen_deseado_sobre_costo=0.35,
    )

    pricing_result = calcular_precio_mercadolibre(pricing_input)

    listing_input = ListingInput(
        title="Auriculares Bluetooth Inalámbricos",
        category_id="MLA3697",
        available_quantity=10,
        buying_mode="buy_it_now",
        condition="new",
        listing_type_id="gold_special",
        description_plain=(
            "Auriculares bluetooth con estuche de carga, autonomía de 6 horas "
            "y conexión estable."
        ),
    )

    payload = build_item_payload(
        data=listing_input,
        price=pricing_result.precio_venta_recomendado,
    )

    print("=== RESULTADO PRICING ===")
    print(pricing_result)
    print("\n=== PAYLOAD LISTO PARA API DE MERCADO LIBRE ===")
    print(payload)


if __name__ == "__main__":
    main()
