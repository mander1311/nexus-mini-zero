import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from nexus import DB_PATH


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    _ensure_parent(DB_PATH)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    _ensure_parent(DB_PATH)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                marketplace TEXT,
                category TEXT,
                price REAL DEFAULT 0,
                commission_rate REAL DEFAULT 0,
                commission_estimate REAL DEFAULT 0,
                affiliate_link TEXT,
                product_link TEXT,
                rating REAL DEFAULT 0,
                review_count INTEGER DEFAULT 0,
                search_interest INTEGER DEFAULT 0,
                competition INTEGER DEFAULT 0,
                notes TEXT,
                favorite INTEGER DEFAULT 0,
                selected INTEGER DEFAULT 0,
                source TEXT DEFAULT 'manual',
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS generated_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                title TEXT,
                description TEXT,
                caption TEXT,
                cta TEXT,
                short_post TEXT,
                video_script TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tracking_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                clicks INTEGER DEFAULT 0,
                sales INTEGER DEFAULT 0,
                commission REAL DEFAULT 0,
                conversion_rate REAL DEFAULT 0,
                source TEXT,
                recorded_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def normalize_product(row: Optional[sqlite3.Row]) -> Optional[Dict[str, Any]]:
    if row is None:
        return None
    product = dict(row)
    product["favorite"] = bool(product.get("favorite", 0))
    product["selected"] = bool(product.get("selected", 0))
    return product


def get_products() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM products ORDER BY updated_at DESC, id DESC"
        ).fetchall()
        return [normalize_product(row) for row in rows]


def get_product_by_id(product_id: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        return normalize_product(row)


def create_product(payload: Dict[str, Any]) -> Dict[str, Any]:
    name = (payload.get("name") or "Produto sem nome").strip()
    marketplace = (payload.get("marketplace") or "Manual").strip()
    category = (payload.get("category") or "Geral").strip()
    price = float(payload.get("price") or 0)
    commission_rate = float(payload.get("commission_rate") or 0)
    commission_estimate = price * (commission_rate / 100)
    product = {
        "name": name,
        "marketplace": marketplace,
        "category": category,
        "price": price,
        "commission_rate": commission_rate,
        "commission_estimate": round(commission_estimate, 2),
        "affiliate_link": payload.get("affiliate_link") or "",
        "product_link": payload.get("product_link") or "",
        "rating": float(payload.get("rating") or 0),
        "review_count": int(payload.get("review_count") or 0),
        "search_interest": int(payload.get("search_interest") or 0),
        "competition": int(payload.get("competition") or 0),
        "notes": payload.get("notes") or "",
        "favorite": bool(payload.get("favorite") or False),
        "selected": bool(payload.get("selected") or False),
        "source": payload.get("source") or "manual",
    }
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO products (
                name, marketplace, category, price, commission_rate, commission_estimate,
                affiliate_link, product_link, rating, review_count, search_interest,
                competition, notes, favorite, selected, source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                product["name"],
                product["marketplace"],
                product["category"],
                product["price"],
                product["commission_rate"],
                product["commission_estimate"],
                product["affiliate_link"],
                product["product_link"],
                product["rating"],
                product["review_count"],
                product["search_interest"],
                product["competition"],
                product["notes"],
                int(product["favorite"]),
                int(product["selected"]),
                product["source"],
            ),
        )
        product["id"] = cursor.lastrowid
    return product


def update_product(product_id: int, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    current = get_product_by_id(product_id)
    if current is None:
        return None
    merged = {**current, **payload}
    price = float(merged.get("price") or 0)
    commission_rate = float(merged.get("commission_rate") or 0)
    merged["commission_estimate"] = round(price * (commission_rate / 100), 2)
    merged["favorite"] = bool(merged.get("favorite") or False)
    merged["selected"] = bool(merged.get("selected") or False)
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE products SET
                name = ?, marketplace = ?, category = ?, price = ?, commission_rate = ?, commission_estimate = ?,
                affiliate_link = ?, product_link = ?, rating = ?, review_count = ?, search_interest = ?,
                competition = ?, notes = ?, favorite = ?, selected = ?, source = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                merged.get("name"),
                merged.get("marketplace"),
                merged.get("category"),
                merged.get("price"),
                merged.get("commission_rate"),
                merged.get("commission_estimate"),
                merged.get("affiliate_link"),
                merged.get("product_link"),
                merged.get("rating"),
                merged.get("review_count"),
                merged.get("search_interest"),
                merged.get("competition"),
                merged.get("notes"),
                int(merged.get("favorite") or False),
                int(merged.get("selected") or False),
                merged.get("source"),
                product_id,
            ),
        )
    return get_product_by_id(product_id)


def delete_product(product_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    return cursor.rowcount > 0
