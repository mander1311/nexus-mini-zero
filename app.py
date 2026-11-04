from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import os

from nexus.db import init_db, get_products, create_product, update_product, delete_product, get_product_by_id
from nexus.scoring import calculate_balanced
from nexus.commission import calculate_projection
from nexus.copywriter import generate_copy

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")


@app.get("/api/health")
def health_check():
    return jsonify({"status": "ok", "app": "NEXUS MINI ZERO", "version": "V1"})


@app.get("/")
def index():
    return send_from_directory(str(FRONTEND_DIR), "index.html")


@app.get("/api/dashboard")
def dashboard():
    products = get_products()
    selected = sum(1 for p in products if p.get("selected"))
    total_products = len(products)
    potential = sum(float(p.get("commission_estimate", 0.0) or 0.0) for p in products)
    contents = 0
    results = 0
    return jsonify({
        "total_products": total_products,
        "opportunities": total_products,
        "selected_products": selected,
        "potential_commission": round(potential, 2),
        "contents_generated": contents,
        "results_registered": results,
    })


@app.get("/api/products")
def list_products():
    return jsonify(get_products())


@app.get("/api/products/<int:product_id>/analysis")
def product_analysis(product_id: int):
    product = get_product_by_id(product_id)
    if product is None:
        return jsonify({"error": "Produto não encontrado."}), 404
    analysis = calculate_balanced(product)
    return jsonify(analysis)


@app.post("/api/products")
def create_product_route():
    payload = request.get_json(silent=True) or {}
    product = create_product(payload)
    return jsonify(product), 201


@app.put("/api/products/<int:product_id>")
def update_product_route(product_id: int):
    payload = request.get_json(silent=True) or {}
    product = update_product(product_id, payload)
    if product is None:
        return jsonify({"error": "Produto não encontrado."}), 404
    return jsonify(product)


@app.delete("/api/products/<int:product_id>")
def delete_product_route(product_id: int):
    deleted = delete_product(product_id)
    if not deleted:
        return jsonify({"error": "Produto não encontrado."}), 404
    return jsonify({"status": "ok", "deleted_id": product_id})


@app.post("/api/calculator")
def calculator():
    payload = request.get_json(silent=True) or {}
    price = float(payload.get("price", 0) or 0)
    commission_rate = float(payload.get("commission_rate", 0) or 0)
    sales = float(payload.get("sales", 1) or 1)
    conversion_rate = float(payload.get("conversion_rate", 0) or 0)
    projection = calculate_projection(price, commission_rate, sales=sales, conversion_rate=conversion_rate)
    return jsonify(projection)


@app.post("/api/copywriter")
def generate_content_route():
    payload = request.get_json(silent=True) or {}
    if not payload.get("name"):
        return jsonify({"error": "Informe o nome do produto."}), 400
    content = generate_copy(payload)
    return jsonify(content)


init_db()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
