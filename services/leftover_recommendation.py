
from database.db import get_connection

from services.recommendation import (
    normalize_ingredient,
    translate_ingredient,
    translate_category
)


def recommend_by_leftovers(leftover_ingredients):
    """
    Merekomendasikan resep berdasarkan jumlah
    bahan sisa yang dapat dimanfaatkan.
    """

    if not leftover_ingredients:
        return []

    available_ingredients = {
        normalize_ingredient(item)
        for item in leftover_ingredients
        if item and item.strip()
    }

    if not available_ingredients:
        return []

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                r.id,
                r.meal_id,
                r.name,
                r.category,
                r.area,
                r.image_url,
                i.name AS ingredient_name
            FROM recipes r
            JOIN recipe_ingredients ri
                ON r.id = ri.recipe_id
            JOIN ingredients i
                ON ri.ingredient_id = i.id
            ORDER BY r.name
        """)

        rows = cursor.fetchall()

        recipes = {}

        # Mengelompokkan bahan berdasarkan resep
        for row in rows:
            recipe_id = row["id"]

            if recipe_id not in recipes:
                recipes[recipe_id] = {
                    "id": recipe_id,
                    "meal_id": row["meal_id"],
                    "name": row["name"],
                    "category": translate_category(row["category"]),
                    "area": row["area"],
                    "image_url": row["image_url"],
                    "ingredients": set()
                }

            recipes[recipe_id]["ingredients"].add(
                normalize_ingredient(row["ingredient_name"])
            )

        recommendations = []

        # Menghitung bahan sisa yang dapat digunakan
        for recipe in recipes.values():
            recipe_ingredients = recipe["ingredients"]

            used_leftovers = (
                recipe_ingredients & available_ingredients
            )

            used_count = len(used_leftovers)
            total_leftovers = len(available_ingredients)

            if used_count == 0:
                continue

            utilization_percentage = (
                used_count / total_leftovers
            ) * 100

            match_percentage = (
                used_count / len(recipe_ingredients)
            ) * 100

            recommendations.append({
                "id": recipe["id"],
                "meal_id": recipe["meal_id"],
                "name": recipe["name"],
                "category": recipe["category"],
                "area": recipe["area"],
                "image_url": recipe["image_url"],
                "used_count": used_count,
                "total_leftovers": total_leftovers,
                "utilization_percentage": round(
                    utilization_percentage, 2
                ),
                "match_percentage": round(match_percentage, 2),
                "used_ingredients": sorted([
                    translate_ingredient(item)
                    for item in used_leftovers
                ]),
                "unused_leftovers": sorted([
                    translate_ingredient(item)
                    for item in available_ingredients - recipe_ingredients
                ]),
                "missing_ingredients": sorted([
                    translate_ingredient(item)
                    for item in recipe_ingredients - available_ingredients
                ])
            })

        # Prioritas utama: jumlah bahan sisa yang digunakan
        recommendations.sort(
            key=lambda item: (
                item["used_count"],
                item["utilization_percentage"],
                item["match_percentage"]
            ),
            reverse=True
        )

        return recommendations

    finally:
        conn.close()


if __name__ == "__main__":
    print("=== FOODMOOD: REKOMENDASI BAHAN SISA ===")

    input_bahan = input(
        "\nMasukkan bahan makanan yang tersedia "
        "(pisahkan dengan koma): "
    )

    bahan_sisa = [
        bahan.strip()
        for bahan in input_bahan.split(",")
        if bahan.strip()
    ]

    hasil = recommend_by_leftovers(bahan_sisa)

    print(f"\nBahan tersisa: {', '.join(bahan_sisa)}")
    print(f"Total resep ditemukan: {len(hasil)}")

    if not hasil:
        print("\nBelum ditemukan resep yang sesuai.")

    for index, recipe in enumerate(hasil[:10], start=1):
        print(f"\n{index}. {recipe['name']}")
        print(f"Kategori: {recipe['category']}")

        print(
            f"Bahan sisa terpakai: "
            f"{recipe['used_count']} dari "
            f"{recipe['total_leftovers']}"
        )

        print(
            f"Persentase pemanfaatan bahan sisa: "
            f"{recipe['utilization_percentage']}%"
        )

        print(
            f"Kecocokan bahan resep: "
            f"{recipe['match_percentage']}%"
        )

        print("Bahan sisa yang digunakan:")
        for bahan in recipe["used_ingredients"]:
            print(f"- {bahan}")

        print("Bahan sisa yang belum digunakan:")
        for bahan in recipe["unused_leftovers"]:
            print(f"- {bahan}")

        print("Bahan resep yang masih dibutuhkan:")
        for bahan in recipe["missing_ingredients"]:
            print(f"- {bahan}")
