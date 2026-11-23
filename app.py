
from flask import Flask, render_template, request, redirect, url_for, flash

from services.recommendation import recommend_by_ingredients
from services.mood_recommendation import recommend_by_mood
from services.leftover_recommendation import recommend_by_leftovers
from services.recipe_rescue import rescue_recipe
from services.anti_bosan import (
    get_anti_bosan_recommendations,
    record_recipe_selection,
    get_recent_history
)

app = Flask(__name__)
app.secret_key = "foodmood-secret-key"


@app.route("/")
def home():
    return render_template("index.html")


# 1. Ingredient Matcher
@app.route("/ingredient-matcher", methods=["GET", "POST"])
def ingredient_matcher():
    results = []
    ingredients = ""

    if request.method == "POST":
        ingredients = request.form.get("ingredients", "")

        ingredient_list = [
            item.strip()
            for item in ingredients.split(",")
            if item.strip()
        ]

        if ingredient_list:
            results = recommend_by_ingredients(ingredient_list)

    return render_template(
        "ingredient_matcher.html",
        results=results,
        ingredients=ingredients
    )


# 2. Mood-Based Recommendation
@app.route("/mood-recommendation", methods=["GET", "POST"])
def mood_recommendation():
    results = []
    selected_mood = ""

    if request.method == "POST":
        selected_mood = request.form.get("mood", "")

        if selected_mood:
            results = recommend_by_mood(selected_mood)

    return render_template(
        "mood_recommendation.html",
        results=results,
        selected_mood=selected_mood
    )


# 3. Smart Leftover
@app.route("/smart-leftover", methods=["GET", "POST"])
def smart_leftover():
    results = []
    leftovers = ""

    if request.method == "POST":
        leftovers = request.form.get("leftovers", "")

        leftover_list = [
            item.strip()
            for item in leftovers.split(",")
            if item.strip()
        ]

        if leftover_list:
            results = recommend_by_leftovers(leftover_list)

    return render_template(
        "smart_leftover.html",
        results=results,
        leftovers=leftovers
    )


# 4. Recipe Rescue
@app.route("/recipe-rescue", methods=["GET", "POST"])
def recipe_rescue():
    result = None
    recipe_name = ""
    ingredients = ""

    if request.method == "POST":
        recipe_name = request.form.get("recipe_name", "")
        ingredients = request.form.get("ingredients", "")

        available_ingredients = [
            item.strip()
            for item in ingredients.split(",")
            if item.strip()
        ]

        result = rescue_recipe(
            recipe_name,
            available_ingredients
        )

    return render_template(
        "recipe_rescue.html",
        result=result,
        recipe_name=recipe_name,
        ingredients=ingredients
    )


# 5. Anti-Bosan Menu
@app.route("/anti-bosan", methods=["GET", "POST"])
def anti_bosan():
    if request.method == "POST":
        recipe_id = request.form.get("recipe_id", type=int)

        if recipe_id and record_recipe_selection(recipe_id):
            flash("Resep berhasil disimpan ke riwayat!")
        else:
            flash("Gagal menyimpan pilihan resep.")

        return redirect(url_for("anti_bosan"))

    recommendations = get_anti_bosan_recommendations()
    history = get_recent_history()

    return render_template(
        "anti_bosan.html",
        recommendations=recommendations,
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)
