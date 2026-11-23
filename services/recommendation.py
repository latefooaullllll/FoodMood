
from database.db import get_connection


# ==========================================
# PENGATURAN REKOMENDASI
# ==========================================

MIN_MATCHED_INGREDIENTS = 2
MIN_MATCH_PERCENTAGE = 20
CATEGORY_BONUS = 15


# ==========================================
# ALIAS BAHAN BAHASA INDONESIA
# ==========================================

ALIAS_BAHAN = {
    # Protein
    "ayam": "chicken",
    "daging ayam": "chicken",
    "sapi": "beef",
    "daging sapi": "beef",
    "kambing": "goat",
    "daging kambing": "goat",
    "domba": "lamb",
    "ikan": "fish",
    "udang": "prawns",
    "cumi": "squid",
    "cumi-cumi": "squid",
    "telur": "egg",
    "telur ayam": "egg",

    # Sayuran
    "kentang": "potato",
    "wortel": "carrot",
    "tomat": "tomato",
    "bawang": "onion",
    "bawang bombai": "onion",
    "bawang merah": "shallot",
    "bawang putih": "garlic",
    "cabai": "chili",
    "cabe": "chili",
    "paprika": "paprika",
    "brokoli": "broccoli",
    "bayam": "spinach",
    "jamur": "mushroom",
    "jamur tiram": "oyster mushrooms",
    "terong": "aubergine",
    "terung": "aubergine",
    "timun": "cucumber",
    "mentimun": "cucumber",
    "jagung": "sweetcorn",
    "kol": "cabbage",
    "kubis": "cabbage",
    "selada": "lettuce",
    "buncis": "green beans",
    "kacang polong": "peas",
    "daun bawang": "spring onions",
    "daun kemangi": "basil leaves",
    "kemangi": "basil",

    # Bumbu dan rempah
    "jahe": "ginger",
    "kunyit": "turmeric",
    "ketumbar": "coriander",
    "lada": "pepper",
    "merica": "pepper",
    "lada hitam": "black pepper",
    "garam": "salt",
    "gula": "sugar",
    "gula pasir": "granulated sugar",
    "kecap": "soy sauce",
    "kecap manis": "sweet soy sauce",
    "saus tomat": "tomato ketchup",
    "saus sambal": "chili sauce",
    "jeruk nipis": "lime",
    "jeruk lemon": "lemon",
    "jintan": "cumin",
    "pala": "nutmeg",
    "daun salam": "bay leaf",
    "daun peterseli": "parsley",
    "safron": "saffron",

    # Bahan tambahan
    "susu": "milk",
    "keju": "cheese",
    "keju parmesan": "parmesan cheese",
    "mentega": "butter",
    "margarin": "margarine",
    "tepung": "plain flour",
    "tepung terigu": "plain flour",
    "tepung jagung": "cornstarch",
    "tepung kentang": "potato starch",
    "tepung serbaguna": "all purpose flour",
    "minyak": "oil",
    "minyak zaitun": "olive oil",
    "minyak goreng": "vegetable oil",
    "minyak bunga matahari": "sunflower oil",
    "madu": "honey",
    "nasi": "rice",
    "beras": "rice",
    "mie": "noodles",
    "mi": "noodles",
    "roti": "bread",
    "santan": "coconut milk",
    "kelapa": "coconut",
    "kacang": "peanuts",
    "selai kacang": "peanut butter",
    "alpukat": "avocado",
    "apel": "apple",
    "kismis": "raisins",
    "air": "water",

    # Bahan khusus
    "krim kental": "double cream",
    "krim": "cream",
    "adas": "fennel",
    "moster": "mustard",
    "daun bawang prei": "leek",
    "kucai": "chives",
    "zaitun hijau": "green olives",
    "zaitun hitam": "black olives",
    "paprika panggang": "roasted pepper",
    "paprika merah": "red pepper",
    "cabai merah": "red chilli",
    "daun ketumbar": "cilantro",
    "buncis besar": "runner beans",
    "jamur tiram": "oyster mushrooms",
    "kaldu ayam": "chicken stock",
    "kaldu ikan": "fish stock",
    "dada ayam": "chicken breast",
    "hati ayam": "chicken liver",
    "daging asap": "bacon",
    "tomat kalengan": "tinned tomatoes",
    "tomat anggur": "grape tomatoes",
    "tomat tangkai": "vine tomatoes",
    "pure tomat": "tomato puree",
    "yoghurt yunani": "greek yogurt",
    "krim asam": "sour cream",
    "tepung serbaguna": "all purpose flour",
    "jagung utuh": "corn on the cob",
    "kacang pinus": "pine nuts",
    "cuka balsamik": "balsamic vinegar",
    "cuka anggur merah": "red wine vinegar",
    "saus ikan": "fish sauce",
    "saus ikan thailand": "thai fish sauce",
    "pasta kari hijau thailand": "thai green curry paste",
    "saus salsa hijau": "green salsa",
    "kulit taco renyah": "hard taco shells",
    "kacang tumbuk": "refried beans",
    "serpihan cabai merah": "red pepper flakes",
    "bubuk moster": "mustard powder",
    "moster dijon": "dijon mustard",
    "daging sapi giling": "ground beef",
    "daging sapi cincang": "minced beef",
    "daging babi": "pork",
    "daging babi cincang": "minced pork",
    "kaki katak": "frogs legs",
    "krim fermentasi": "creme fraiche",
    "krim kental": "heavy cream",
    "jintan putih": "cumin",
    "jintan putih bubuk": "ground cumin",
    "kale": "kale",
    "zukini": "zucchini",
    "sosis": "sausages",
    "oat": "oats",
    "anggur sherry": "sherry",
    "anggur sherry kering": "dry sherry",
}


# ==========================================
# PENYERAGAMAN NAMA BAHAN
# ==========================================

ALIAS_JAMAK = {
    "onions": "onion",
    "potatoes": "potato",
    "tomatoes": "tomato",
    "tomatos": "tomato",
    "carrots": "carrot",
    "eggs": "egg",
    "mushrooms": "mushroom",
    "peppers": "pepper",
    "chilies": "chili",
    "chillies": "chili",
    "lemons": "lemon",
    "limes": "lime",
    "apples": "apple",
    "bananas": "banana",
    "oranges": "orange",
    "chicken breasts": "chicken",
    "chicken breast": "chicken",
    "beef steaks": "beef",
    "shrimp": "prawns",
    "shallots": "shallot",
    "spring onion": "spring onions",
    "tinned tomatos": "tinned tomatoes",
    "green olive": "green olives",
    "black olive": "black olives",
    "jalapenos": "jalapeno",
    "jalapenos": "jalapeno",
}


# ==========================================
# TERJEMAHAN NAMA BAHAN
# ==========================================

NAMA_BAHAN_INDONESIA = {
    # Protein
    "chicken": "Ayam",
    "beef": "Daging sapi",
    "goat": "Daging kambing",
    "lamb": "Daging domba",
    "fish": "Ikan",
    "prawns": "Udang",
    "squid": "Cumi-cumi",
    "egg": "Telur",
    "pork": "Daging babi",
    "bacon": "Daging asap",
    "ground beef": "Daging sapi giling",
    "minced beef": "Daging sapi cincang",
    "minced pork": "Daging babi cincang",
    "frogs legs": "Kaki katak",
    "chicken breast": "Dada ayam",
    "chicken liver": "Hati ayam",

    # Sayuran
    "potato": "Kentang",
    "carrot": "Wortel",
    "tomato": "Tomat",
    "onion": "Bawang bombai",
    "shallot": "Bawang merah",
    "garlic": "Bawang putih",
    "chili": "Cabai",
    "red chilli": "Cabai merah",
    "red chili": "Cabai merah",
    "bell pepper": "Paprika",
    "paprika": "Paprika",
    "roasted pepper": "Paprika panggang",
    "red pepper": "Paprika merah",
    "broccoli": "Brokoli",
    "spinach": "Bayam",
    "mushroom": "Jamur",
    "oyster mushrooms": "Jamur tiram",
    "aubergine": "Terong",
    "eggplant": "Terong",
    "cucumber": "Timun",
    "sweetcorn": "Jagung",
    "corn": "Jagung",
    "corn on the cob": "Jagung utuh",
    "cabbage": "Kubis",
    "lettuce": "Selada",
    "green beans": "Buncis",
    "runner beans": "Buncis besar",
    "peas": "Kacang polong",
    "spring onions": "Daun bawang",
    "scallions": "Daun bawang",
    "leek": "Daun bawang prei",
    "fennel": "Adas",
    "basil": "Kemangi",
    "basil leaves": "Daun kemangi",
    "chives": "Kucai",
    "parsley": "Daun peterseli",
    "cilantro": "Daun ketumbar",
    "avocado": "Alpukat",
    "grape tomatoes": "Tomat anggur",
    "vine tomatoes": "Tomat tangkai",
    "kale": "Kale",
    "zucchini": "Zukini",

    # Bumbu dan rempah
    "ginger": "Jahe",
    "turmeric": "Kunyit",
    "coriander": "Ketumbar",
    "pepper": "Lada",
    "black pepper": "Lada hitam",
    "ground black pepper": "Lada hitam bubuk",
    "cayenne pepper": "Cabai rawit bubuk",
    "salt": "Garam",
    "sugar": "Gula",
    "granulated sugar": "Gula pasir",
    "cumin": "Jintan putih",
    "ground cumin": "Jintan putih bubuk",
    "nutmeg": "Pala",
    "bay leaf": "Daun salam",
    "thyme": "Daun timi",
    "marjoram": "Marjoram",
    "saffron": "Safron",
    "mustard": "Moster",
    "mustard powder": "Bubuk moster",
    "ground mustard": "Moster bubuk",
    "dijon mustard": "Moster Dijon",
    "smoked paprika": "Paprika asap",
    "red pepper flakes": "Serpihan cabai merah",
    "jalapeno": "Cabai jalapeno",

    # Bahan tambahan
    "milk": "Susu",
    "cheese": "Keju",
    "parmesan": "Keju parmesan",
    "parmesan cheese": "Keju parmesan",
    "butter": "Mentega",
    "margarine": "Margarin",
    "plain flour": "Tepung terigu",
    "flour": "Tepung",
    "all purpose flour": "Tepung serbaguna",
    "cornstarch": "Tepung jagung",
    "potato starch": "Tepung kentang",
    "oil": "Minyak",
    "olive oil": "Minyak zaitun",
    "vegetable oil": "Minyak goreng",
    "sunflower oil": "Minyak bunga matahari",
    "honey": "Madu",
    "rice": "Beras atau nasi",
    "noodles": "Mi",
    "bread": "Roti",
    "coconut milk": "Santan",
    "coconut": "Kelapa",
    "peanut butter": "Selai kacang",
    "peanuts": "Kacang tanah",
    "raisins": "Kismis",
    "pine nuts": "Kacang pinus",
    "oats": "Oat",
    "water": "Air",
    "apple": "Apel",

    # Saus dan cairan
    "soy sauce": "Kecap",
    "sweet soy sauce": "Kecap manis",
    "tomato ketchup": "Saus tomat",
    "chili sauce": "Saus sambal",
    "lime": "Jeruk nipis",
    "lemon": "Jeruk lemon",
    "green olives": "Zaitun hijau",
    "black olives": "Zaitun hitam",
    "fish sauce": "Saus ikan",
    "thai fish sauce": "Saus ikan Thailand",
    "thai green curry paste": "Pasta kari hijau Thailand",
    "green salsa": "Saus salsa hijau",
    "tomato puree": "Pure tomat",
    "tinned tomatoes": "Tomat kalengan",
    "tinned tomatos": "Tomat kalengan",
    "balsamic vinegar": "Cuka balsamik",
    "red wine vinegar": "Cuka anggur merah",
    "vinegar": "Cuka",
    "sherry": "Anggur sherry",
    "dry sherry": "Anggur sherry kering",

    # Kaldu dan produk susu
    "chicken stock": "Kaldu ayam",
    "chicken stock cube": "Kaldu ayam bubuk",
    "fish stock": "Kaldu ikan",
    "double cream": "Krim kental",
    "heavy cream": "Krim kental",
    "cream": "Krim",
    "creme fraiche": "Krim fermentasi",
    "greek yogurt": "Yoghurt Yunani",
    "sour cream": "Krim asam",
    "creamed corn": "Jagung krim",

    # Bahan khusus lainnya
    "hard taco shells": "Kulit taco renyah",
    "refried beans": "Kacang tumbuk",
}


# ==========================================
# TERJEMAHAN KATEGORI RESEP
# ==========================================

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
    "miscellaneous": "Lain-lain",
}


# ==========================================
# FUNGSI PENYERAGAMAN BAHAN
# ==========================================

def normalize_ingredient(name):
    """Menyeragamkan nama bahan agar mudah dicocokkan."""

    name = str(name or "").strip().lower()

    if name in ALIAS_BAHAN:
        name = ALIAS_BAHAN[name]

    if name in ALIAS_JAMAK:
        name = ALIAS_JAMAK[name]

    return name


def translate_ingredient(name):
    """Mengubah nama bahan menjadi Bahasa Indonesia."""

    normalized = normalize_ingredient(name)

    return NAMA_BAHAN_INDONESIA.get(
        normalized,
        str(name).strip().capitalize()
    )


def translate_category(category):
    """Mengubah kategori resep menjadi Bahasa Indonesia."""

    if not category:
        return "Lain-lain"

    normalized = str(category).strip().lower()

    return KATEGORI_INDONESIA.get(
        normalized,
        str(category).strip()
    )


# ==========================================
# FUNGSI REKOMENDASI RESEP
# ==========================================

def recommend_by_ingredients(user_ingredients):
    """Memberikan rekomendasi resep berdasarkan bahan yang tersedia."""

    bahan_tersedia = {
        normalize_ingredient(bahan)
        for bahan in user_ingredients
        if str(bahan).strip()
    }

    if not bahan_tersedia:
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
                r.image_url
            FROM recipes r
        """)

        recipes = cursor.fetchall()

        hasil_rekomendasi = []

        for recipe in recipes:
            cursor.execute("""
                SELECT i.name
                FROM ingredients i
                JOIN recipe_ingredients ri
                    ON i.id = ri.ingredient_id
                WHERE ri.recipe_id = ?
            """, (recipe["id"],))

            bahan_resep_asli = [
                row["name"] for row in cursor.fetchall()
            ]

            bahan_resep = {
                normalize_ingredient(bahan)
                for bahan in bahan_resep_asli
            }

            if not bahan_resep:
                continue

            bahan_cocok = bahan_tersedia.intersection(bahan_resep)
            bahan_belum_ada = bahan_resep.difference(bahan_tersedia)

            jumlah_cocok = len(bahan_cocok)
            jumlah_seluruh = len(bahan_resep)

            persentase_cocok = (
                jumlah_cocok / jumlah_seluruh
            ) * 100

            if jumlah_cocok < MIN_MATCHED_INGREDIENTS:
                continue

            if persentase_cocok < MIN_MATCH_PERCENTAGE:
                continue

            bonus_kategori = (
                CATEGORY_BONUS if recipe["category"] else 0
            )

            skor_prioritas = persentase_cocok + bonus_kategori

            hasil_rekomendasi.append({
                "id": recipe["id"],
                "meal_id": recipe["meal_id"],
                "name": recipe["name"],
                "category": translate_category(recipe["category"]),
                "area": recipe["area"],
                "image_url": recipe["image_url"],
                "matched_count": jumlah_cocok,
                "total_ingredients": jumlah_seluruh,
                "match_percentage": round(persentase_cocok, 2),
                "category_bonus": bonus_kategori,
                "priority_score": round(skor_prioritas, 2),

                "matched_ingredients": sorted([
                    translate_ingredient(bahan)
                    for bahan in bahan_cocok
                ]),

                "missing_ingredients": sorted([
                    translate_ingredient(bahan)
                    for bahan in bahan_belum_ada
                ]),
            })

        hasil_rekomendasi.sort(
            key=lambda item: (
                item["priority_score"],
                item["match_percentage"],
                item["matched_count"]
            ),
            reverse=True
        )

        return hasil_rekomendasi

    finally:
        conn.close()


# ==========================================
# PENGUJIAN
# ==========================================

if __name__ == "__main__":

    bahan_uji = [
        "Ayam",
        "Bawang putih",
        "Kentang",
        "Susu"
    ]

    hasil = recommend_by_ingredients(bahan_uji)

    print("=== HASIL REKOMENDASI FOODMOOD ===")
    print("Bahan tersedia:", ", ".join(bahan_uji))

    if not hasil:
        print("\nBelum ditemukan resep yang sesuai.")

    else:
        for nomor, resep in enumerate(hasil[:5], start=1):

            print(f"\n{nomor}. {resep['name']}")
            print(f"Kategori: {resep['category']}")
            print(f"Kecocokan: {resep['match_percentage']}%")

            print(
                f"Bahan cocok: {resep['matched_count']} "
                f"dari {resep['total_ingredients']}"
            )

            print(
                "Bahan cocok:",
                ", ".join(resep["matched_ingredients"])
            )

            print(
                "Bahan belum tersedia:",
                ", ".join(resep["missing_ingredients"])
            )
