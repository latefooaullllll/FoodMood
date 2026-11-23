
import sqlite3
from pathlib import Path

# Lokasi database
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "foodmood.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabel resep
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT,
            area TEXT,
            instructions TEXT,
            image_url TEXT,
            source_url TEXT
        )
    """)

    # Tabel bahan makanan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Hubungan resep dan bahan makanan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            ingredient_id INTEGER NOT NULL,
            measure TEXT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
            UNIQUE (recipe_id, ingredient_id)
        )
    """)

    # Tag preferensi makanan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            tag TEXT NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id),
            UNIQUE (recipe_id, tag)
        )
    """)

    # Riwayat rekomendasi resep untuk fitur Anti-Bosan Menu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database FoodMood berhasil dibuat!")
    print(
        "Tabel recipes, ingredients, recipe_ingredients, "
        "recipe_tags, dan recommendation_history siap digunakan."
    )


if __name__ == "__main__":
    init_db()
