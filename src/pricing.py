"""Motor de pricing para Mercado Libre.

Permite calcular un precio objetivo en base a:
- costo total asociado,
- margen deseado (% sobre costo),
- comisión e impuestos (% sobre precio de venta).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PricingInput:
    costo_producto: float
    costo_envio: float = 0.0
    costo_empaque: float = 0.0
    costo_fijo_operativo: float = 0.0
    porcentaje_comision_ml: float = 0.0
    porcentaje_impuestos: float = 0.0
    margen_deseado_sobre_costo: float = 0.3


@dataclass(frozen=True)
class PricingResult:
    costo_total: float
    ganancia_objetivo: float
    precio_venta_recomendado: float
    comision_estimada: float
    impuestos_estimados: float
    ganancia_neta_estimada: float


def _validate_percent(value: float, field_name: str) -> None:
    if not 0 <= value < 1:
        raise ValueError(f"{field_name} debe estar entre 0 y 1 (exclusivo en 1).")


def calcular_precio_mercadolibre(params: PricingInput) -> PricingResult:
    """Calcula precio de venta recomendado para lograr el margen objetivo.

    La comisión e impuestos se interpretan como porcentajes sobre el precio final.
    """

    for val, field_name in [
        (params.porcentaje_comision_ml, "porcentaje_comision_ml"),
        (params.porcentaje_impuestos, "porcentaje_impuestos"),
        (params.margen_deseado_sobre_costo, "margen_deseado_sobre_costo"),
    ]:
        _validate_percent(val, field_name)

    costo_total = (
        params.costo_producto
        + params.costo_envio
        + params.costo_empaque
        + params.costo_fijo_operativo
    )

    if costo_total <= 0:
        raise ValueError("El costo total debe ser mayor que cero.")

    retenciones_sobre_venta = (
        params.porcentaje_comision_ml + params.porcentaje_impuestos
    )
    if retenciones_sobre_venta >= 1:
        raise ValueError(
            "La suma de comisión e impuestos debe ser menor a 1 para calcular precio."
        )

    ganancia_objetivo = costo_total * params.margen_deseado_sobre_costo
    precio_venta = (costo_total + ganancia_objetivo) / (1 - retenciones_sobre_venta)

    comision = precio_venta * params.porcentaje_comision_ml
    impuestos = precio_venta * params.porcentaje_impuestos
    ganancia_neta = precio_venta - costo_total - comision - impuestos

    return PricingResult(
        costo_total=round(costo_total, 2),
        ganancia_objetivo=round(ganancia_objetivo, 2),
        precio_venta_recomendado=round(precio_venta, 2),
        comision_estimada=round(comision, 2),
        impuestos_estimados=round(impuestos, 2),
        ganancia_neta_estimada=round(ganancia_neta, 2),
    )


if __name__ == "__main__":
    demo = PricingInput(
        costo_producto=10000,
        costo_envio=1200,
        costo_empaque=300,
        costo_fijo_operativo=500,
        porcentaje_comision_ml=0.17,
        porcentaje_impuestos=0.03,
        margen_deseado_sobre_costo=0.35,
    )
    result = calcular_precio_mercadolibre(demo)
    print(result)
