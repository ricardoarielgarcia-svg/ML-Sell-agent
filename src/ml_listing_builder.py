"""Utilities para construir payload de publicación en Mercado Libre.

Este módulo no realiza requests todavía; solo prepara estructura compatible
con el endpoint de creación de ítems.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ListingInput:
    title: str
    category_id: str
    available_quantity: int
    buying_mode: str
    condition: str
    listing_type_id: str
    description_plain: str
    currency_id: str = "ARS"


def build_item_payload(data: ListingInput, price: float) -> dict[str, Any]:
    if price <= 0:
        raise ValueError("price debe ser mayor que cero")

    if not data.title.strip():
        raise ValueError("title no puede estar vacío")

    return {
        "title": data.title,
        "category_id": data.category_id,
        "price": round(price, 2),
        "currency_id": data.currency_id,
        "available_quantity": data.available_quantity,
        "buying_mode": data.buying_mode,
        "condition": data.condition,
        "listing_type_id": data.listing_type_id,
        "sale_terms": [],
        "pictures": [],
        "attributes": [],
        "description": {"plain_text": data.description_plain},
    }
