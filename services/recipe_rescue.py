
from database.db import get_connection
from services.recommendation import translate_ingredient, translate_category


# Daftar alternatif bahan makanan
INGREDIENT_ALTERNATIVES = {
    "butter": ["margarine"],
    "milk": ["evaporated milk", "soy milk"],
    "double cream": ["heavy cream", "cooking cream"],
    "olive oil": ["sunflower oil", "vegetable oil"],
    "sunflower oil": ["vegetable oil"],
    "vegetable oil": ["sunflower oil"],
    "paprika": ["smoked paprika", "chili powder"],
    "green olives": ["black olives"],
    "onion": ["shallots"],
    "garlic": ["garlic powder"],
    "lemon": ["lime"],
    "lime": ["lemon"],
    "plain flour": ["all-purpose flour"],
    "brown sugar": ["white sugar"],
    "white sugar": ["brown sugar"],
    "chicken stock": ["chicken stock cube"],
    "chicken stock cube": ["chicken stock"],
    "tomato puree": ["tomato paste"],
    "tomato paste": ["tomato puree"],
    "sour cream": ["plain yogurt"],
    "fresh cream": ["cooking cream"],
    "parmesan cheese": ["cheddar cheese"],
    "spring onions": ["chives"]
}


# Menyamakan nama bahan bahasa Indonesia dan Inggris
INGREDIENT_ALIASES = {
    "onions": "onion",
    "tomatoes": "tomato",
    "tomatos": "tomato",
    "potatoes": "potato",
    "carrots": "carrot",
    "eggs": "egg",

    "ayam": "chicken",
    "daging ayam": "chicken",
    "kentang": "potato",
    "bawang bombai": "onion",
    "bawang bombay": "onion",
    "bawang merah": "shallot",
    "bawang putih": "garlic",
    "telur": "egg",
    "telur ayam": "egg",
    "tomat": "tomato",
    "wortel": "carrot",
    "susu": "milk",
    "mentega": "butter",
    "margarin": "margarine",
    "minyak zaitun": "olive oil",
    "minyak sayur": "vegetable oil",
    "minyak bunga matahari": "sunflower oil",
    "tepung": "plain flour",
    "tepung terigu": "plain flour",
    "gula": "white sugar",
    "gula merah": "brown sugar",
    "jeruk nipis": "lime",
    "zaitun hijau": "green olives",
    "zaitun hitam": "black olives",
    "keju parmesan": "parmesan cheese",
    "daun bawang": "spring onions"
}


# Terjemahan tambahan untuk bahan yang belum ada di kamus utama
TERJEMAHAN_BAHAN = {
    "chicken": "Ayam",
    "garlic": "Bawang putih",
    "onion": "Bawang bombai",
    "potato": "Kentang",
    "green olives": "Zaitun hijau",
    "black olives": "Zaitun hitam",
    "olive oil": "Minyak zaitun",
    "sunflower oil": "Minyak bunga matahari",
    "vegetable oil": "Minyak sayur",
    "paprika": "Paprika",
    "smoked paprika": "Paprika asap",
    "chili powder": "Bubuk cabai",
    "roasted pepper": "Paprika panggang",
    "tinned tomatos": "Tomat kalengan",
    "tinned tomatoes": "Tomat kalengan",
    "tomato": "Tomat",
    "shallots": "Bawang merah",
    "garlic powder": "Bubuk bawang putih",
    "plain flour": "Tepung terigu",
    "all-purpose flour": "Tepung serbaguna",
    "margarine": "Margarin",
    "butter": "Mentega",
    "milk": "Susu",
    "lemon": "Lemon",
    "lime": "Jeruk nipis",
    "egg": "Telur"
}


def normalize_ingredient(name):
    """Menyeragamkan nama bahan makanan."""

    normalized = name.strip().lower()

    return INGREDIENT_ALIASES.get(
        normalized,
        normalized
    )


def translate_food_name(name):
    """Mengubah nama bahan menjadi bahasa Indonesia."""

    normalized = name.strip().lower()

    if normalized in TERJEMAHAN_BAHAN:
        return TERJEMAHAN_BAHAN[normalized]

    translated = translate_ingredient(name)

    if translated and translated.lower() != normalized:
        return translated

    return name


def rescue_recipe(recipe_name, available_ingredients):
    """
    Memeriksa bahan resep dan memberikan alternatif
    untuk bahan yang belum tersedia.
    """

    if not recipe_name or not recipe_name.strip():
        return None

    available = {
        normalize_ingredient(item)
        for item in available_ingredients
        if item and item.strip()
    }

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, meal_id, name, category
            FROM recipes
            WHERE LOWER(name) = LOWER(?)
            LIMIT 1
        """, (recipe_name.strip(),))

        recipe = cursor.fetchone()

        if not recipe:
            return None

        cursor.execute("""
            SELECT i.name
            FROM recipe_ingredients ri
            JOIN ingredients i
                ON ri.ingredient_id = i.id
            WHERE ri.recipe_id = ?
            ORDER BY i.name
        """, (recipe["id"],))

        ingredient_rows = cursor.fetchall()

    finally:
        conn.close()

    recipe_ingredients = [
        row["name"] for row in ingredient_rows
    ]

    matched = []
    missing = []

    for ingredient in recipe_ingredients:
        normalized = normalize_ingredient(ingredient)

        if normalized in available:
            matched.append(translate_food_name(ingredient))
        else:
            missing.append(ingredient)

    rescue_results = []

    for ingredient in missing:
        key = normalize_ingredient(ingredient)

        alternatives = INGREDIENT_ALTERNATIVES.get(
            key, []
        )

        rescue_results.append({
            "ingredient": translate_food_name(ingredient),
            "alternatives": [
                translate_food_name(item)
                for item in alternatives
            ]
        })

    return {
        "meal_id": recipe["meal_id"],
        "name": recipe["name"],
        "category": translate_category(recipe["category"]),
        "total_ingredients": len(recipe_ingredients),
        "matched_ingredients": matched,
        "missing_ingredients": [
            translate_food_name(item)
            for item in missing
        ],
        "rescue_results": rescue_results
    }


if __name__ == "__main__":

    print("=== FOODMOOD: PENYELAMAT RESEP ===")

    recipe_name = input("\nMasukkan nama resep: ")

    ingredients_input = input(
        "Masukkan bahan yang tersedia (pisahkan dengan koma): "
    )

    available_ingredients = [
        item.strip()
        for item in ingredients_input.split(",")
        if item.strip()
    ]

    result = rescue_recipe(
        recipe_name,
        available_ingredients
    )

    if not result:
        print("\nResep tidak ditemukan.")

    else:
        print(f"\nResep: {result['name']}")
        print(f"Kategori: {result['category']}")

        print(
            f"\nTotal bahan resep: "
            f"{result['total_ingredients']}"
        )

        print(
            f"Bahan tersedia: "
            f"{len(result['matched_ingredients'])}"
        )

        print(
            f"Bahan belum tersedia: "
            f"{len(result['missing_ingredients'])}"
        )

        print("\n=== BAHAN YANG TERSEDIA ===")

        for ingredient in result["matched_ingredients"]:
            print(f"- {ingredient}")

        print("\n=== BAHAN YANG BELUM TERSEDIA ===")

        for item in result["rescue_results"]:
            print(f"\n- {item['ingredient']}")

            if item["alternatives"]:
                print(
                    "  Alternatif: "
                    + ", ".join(item["alternatives"])
                )
            else:
                print("  Alternatif belum tersedia.")

        print("\nProses Penyelamat Resep selesai!")
