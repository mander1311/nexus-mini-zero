from __future__ import annotations


def estimate_commission(price: float, commission_rate: float) -> float:
    if price < 0:
        raise ValueError("Preço não pode ser negativo.")
    return round(price * (commission_rate / 100), 2)


def calculate_projection(price: float, commission_rate: float, sales: float = 1, conversion_rate: float = 0.0) -> dict:
    per_sale = estimate_commission(price, commission_rate)
    total_sales = max(0.0, sales)
    converted_sales = total_sales * max(0.0, min(1.0, conversion_rate))
    projected_commission = round(per_sale * converted_sales, 2)
    return {
        "price": round(price, 2),
        "commission_rate": round(commission_rate, 2),
        "per_sale": round(per_sale, 2),
        "sales": round(total_sales, 2),
        "conversion_rate": round(max(0.0, min(1.0, conversion_rate)), 4),
        "converted_sales": round(converted_sales, 2),
        "projected_commission": projected_commission,
        "note": "Projeção estimada; não representa garantia de venda.",
    }
