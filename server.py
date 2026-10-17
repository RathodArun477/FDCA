from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Analysis import analyze_all_cuisine, full_analyze_recipe, recipes_df, countries_df
from difflib import get_close_matches
from API_Service import get_country_live_terroir

app = FastAPI(
    title="FDCA API",
    description="Food Diversity & Cultural Analysis Backend Engine"
)

# Enable CORS for local Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COUNTRY_ALIASES = {
    "united states of america": "united states",
    "usa": "united states",
    "us": "united states",
    "u.s.a.": "united states",
    "u.s.": "united states",
    "uk": "united kingdom",
    "uae": "united arab emirates",
}

def find_best_recipe_match(query: str):
    query = query.lower().strip()
    recipes = recipes_df["Recipe Name"].astype(str).str.lower().tolist()

    if query in recipes:
        return query

    partial = [r for r in recipes if query in r]
    if partial:
        return partial[0]

    close = get_close_matches(query, recipes, n=1, cutoff=0.55)
    if close:
        return close[0]

    return None

@app.get("/api/meta")
def get_metadata():
    countries = sorted([str(c).title() for c in countries_df["Country"].dropna().unique()])
    recipes = sorted([str(r).title() for r in recipes_df["Recipe Name"].dropna().unique()])
    return {
        "countries": countries,
        "recipes": recipes
    }

@app.get("/api/search")
def search_query(q: str):
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    clean_q = q.strip().lower()
    normalized_q = COUNTRY_ALIASES.get(clean_q, clean_q)

    # First check if it matches a country
    country_res = analyze_all_cuisine(normalized_q)

    if country_res.get("climate") is not None:
        # Enrich with live Open-Meteo terroir and geocoding
        terroir = get_country_live_terroir(normalized_q)
        return {
            "type": "country",
            "query": normalized_q,
            "data": country_res,
            "terroir": terroir
        }

    # Otherwise, check if it matches a food/recipe
    matched_recipe = find_best_recipe_match(clean_q)
    if matched_recipe is not None:
        recipe_res = full_analyze_recipe(matched_recipe)
        return {
            "type": "recipe",
            "query": matched_recipe,
            "data": recipe_res
        }

    raise HTTPException(status_code=404, detail="No matching country or recipe found.")

@app.get("/api/compare")
def compare_cultures(country_a: str, country_b: str):
    clean_a = COUNTRY_ALIASES.get(country_a.strip().lower(), country_a.strip().lower())
    clean_b = COUNTRY_ALIASES.get(country_b.strip().lower(), country_b.strip().lower())

    res_a = analyze_all_cuisine(clean_a)
    res_b = analyze_all_cuisine(clean_b)

    terroir_a = get_country_live_terroir(clean_a)
    terroir_b = get_country_live_terroir(clean_b)

    return {
        "country_a": {"name": country_a, "data": res_a, "terroir": terroir_a},
        "country_b": {"name": country_b, "data": res_b, "terroir": terroir_b}
    }
