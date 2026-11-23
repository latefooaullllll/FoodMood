
from database.db import get_connection


# Aturan pengelompokan mood berdasarkan nama resep
NAME_RULES = {
    "berkuah": [
        "soup", "stew", "broth", "chowder",
        "ramen", "pho", "laksa", "bisque",
        "hotpot"
    ],
    "ringan": [
        "salad", "bruschetta", "salsa",
        "dip", "gazpacho", "ceviche"
    ],
    "manis": [
        "cake", "pudding", "cookie", "brownie",
        "fudge", "tart", "ice cream", "mousse",
        "sweet"
    ]
}


# Aturan pengelompokan berdasarkan bahan
INGREDIENT_RULES = {
    "pedas": [
        "chili", "chilli", "jalapeno",
        "cayenne", "sriracha", "tabasco",
        "hot sauce", "harissa", "gochujang"
    ]
}


def contains_keyword(text, keywords):
    """Memeriksa apakah teks mengandung salah satu kata kunci."""
    text = (text or "").lower()

    return any(keyword in text for keyword in keywords)


def determine_moods(recipe):
    """Menentukan tag mood berdasarkan karakteristik resep."""

    moods = set()

    name = recipe["name"] or ""
    category = (recipe["category"] or "").lower()
    ingredients = recipe["ingredients"]

    # Mood manis
    if category == "dessert":
        moods.add("manis")
    elif contains_keyword(name, NAME_RULES["manis"]):
        moods.add("manis")

    # Mood pedas
    for ingredient in ingredients:
        if contains_keyword(
            ingredient,
            INGREDIENT_RULES["pedas"]
        ):
            moods.add("pedas")
            break

    # Mood berkuah
    if contains_keyword(name, NAME_RULES["berkuah"]):
        moods.add("berkuah")

    # Mood ringan
    if category == "starter":
        moods.add("ringan")
    elif contains_keyword(name, NAME_RULES["ringan"]):
        moods.add("ringan")

    return moods


def generate_mood_tags():
    """Membaca resep dan menyimpan tag mood ke database."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.name,
            r.category,
            i.name AS ingredient_name
        FROM recipes r
        LEFT JOIN recipe_ingredients ri
            ON r.id = ri.recipe_id
        LEFT JOIN ingredients i
            ON ri.ingredient_id = i.id
        ORDER BY r.id
    """)

    rows = cursor.fetchall()

    recipes = {}

    # Mengelompokkan bahan berdasarkan resep
    for row in rows:
        recipe_id = row["id"]

        if recipe_id not in recipes:
            recipes[recipe_id] = {
                "id": recipe_id,
                "name": row["name"],
                "category": row["category"],
                "ingredients": []
            }

        if row["ingredient_name"]:
            recipes[recipe_id]["ingredients"].append(
                row["ingredient_name"]
            )

    mood_counts = {
        "pedas": 0,
        "manis": 0,
        "berkuah": 0,
        "ringan": 0
    }

    tagged_recipes = 0

    # Menentukan dan menyimpan mood setiap resep
    for recipe in recipes.values():
        moods = determine_moods(recipe)

        if moods:
            tagged_recipes += 1

        for mood in moods:
            cursor.execute("""
                INSERT OR IGNORE INTO recipe_tags
                (recipe_id, tag)
                VALUES (?, ?)
            """, (recipe["id"], mood))

            mood_counts[mood] += 1

    conn.commit()
    conn.close()

    print("=== PROSES PEMBUATAN MOOD TAG FOODMOOD ===")
    print(f"Total resep diperiksa : {len(recipes)}")
    print(f"Resep memiliki tag    : {tagged_recipes}")

    print("\n=== JUMLAH RESEP PER MOOD ===")

    for mood, total in mood_counts.items():
        print(f"{mood.capitalize():10}: {total}")

    print("\nMood tag berhasil disimpan ke database!")


if __name__ == "__main__":
    generate_mood_tags()
