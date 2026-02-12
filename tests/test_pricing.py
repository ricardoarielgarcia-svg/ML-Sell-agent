from src.pricing import PricingInput, calcular_precio_mercadolibre


def test_calcular_precio_retorna_margen_objetivo_aproximado():
    params = PricingInput(
        costo_producto=100,
        costo_envio=10,
        costo_empaque=5,
        costo_fijo_operativo=5,
        porcentaje_comision_ml=0.1,
        porcentaje_impuestos=0.05,
        margen_deseado_sobre_costo=0.25,
    )

    result = calcular_precio_mercadolibre(params)

    assert result.costo_total == 120
    assert result.ganancia_objetivo == 30
    assert result.precio_venta_recomendado == 176.47
    assert result.ganancia_neta_estimada == 30.0
