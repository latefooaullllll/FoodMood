
from database.db import get_connection


def check_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Menghitung jumlah resep
    cursor.execute("SELECT COUNT(*) AS total FROM recipes")
    total_recipes = cursor.fetchone()["total"]

    # Menghitung jumlah bahan
    cursor.execute("SELECT COUNT(*) AS total FROM ingredients")
    total_ingredients = cursor.fetchone()["total"]

    # Menghitung hubungan resep dan bahan
    cursor.execute("SELECT COUNT(*) AS total FROM recipe_ingredients")
    total_relations = cursor.fetchone()["total"]

    print("=== DATA DATABASE FOODMOOD ===")
    print(f"Total resep          : {total_recipes}")
    print(f"Total bahan makanan : {total_ingredients}")
    print(f"Total hubungan      : {total_relations}")

    # Menampilkan 10 resep pertama
    cursor.execute("""
        SELECT id, name, category, area
        FROM recipes
        ORDER BY name
        LIMIT 10
    """)

    print("\n=== CONTOH DATA RESEP ===")

    for recipe in cursor.fetchall():
        print(
            f"{recipe['id']}. {recipe['name']} "
            f"| {recipe['category']} "
            f"| {recipe['area']}"
        )

    conn.close()


if __name__ == "__main__":
    check_database()
