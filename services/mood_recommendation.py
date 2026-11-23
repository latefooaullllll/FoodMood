
from database.db import get_connection


# Pilihan mood dalam Bahasa Indonesia
AVAILABLE_MOODS = [
    "pedas",
    "manis",
    "berkuah",
    "ringan"
]


# Terjemahan kategori resep
KATEGORI_INDONESIA = {
    "chicken": "Ayam",
    "beef": "Daging sapi",
    "seafood": "Hidangan laut",
    "side": "Hidangan pendamping",
    "vegetarian": "Vegetarian",
    "starter": "Hidangan pembuka",
    "dessert": "Hidangan penutup",
    "pork": "Daging babi",
    "vegan": "Nabati",
    "breakfast": "Sarapan",
    "lamb": "Daging domba",
    "goat": "Daging kambing",
    "pasta": "Pasta",
    "miscellaneous": "Lain-lain"
}


def translate_category(category):
    """Menerjemahkan kategori resep ke Bahasa Indonesia."""
    if not category:
        return "Tidak diketahui"

    return KATEGORI_INDONESIA.get(
        category.strip().lower(),
        category
    )


def recommend_by_mood(mood):
    """Mengambil rekomendasi resep berdasarkan mood pengguna."""

    mood = mood.strip().lower()

    if mood not in AVAILABLE_MOODS:
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
                rt.tag AS mood
            FROM recipes r
            JOIN recipe_tags rt
                ON r.id = rt.recipe_id
            WHERE LOWER(rt.tag) = ?
            ORDER BY r.name
        """, (mood,))

        rows = cursor.fetchall()

        recommendations = []

        for row in rows:
            recommendations.append({
                "id": row["id"],
                "meal_id": row["meal_id"],
                "name": row["name"],
                "category": translate_category(row["category"]),
                "area": row["area"],
                "image_url": row["image_url"],
                "mood": row["mood"].capitalize()
            })

        return recommendations

    finally:
        conn.close()


if __name__ == "__main__":
    print("=== FOODMOOD: REKOMENDASI BERDASARKAN MOOD ===")

    print("\nPilihan mood:")

    for index, mood in enumerate(AVAILABLE_MOODS, start=1):
        print(f"{index}. {mood.capitalize()}")

    pilihan = input("\nPilih mood (1-4): ").strip()

    mood_options = {
        "1": "pedas",
        "2": "manis",
        "3": "berkuah",
        "4": "ringan"
    }

    if pilihan not in mood_options:
        print("Pilihan tidak valid.")
    else:
        mood = mood_options[pilihan]
        hasil = recommend_by_mood(mood)

        print(f"\n=== REKOMENDASI MOOD: {mood.upper()} ===")
        print(f"Total resep ditemukan: {len(hasil)}")

        for index, recipe in enumerate(hasil[:10], start=1):
            print(f"\n{index}. {recipe['name']}")
            print(f"Kategori: {recipe['category']}")
            print(f"Asal: {recipe['area']}")
            print(f"Mood: {recipe['mood']}")
