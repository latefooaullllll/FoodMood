from database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""")

tables = cursor.fetchall()

print("=== DAFTAR TABEL DATABASE FOODMOOD ===")

for table in tables:
    print("-", table["name"])

if any(table["name"] == "recommendation_history" for table in tables):
    print("\nTabel recommendation_history berhasil dibuat!")
else:
    print("\nTabel recommendation_history belum ditemukan.")

conn.close()