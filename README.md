# ML Sell Agent (base inicial)

Este repositorio contiene una base para construir un sistema que:

1. Recibe información de productos.
2. Calcula un precio de publicación orientado a una **ganancia objetivo** sobre costo.
3. Prepara un payload para publicar en Mercado Libre usando la API oficial.
4. Deja trazabilidad de costos y supuestos de negocio.

> ⚠️ Este proyecto no expone ni almacena tokens reales por defecto. Usa variables de entorno para credenciales.

## ¿Cómo verlo funcionando ahora mismo?

1. Ejecutá el demo integrado:

```bash
python3 -m src.demo
```

2. Vas a ver dos salidas:
   - `PricingResult(...)` con costos, precio recomendado y ganancia estimada.
   - Un diccionario `payload` con el cuerpo base para publicar en Mercado Libre.

3. Validá que los tests pasen:

```bash
python3 -m pytest -q
```


## API para probar (sin dependencias externas)

Levantá el servidor local:

```bash
python3 -m src.api
```

Probar salud:

```bash
curl -s http://localhost:8000/health
```

Simular publicación completa (pricing + payload):

```bash
curl -s -X POST http://localhost:8000/simular-publicacion   -H "Content-Type: application/json"   -d '{
    "pricing": {
      "costo_producto": 10000,
      "costo_envio": 1200,
      "costo_empaque": 300,
      "costo_fijo_operativo": 500,
      "porcentaje_comision_ml": 0.17,
      "porcentaje_impuestos": 0.03,
      "margen_deseado_sobre_costo": 0.35
    },
    "listing": {
      "title": "Auriculares Bluetooth Inalámbricos",
      "category_id": "MLA3697",
      "available_quantity": 10,
      "buying_mode": "buy_it_now",
      "condition": "new",
      "listing_type_id": "gold_special",
      "description_plain": "Auriculares bluetooth con estuche de carga",
      "currency_id": "ARS"
    }
  }'
```

Endpoints disponibles:
- `GET /health`
- `POST /pricing`
- `POST /listing-payload`
- `POST /simular-publicacion`

## Arquitectura sugerida

- **Ingesta de producto**: formulario o CSV/Excel.
- **Motor de pricing** (`src/pricing.py`): calcula precio de venta con costos asociados.
- **Publicador ML** (`src/ml_listing_builder.py`): genera payload base para endpoint `/items`.
- **Orquestación**: un servicio API (FastAPI/Django) y una cola para publicaciones masivas.
- **Optimización**:
  - testing de títulos/imágenes,
  - ajuste de presupuesto de campañas,
  - monitoreo de margen real por publicación.

## Fórmula de pricing incluida

Dado:

- `costo_producto`
- `costo_envio`
- `costo_empaque`
- `costo_fijo`
- `% comisión ML`
- `% impuesto`
- `% margen deseado sobre costo`

Se calcula:

- `costo_total = suma de costos fijos y variables`
- `ganancia_objetivo = costo_total * margen_deseado`
- `precio_venta = (costo_total + ganancia_objetivo) / (1 - comision - impuesto)`

Incluye validación para evitar escenarios inválidos (`comision + impuesto >= 1`).

## Próximos pasos recomendados

1. Crear autenticación OAuth2 con Mercado Libre.
2. Implementar endpoint para crear publicaciones reales.
3. Persistir costos y resultados en una base de datos.
4. Agregar simulador de escenarios (sensibilidad de margen/comisión).
5. Incorporar reglas por categoría (comisión y logística varían).
