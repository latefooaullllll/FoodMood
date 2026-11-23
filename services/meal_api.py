
import requests

from database.db import get_connection

BASE_URL = "https://www.themealdb.com/api/json/v1/1"


def get_categories():
    """Mengambil seluruh kategori resep dari TheMealDB."""
    url = f"{BASE_URL}/list.php?c=list"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()
    return data.get("meals") or []


def get_meals_by_category(category):
    """Mengambil daftar resep berdasarkan kategori."""
    url = f"{BASE_URL}/filter.php?c={category}"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()
    return data.get("meals") or []


def get_meal_detail(meal_id):
    """Mengambil detail satu resep."""
    url = f"{BASE_URL}/lookup.php?i={meal_id}"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()
    meals = data.get("meals")

    return meals[0] if meals else None


def save_meal(meal):
    """Menyimpan resep dan bahan ke SQLite."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO recipes
        (meal_id, name, category, area, instructions, image_url, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        meal.get("idMeal"),
        meal.get("strMeal"),
        meal.get("strCategory"),
        meal.get("strArea"),
        meal.get("strInstructions"),
        meal.get("strMealThumb"),
        meal.get("strSource")
    ))

    cursor.execute(
        "SELECT id FROM recipes WHERE meal_id = ?",
        (meal.get("idMeal"),)
    )
    recipe = cursor.fetchone()

    if recipe:
        recipe_id = recipe["id"]

        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")

            if ingredient and ingredient.strip():
                ingredient = ingredient.strip()

                cursor.execute("""
                    INSERT OR IGNORE INTO ingredients (name)
                    VALUES (?)
                """, (ingredient,))

                cursor.execute(
                    "SELECT id FROM ingredients WHERE name = ?",
                    (ingredient,)
                )
                ingredient_data = cursor.fetchone()

                cursor.execute("""
                    INSERT OR IGNORE INTO recipe_ingredients
                    (recipe_id, ingredient_id, measure)
                    VALUES (?, ?, ?)
                """, (
                    recipe_id,
                    ingredient_data["id"],
                    (measure or "").strip()
                ))

    conn.commit()
    conn.close()


def import_recipes(category):
    """Mengambil dan menyimpan resep dari satu kategori."""
    print(f"\nMengambil resep kategori: {category}")

    meals = get_meals_by_category(category)

    if not meals:
        print("Tidak ada resep yang ditemukan.")
        return 0

    total_processed = 0

    for item in meals:
        detail = get_meal_detail(item["idMeal"])

        if detail:
            save_meal(detail)
            total_processed += 1
            print(f"Berhasil memproses: {detail['strMeal']}")

    print(f"Total resep diproses dari {category}: {total_processed}")

    return total_processed


def import_all_categories():
    """Mengambil dan menyimpan resep dari seluruh kategori."""
    print("Mengambil seluruh kategori dari TheMealDB...")

    categories = get_categories()

    if not categories:
        print("Kategori tidak ditemukan.")
        return

    print(f"\nDitemukan {len(categories)} kategori resep.")

    total_processed = 0

    for category_data in categories:
        category = category_data["strCategory"]

        try:
            total_processed += import_recipes(category)

        except requests.RequestException as error:
            print(f"Gagal mengambil kategori {category}: {error}")

    print("\n===================================")
    print("PROSES IMPORT SELURUH KATEGORI SELESAI")
    print(f"Jumlah kategori : {len(categories)}")
    print(f"Total diproses  : {total_processed}")
    print("===================================")


if __name__ == "__main__":
    import_all_categories()
