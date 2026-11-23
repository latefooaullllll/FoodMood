
from database.db import get_connection


def get_anti_bosan_recommendations(limit=10, recent_limit=5):
    """
    Memberikan rekomendasi resep dengan menghindari
    resep yang baru saja dipilih pengguna.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Mengambil riwayat resep yang baru dipilih
    cursor.execute("""
        SELECT recipe_id
        FROM recommendation_history
        ORDER BY selected_at DESC, id DESC
        LIMIT ?
    """, (recent_limit,))

    recent_ids = [row["recipe_id"] for row in cursor.fetchall()]

    if recent_ids:
        placeholders = ",".join("?" for _ in recent_ids)

        cursor.execute(f"""
            SELECT id, name, category, image_url
            FROM recipes
            WHERE id NOT IN ({placeholders})
            ORDER BY RANDOM()
            LIMIT ?
        """, (*recent_ids, limit))

        recommendations = cursor.fetchall()

    else:
        cursor.execute("""
            SELECT id, name, category, image_url
            FROM recipes
            ORDER BY RANDOM()
            LIMIT ?
        """, (limit,))

        recommendations = cursor.fetchall()

    # Jika semua resep masuk riwayat, tampilkan kembali
    # resep yang tersedia agar rekomendasi tidak kosong.
    if not recommendations:
        cursor.execute("""
            SELECT id, name, category, image_url
            FROM recipes
            ORDER BY RANDOM()
            LIMIT ?
        """, (limit,))

        recommendations = cursor.fetchall()

    conn.close()

    return [dict(row) for row in recommendations]


def record_recipe_selection(recipe_id):
    """Menyimpan resep yang dipilih pengguna."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM recipes WHERE id = ?",
        (recipe_id,)
    )

    recipe = cursor.fetchone()

    if not recipe:
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO recommendation_history (recipe_id)
        VALUES (?)
    """, (recipe_id,))

    conn.commit()
    conn.close()

    return True


def get_recent_history(limit=5):
    """Mengambil riwayat resep yang terakhir dipilih."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.name, r.category, h.selected_at
        FROM recommendation_history h
        JOIN recipes r ON h.recipe_id = r.id
        ORDER BY h.selected_at DESC, h.id DESC
        LIMIT ?
    """, (limit,))

    history = cursor.fetchall()
    conn.close()

    return [dict(row) for row in history]


if __name__ == "__main__":
    print("=== FOODMOOD: ANTI-BOSAN MENU ===")

    recommendations = get_anti_bosan_recommendations()

    print("\n=== REKOMENDASI RESEP ===")

    for index, recipe in enumerate(recommendations, start=1):
        print(f"{index}. {recipe['name']}")
        print(f"   Kategori: {recipe['category']}")
        print(f"   ID Resep: {recipe['id']}")

    if not recommendations:
        print("Belum ada data resep.")
    else:
        print("\nPilih resep yang ingin dicoba.")
        choice = input("Masukkan nomor resep (0 untuk batal): ")

        try:
            choice = int(choice)

            if choice == 0:
                print("Tidak ada resep yang dipilih.")

            elif 1 <= choice <= len(recommendations):
                selected_recipe = recommendations[choice - 1]

                success = record_recipe_selection(
                    selected_recipe["id"]
                )

                if success:
                    print(
                        f"\nResep '{selected_recipe['name']}' "
                        "berhasil disimpan ke riwayat!"
                    )
                else:
                    print("\nGagal menyimpan riwayat resep.")

            else:
                print("\nNomor pilihan tidak valid.")

        except ValueError:
            print("\nMasukkan nomor yang benar.")

    print("\n=== RIWAYAT RESEP TERAKHIR ===")

    history = get_recent_history()

    if history:
        for item in history:
            print(f"- {item['name']} ({item['category']})")
            print(f"  Dipilih: {item['selected_at']}")
    else:
        print("Belum ada riwayat resep.")

    print("\nProses Anti-Bosan Menu selesai!")
