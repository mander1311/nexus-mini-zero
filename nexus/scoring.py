def normalize_ratio(value, lower, upper):
    if upper == lower:
        return 0.0
    return max(0.0, min(1.0, (value - lower) / (upper - lower)))


def calculate_balanced(product):
    price = float(product.get("price") or 0)
    commission_rate = float(product.get("commission_rate") or 0)
    commission_estimate = float(product.get("commission_estimate") or (price * (commission_rate / 100)))
    search_interest = float(product.get("search_interest") or 0)
    rating = float(product.get("rating") or 0)
    review_count = float(product.get("review_count") or 0)
    competition = float(product.get("competition") or 0)

    commission_score = min(100.0, max(0.0, (commission_estimate / max(price, 1.0)) * 100.0 * 1.5))
    demand_score = min(100.0, max(0.0, search_interest / 100.0 * 100.0))
    rating_score = min(100.0, max(0.0, (rating / 5.0) * 100.0))
    competition_score = 100.0 - min(100.0, competition)

    if review_count > 0:
        review_weight = min(100.0, (review_count / 1000.0) * 100.0)
        rating_score = (rating_score * 0.8) + (min(100.0, review_weight) * 0.2)

    balanced = (
        commission_score * 0.35
        + demand_score * 0.30
        + rating_score * 0.20
        + competition_score * 0.15
    )

    explanation = {
        "commission": round(commission_score, 2),
        "demand": round(demand_score, 2),
        "rating": round(rating_score, 2),
        "competition": round(competition_score, 2),
        "weights": {
            "commission": 35,
            "demand": 30,
            "rating": 20,
            "competition": 15,
        },
    }

    return {
        "score": round(balanced, 2),
        "recommendation": "Oportunidade moderada" if balanced >= 60 else "Aguardando revisão",
        "factors": explanation,
        "estimated_commission": round(commission_estimate, 2),
        "estimated_market_demand": round(search_interest, 2),
        "marketplace": product.get("marketplace"),
        "product_name": product.get("name"),
    }
