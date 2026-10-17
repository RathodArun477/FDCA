import streamlit as st
import pandas as pd
from collections import Counter
from Analysis import analyze_all_cuisine, full_analyze_recipe, recipes_df, countries_df
from difflib import get_close_matches
import plotly.express as px
import plotly.graph_objects as go
from API_Service import get_country_live_terroir

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FDCA - Food Diversity & Cultural Analysis",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- COUNTRY ALIASES ----------------
COUNTRY_ALIASES = {
    "united states of america": "united states",
    "usa": "united states",
    "us": "united states",
    "u.s.a.": "united states",
    "u.s.": "united states",
    "uk": "united kingdom",
    "uae": "united arab emirates",
}

# ---------------- FUZZY RECIPE MATCH ----------------
def find_best_recipe_match(query, recipes_df):
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

# ---------------- HIGH CONTRAST BOTANICAL SAGE GREEN & WARM TERRACOTTA THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap');

/* Force Page Background & Font across all Streamlit Containers */
html, body, [data-testid="stAppViewContainer"], .main, .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: #EAEFEA !important;
    color: #112217 !important;
}

/* Ensure Main Block Container doesn't have excess top padding */
.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 3rem !important;
    max-width: 1250px !important;
}

/* Brand Badge */
.brand-badge {
    display: inline-block;
    padding: 6px 16px;
    background: #D5E2D7;
    color: #1A402E;
    font-size: 0.82rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    border-radius: 9999px;
    margin-bottom: 0.6rem;
    border: 1.5px solid #AFC8B4;
    box-shadow: 0 2px 6px rgba(26, 64, 46, 0.08);
}

/* Main Hero Typography */
.main-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.85rem !important;
    font-weight: 800 !important;
    color: #0F2D1E !important;
    line-height: 1.15 !important;
    margin-bottom: 0.35rem !important;
}

.subtitle {
    color: #2D5A43 !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    margin-bottom: 1.8rem !important;
    line-height: 1.5 !important;
}

/* Glassmorphism & Bento Grid Cards */
.bento-card {
    background: rgba(255, 255, 255, 0.92) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: 18px !important;
    padding: 24px !important;
    border: 1.5px solid #CCDBCD !important;
    box-shadow: 0 10px 30px -5px rgba(20, 50, 35, 0.08), 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    margin-bottom: 18px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

.bento-card:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 14px 34px -4px rgba(20, 50, 35, 0.13) !important;
    border-color: #9DBFA4 !important;
}

.bento-hero {
    background: linear-gradient(135deg, rgba(235, 244, 237, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
    border: 1.5px solid #B8D2BF !important;
}

.bento-terracotta {
    background: linear-gradient(135deg, rgba(255, 245, 239, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
    border: 1.5px solid #F3C3A8 !important;
}

.bento-title {
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    color: #0F2D1E !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin-bottom: 14px !important;
}

/* Contrast Tags & Badges */
.tag {
    display: inline-flex !important;
    align-items: center !important;
    padding: 6px 14px !important;
    margin: 4px !important;
    background: #E4ECE5 !important;
    color: #143524 !important;
    border-radius: 9999px !important;
    border: 1.5px solid #B4CDBA !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

.tag:hover {
    background: #D2E2D5 !important;
    color: #0A1F15 !important;
}

.tag-terracotta {
    background: #FEECE3 !important;
    color: #9C3A10 !important;
    border-color: #F7BA98 !important;
}

.tag-terracotta:hover {
    background: #FDDEC0 !important;
}

.stat-chip {
    display: inline-flex !important;
    align-items: center !important;
    padding: 6px 14px !important;
    background: #FEEDE4 !important;
    border-radius: 10px !important;
    border: 1.5px solid #F5BCA0 !important;
    color: #9C3A10 !important;
    font-size: 0.88rem !important;
    font-weight: 800 !important;
    margin-right: 8px !important;
    margin-bottom: 8px !important;
}

/* Quick Suggestion Buttons */
.stButton>button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    border: 1.5px solid #B4CDBA !important;
    background-color: #FFFFFF !important;
    color: #1A402E !important;
    box-shadow: 0 2px 6px rgba(26, 64, 46, 0.05) !important;
    transition: all 0.2s ease !important;
    padding: 8px 16px !important;
}

.stButton>button:hover {
    background-color: #DDEBE0 !important;
    border-color: #1A402E !important;
    color: #0A1F15 !important;
    transform: translateY(-1px) !important;
}

/* Tab Overrides */
div[data-baseweb="tab-list"] {
    gap: 10px !important;
    border-bottom: 2px solid #C8DACB !important;
    padding-bottom: 2px !important;
}
div[data-baseweb="tab"] {
    background: #DCE7DF !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 10px 22px !important;
    font-weight: 700 !important;
    color: #2D5A43 !important;
    border: 1.5px solid #B8CFC0 !important;
    border-bottom: none !important;
}
div[aria-selected="true"] {
    background: #FFFFFF !important;
    color: #0F2D1E !important;
    border: 2px solid #2D5A43 !important;
    border-bottom: 2px solid #FFFFFF !important;
    margin-bottom: -2px !important;
}

/* Input Fields */
.stTextInput>div>div>input {
    border-radius: 14px !important;
    border: 2px solid #AFC8B4 !important;
    background-color: #FFFFFF !important;
    color: #0F2D1E !important;
    padding: 12px 18px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
}

.stTextInput>div>div>input:focus {
    border-color: #1A402E !important;
    box-shadow: 0 0 0 3px rgba(26, 64, 46, 0.2) !important;
}

/* Live Weather Banner */
.terroir-banner {
    background: linear-gradient(90deg, #FFF6EF 0%, #FEEDE3 100%) !important;
    border-left: 6px solid #C05621 !important;
    padding: 14px 20px !important;
    border-radius: 12px !important;
    margin: 14px 0 20px 0 !important;
    border-top: 1.5px solid #F5C6AB !important;
    border-right: 1.5px solid #F5C6AB !important;
    border-bottom: 1.5px solid #F5C6AB !important;
    box-shadow: 0 4px 14px rgba(192, 86, 33, 0.08) !important;
}

/* Native Metrics Styling */
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    color: #0F2D1E !important;
}

[data-testid="stMetricLabel"] {
    font-weight: 800 !important;
    color: #234D37 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-size: 0.85rem !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TAG HELPER ----------------
def tagify(items, highlight=False):
    if not items:
        st.write("No data available.")
        return
    css_cls = 'tag tag-terracotta' if highlight else 'tag'
    html = "".join([f"<span class='{css_cls}'>{i.title()}</span>" for i in items])
    st.markdown(html, unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div style='text-align: center;'><span class='brand-badge'>🌿 Agro-Cultural Intelligence</span></div>", unsafe_allow_html=True)
st.markdown("<div class='main-title' style='text-align: center;'>Food Diversity & Cultural Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle' style='text-align: center;'>Bridging geographical climate zones, agricultural yields, and culinary terroirs.</div>", unsafe_allow_html=True)

# Main Navigation Tabs
tab_explore, tab_compare = st.tabs(["🔍 Explorer & Bento Dashboard", "⚖️ Cross-Culture Comparison"])

# ========================================================
# TAB 1: EXPLORER & BENTO DASHBOARD
# ========================================================
with tab_explore:
    # Session state initialization for quick search tags
    if "search_input" not in st.session_state:
        st.session_state["search_input"] = ""

    def set_quick_query(val):
        st.session_state["search_input"] = val

    # Quick suggestion chips
    st.markdown("<p style='font-size: 0.9rem; color: #1A402E; margin-bottom: 8px; font-weight: 800;'>💡 Quick Explorations:</p>", unsafe_allow_html=True)
    col_q1, col_q2, col_q3, col_q4, col_q5, col_q6 = st.columns(6)
    with col_q1:
        if st.button("🇮🇹 Italy", use_container_width=True, key="btn_it"):
            set_quick_query("Italy")
    with col_q2:
        if st.button("🇮🇳 India", use_container_width=True, key="btn_in"):
            set_quick_query("India")
    with col_q3:
        if st.button("🇲🇽 Mexico", use_container_width=True, key="btn_mx"):
            set_quick_query("Mexico")
    with col_q4:
        if st.button("🇯🇵 Japan", use_container_width=True, key="btn_jp"):
            set_quick_query("Japan")
    with col_q5:
        if st.button("🍕 Pizza", use_container_width=True, key="btn_pizza"):
            set_quick_query("Classic Margherita Pizza")
    with col_q6:
        if st.button("🍲 Kimchi", use_container_width=True, key="btn_kimchi"):
            set_quick_query("Spicy Kimchi Fried Rice")

    search_query = st.text_input(
        label="Search query",
        value=st.session_state["search_input"],
        placeholder="Type a country (e.g. Italy, India, Thailand) or a food item (e.g. Pizza, Curry)...",
        label_visibility="collapsed",
        key="main_search_input"
    )

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    # ---------------- EMPTY LANDING BENTO ----------------
    if not search_query.strip():
        col_b1, col_b2, col_b3 = st.columns([1.2, 1, 1])
        with col_b1:
            st.markdown("""
            <div class='bento-card bento-hero'>
                <span style='font-size: 2.2rem;'>🌍</span>
                <div class='bento-title' style='margin-top: 10px;'>Country Agro-Terroir</div>
                <p style='color: #2D5A43; font-size: 0.95rem; line-height: 1.6; font-weight: 500;'>
                    Discover how regional temperatures and domestic agricultural farming shape national culinary identities.
                </p>
                <span class='stat-chip'>192 Countries</span>
                <span class='stat-chip'>Live Terroir API</span>
            </div>
            """, unsafe_allow_html=True)
        with col_b2:
            st.markdown("""
            <div class='bento-card'>
                <span style='font-size: 2.2rem;'>🍽</span>
                <div class='bento-title' style='margin-top: 10px;'>Ingredient Lineage</div>
                <p style='color: #2D5A43; font-size: 0.95rem; line-height: 1.6; font-weight: 500;'>
                    Reverse-engineer signature culinary dishes back to raw botanical crops and international producer regions.
                </p>
                <span class='stat-chip'>Crop Mapping</span>
                <span class='stat-chip'>Macro Nutrients</span>
            </div>
            """, unsafe_allow_html=True)
        with col_b3:
            st.markdown("""
            <div class='bento-card bento-terracotta'>
                <span style='font-size: 2.2rem;'>🌾</span>
                <div class='bento-title' style='margin-top: 10px; color: #9C3A10;'>Cultural Autonomy</div>
                <p style='color: #7B2D0C; font-size: 0.95rem; line-height: 1.6; font-weight: 500;'>
                    Evaluate domestic food self-sufficiency vs. historical reliance on global trade routes and imported crops.
                </p>
                <span class='stat-chip'>Climate Fit %</span>
                <span class='stat-chip'>Dependency Ratio</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        # ---------------- SEARCH ACTION ----------------
        query = search_query.strip().lower()
        query = COUNTRY_ALIASES.get(query, query)

        with st.spinner("Analyzing agricultural and culinary datasets..."):
            country_result = analyze_all_cuisine(query)

        # ---------------- FOOD SEARCH (BENTO GRID) ----------------
        if country_result["climate"] is None:
            matched_recipe = find_best_recipe_match(query, recipes_df)

            if matched_recipe is None:
                st.error("No matching country or food item found. Try searching for a country (e.g., 'India', 'France') or a dish (e.g., 'Pizza', 'Curry').")
            else:
                recipe_result = full_analyze_recipe(matched_recipe)

                # Hero Bento Header
                st.markdown(f"""
                <div class='bento-card bento-hero'>
                    <span class='brand-badge' style='background: #FEECE3; color: #9C3A10; border-color: #F7BA98;'>Culinary Dish Profile</span>
                    <h2 style='font-family: "Playfair Display", serif; color: #0F2D1E; margin: 6px 0 10px 0; font-size: 2.2rem; font-weight: 800;'>🍽 {matched_recipe.title()}</h2>
                </div>
                """, unsafe_allow_html=True)

                # Bento Row 1: Metrics
                cal_str = f"{recipe_result['calories']} kcal" if recipe_result['calories'] else "N/A"
                prep_str = f"{recipe_result['prep_time']}m" if recipe_result['prep_time'] else "N/A"
                cook_str = f"{recipe_result['cook_time']}m" if recipe_result['cook_time'] else "N/A"
                serv_str = f"{recipe_result['servings']}" if recipe_result['servings'] else "N/A"

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("🔥 Calories / Serv.", cal_str)
                m2.metric("⏱ Prep Time", prep_str)
                m3.metric("🍳 Cook Time", cook_str)
                m4.metric("👥 Servings", serv_str)

                if recipe_result["dietary"]:
                    diet_html = "".join([f"<span class='stat-chip'>🌱 {d.title()}</span>" for d in recipe_result["dietary"]])
                    st.markdown(f"<div style='margin-bottom: 14px;'>{diet_html}</div>", unsafe_allow_html=True)

                # Bento Row 2: Ingredients vs Botanical Crops
                b1, b2 = st.columns(2)
                with b1:
                    st.markdown("""
                    <div class='bento-card' style='min-height: 240px;'>
                        <div class='bento-title'>🛒 Ingredients Breakdown</div>
                    """, unsafe_allow_html=True)
                    tagify(recipe_result["ingredients"])
                    st.markdown("</div>", unsafe_allow_html=True)

                with b2:
                    st.markdown("""
                    <div class='bento-card bento-terracotta' style='min-height: 240px;'>
                        <div class='bento-title' style='color: #9C3A10;'>🌾 Botanical Crops Sourced</div>
                    """, unsafe_allow_html=True)
                    tagify(recipe_result["crops"], highlight=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Interactive Global Producer Map for Dish Crops
                if recipe_result["countries_for_crops"]:
                    st.markdown("""
                    <div class='bento-card'>
                        <div class='bento-title'>🌐 Global Producer Map for Recipe Crops</div>
                    """, unsafe_allow_html=True)
                    
                    geo_records = []
                    for crop_name, producer_countries in recipe_result["countries_for_crops"].items():
                        for p_country in producer_countries:
                            geo_records.append({"Country": p_country.title(), "Crop": crop_name.title()})
                    
                    if geo_records:
                        geo_df = pd.DataFrame(geo_records).groupby("Country", as_index=False).agg({"Crop": lambda x: ", ".join(set(x))})
                        geo_df["Crops Cultivated"] = geo_df["Crop"]
                        geo_df["Count"] = geo_df["Crop"].apply(lambda x: len(x.split(", ")))

                        fig_dish_map = px.choropleth(
                            geo_df,
                            locations="Country",
                            locationmode="country names",
                            color="Count",
                            hover_name="Country",
                            hover_data={"Count": True, "Crops Cultivated": True},
                            color_continuous_scale=[[0, "#E2ECE5"], [0.5, "#6A9B7D"], [1, "#1A402E"]],
                        )
                        fig_dish_map.update_layout(
                            margin={"r": 0, "t": 0, "l": 0, "b": 0},
                            coloraxis_showscale=False,
                            geo=dict(bgcolor='rgba(0,0,0,0)', showframe=False, showcoastlines=True, coastlinecolor="#B4CDBA", projection_type='natural earth'),
                            height=360
                        )
                        st.plotly_chart(fig_dish_map, use_container_width=True)

                    st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- COUNTRY SEARCH (BENTO DASHBOARD) ----------------
        else:
            terroir_data = get_country_live_terroir(query)
            flag_emoji = terroir_data["geo"]["flag"] if (terroir_data and terroir_data.get("geo")) else "🌍"
            country_display_name = terroir_data["geo"]["name"] if (terroir_data and terroir_data.get("geo")) else search_query.title()

            # Bento Top Hero: Country Terroir Banner
            st.markdown(f"""
            <div class='bento-card bento-hero'>
                <span class='brand-badge'>National Profile</span>
                <h1 style='font-family: "Playfair Display", serif; color: #0F2D1E; margin: 4px 0 8px 0; font-size: 2.5rem; font-weight: 800;'>{flag_emoji} {country_display_name}</h1>
                <p style='color: #2D5A43; margin: 0; font-size: 1.05rem; font-weight: 600;'>
                    Climatic Zone Classification: <b style='color: #0F2D1E; background: #D5E2D7; padding: 4px 10px; border-radius: 6px;'>{country_result['climate']}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Live Weather Banner (Terracotta & Amber)
            if terroir_data and terroir_data.get("weather"):
                w = terroir_data["weather"]
                g = terroir_data["geo"]
                precip_val = f"{w['precipitation']} mm" if w.get('precipitation') is not None else "0 mm"
                hum_val = f"{w['humidity']}%" if w.get('humidity') is not None else "N/A"
                temp_val = f"{w['temp_c']} °C" if w.get('temp_c') is not None else "N/A"

                st.markdown(f"""
                <div class='terroir-banner'>
                    <span style='color: #9C3A10; font-weight:800;'>🌤 Live Agricultural Terroir (Open-Meteo API):</span> 
                    <span style='color: #381A0B; margin-left: 8px; font-weight:600;'>Current Temp: <b style='color: #7B2D0C;'>{temp_val}</b> | Humidity: <b style='color: #7B2D0C;'>{hum_val}</b> | Precipitation: <b style='color: #7B2D0C;'>{precip_val}</b></span>
                    <span style='color: #7B2D0C; font-size: 0.85rem; margin-left: 10px; font-weight: 700;'>({g.get('timezone', 'Local')})</span>
                </div>
                """, unsafe_allow_html=True)

            # Bento Grid: 3 Metric KPI Cards
            local = country_result["crop_dependency"]["local_crops_used"]
            imported = country_result["crop_dependency"]["imported_crops_used"]
            fit = int(country_result["climate_alignment"]["alignment_score"] * 100)

            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.markdown(f"""
                <div class='bento-card' style='text-align: center; padding: 22px;'>
                    <div style='color: #2D5A43; font-size: 0.9rem; font-weight: 800; text-transform: uppercase;'>Domestic Crops</div>
                    <div style='font-family: "Playfair Display", serif; font-size: 2.6rem; font-weight: 800; color: #1A402E; margin: 4px 0;'>{local}</div>
                    <div style='color: #4B6354; font-size: 0.82rem; font-weight: 600;'>Grown locally within country borders</div>
                </div>
                """, unsafe_allow_html=True)
            with kpi2:
                st.markdown(f"""
                <div class='bento-card bento-terracotta' style='text-align: center; padding: 22px;'>
                    <div style='color: #9C3A10; font-size: 0.9rem; font-weight: 800; text-transform: uppercase;'>Imported Crops</div>
                    <div style='font-family: "Playfair Display", serif; font-size: 2.6rem; font-weight: 800; color: #9C3A10; margin: 4px 0;'>{imported}</div>
                    <div style='color: #7B2D0C; font-size: 0.82rem; font-weight: 600;'>Historically sourced through global trade</div>
                </div>
                """, unsafe_allow_html=True)
            with kpi3:
                st.markdown(f"""
                <div class='bento-card' style='text-align: center; padding: 22px;'>
                    <div style='color: #2D5A43; font-size: 0.9rem; font-weight: 800; text-transform: uppercase;'>Climate Alignment</div>
                    <div style='font-family: "Playfair Display", serif; font-size: 2.6rem; font-weight: 800; color: #1A402E; margin: 4px 0;'>{fit}%</div>
                    <div style='color: #4B6354; font-size: 0.82rem; font-weight: 600;'>Cuisine compatibility with regional terroir</div>
                </div>
                """, unsafe_allow_html=True)

            # Interactive Global Choropleth Trade Map
            trade_origins = []
            for crop_name in country_result.get("imported_crops", []):
                origin_countries = country_result["countries_for_crops"].get(crop_name, [])
                for oc in origin_countries:
                    trade_origins.append({"Country": oc.title(), "Type": "Trade Supplier", "Crop": crop_name.title()})
            
            # Add target country
            map_data = [{"Country": country_display_name, "Type": "Domestic Nation", "Crop": "Domestic Cuisine Center"}]
            map_data.extend(trade_origins)

            if map_data:
                st.markdown("""
                <div class='bento-card'>
                    <div class='bento-title'>🗺 Global Agricultural Origins & Trade Network</div>
                """, unsafe_allow_html=True)

                map_df = pd.DataFrame(map_data).drop_duplicates(subset=["Country", "Type"])
                
                fig_map = px.choropleth(
                    map_df,
                    locations="Country",
                    locationmode="country names",
                    color="Type",
                    color_discrete_map={"Domestic Nation": "#1A402E", "Trade Supplier": "#C05621"},
                    hover_name="Country",
                    hover_data={"Type": True, "Crop": True}
                )
                fig_map.update_layout(
                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=""),
                    geo=dict(bgcolor='rgba(0,0,0,0)', showframe=False, showcoastlines=True, coastlinecolor="#B4CDBA", projection_type='natural earth'),
                    height=380
                )
                st.plotly_chart(fig_map, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Bento Middle Row: Asymmetric Cards (Cultural Terroir Story & Dominant Recipes)
            mid1, mid2 = st.columns([1.3, 1])
            with mid1:
                st.markdown(f"""
                <div class='bento-card' style='min-height: 290px;'>
                    <div class='bento-title'>✨ Cultural Terroir & Agrarian Narrative</div>
                    <p style='color: #1A3022; font-size: 1rem; line-height: 1.8; margin-top: 10px; font-weight: 500;'>
                        {country_result['analysis_summary']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            with mid2:
                st.markdown("""
                <div class='bento-card bento-terracotta' style='min-height: 290px;'>
                    <div class='bento-title' style='color: #9C3A10;'>🍲 Traditional Signature Recipes</div>
                """, unsafe_allow_html=True)
                tagify(country_result["recipes"][:6], highlight=True)
                if len(country_result["recipes"]) > 6:
                    with st.expander(f"View all {len(country_result['recipes'])} recipes"):
                        tagify(country_result["recipes"], highlight=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Bento Bottom Row: Crops
            bot1, bot2 = st.columns(2)
            with bot1:
                st.markdown("""
                <div class='bento-card'>
                    <div class='bento-title'>🌱 Climate-Aligned Native Crops</div>
                """, unsafe_allow_html=True)
                suitable = country_result["suitable_crops"]
                tagify(suitable[:10])
                if len(suitable) > 10:
                    with st.expander(f"View all {len(suitable)} suitable crops"):
                        tagify(suitable)
                st.markdown("</div>", unsafe_allow_html=True)

            with bot2:
                st.markdown("""
                <div class='bento-card'>
                    <div class='bento-title'>🌾 Key Crops Utilized in Recipes</div>
                """, unsafe_allow_html=True)
                dominant = country_result["crop_dependency"]["dominant_crops"]
                tagify(dominant, highlight=False)
                all_crops = country_result["crops_used_in_recipes"]
                if len(all_crops) > len(dominant):
                    with st.expander(f"View all {len(all_crops)} recipe crops"):
                        tagify(all_crops)
                st.markdown("</div>", unsafe_allow_html=True)

            # Interactive Plotly Analytics Section
            with st.expander("📈 Interactive Analytics & Crop Distribution", expanded=True):
                col_chart1, col_chart2 = st.columns(2)

                # Interactive Donut Chart (Plotly)
                with col_chart1:
                    total_crops = local + imported
                    if total_crops > 0:
                        fig_donut = go.Figure(data=[go.Pie(
                            labels=["Domestic Sourced", "Imported / Trade"],
                            values=[local, imported],
                            hole=.55,
                            marker_colors=["#1A402E", "#C05621"],
                            textinfo="percent+label",
                            textfont_size=12,
                            hoverinfo="label+value+percent"
                        )])
                        fig_donut.update_layout(
                            title=dict(text="Domestic vs. Imported Crop Ratio", font=dict(family="Playfair Display", size=16, color="#0F2D1E")),
                            margin=dict(l=20, r=20, t=40, b=20),
                            showlegend=False,
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            height=280
                        )
                        st.plotly_chart(fig_donut, use_container_width=True)
                    else:
                        st.write("No crop distribution data available.")

                # Interactive Horizontal Bar Chart (Plotly)
                with col_chart2:
                    crop_counts = Counter(country_result["crops_used_in_recipes"])
                    top_crops = crop_counts.most_common(6)

                    if top_crops:
                        crops_labels, counts = zip(*top_crops)
                        crops_labels = [c.title() for c in crops_labels]

                        bar_df = pd.DataFrame({"Crop": crops_labels, "Frequency": counts})
                        fig_bar = px.bar(
                            bar_df,
                            x="Frequency",
                            y="Crop",
                            orientation="h",
                            color_discrete_sequence=["#1A402E"]
                        )
                        fig_bar.update_layout(
                            title=dict(text="Dominant Crops in National Recipes", font=dict(family="Playfair Display", size=16, color="#0F2D1E")),
                            yaxis=dict(autorange="reversed", title=""),
                            xaxis=dict(title="Occurrences in Cuisine", gridcolor="#CCDBCD"),
                            margin=dict(l=20, r=20, t=40, b=20),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            height=280
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)
                    else:
                        st.write("No recipe crop occurrences found.")

# ========================================================
# TAB 2: CROSS-CULTURE COMPARISON (Feature C)
# ========================================================
with tab_compare:
    st.markdown("""
    <div class='bento-card bento-hero'>
        <div class='bento-title'>⚖️ Cross-Culture Bento Comparison</div>
        <p style='color: #2D5A43; font-size: 1rem; margin: 0; font-weight: 500;'>
            Compare agro-climatic terroir, crop autonomy, and staple culinary traditions between any two regions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    country_list = sorted([str(c).title() for c in countries_df["Country"].dropna().unique()])

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        default_idx1 = country_list.index("Italy") if "Italy" in country_list else 0
        country_a = st.selectbox("Select Culture A:", country_list, index=default_idx1)
    with col_c2:
        default_idx2 = country_list.index("Japan") if "Japan" in country_list else 1
        country_b = st.selectbox("Select Culture B:", country_list, index=default_idx2)

    if st.button("Generate Comparison", type="primary", use_container_width=True):
        res_a = analyze_all_cuisine(country_a.lower())
        res_b = analyze_all_cuisine(country_b.lower())

        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        col_comp1, col_comp2 = st.columns(2)

        # Country A Bento Card
        with col_comp1:
            fit_a = int(res_a["climate_alignment"]["alignment_score"] * 100) if res_a.get("climate_alignment") else 0
            st.markdown(f"""
            <div class='bento-card'>
                <h3 style='font-family: "Playfair Display", serif; color: #0F2D1E; margin-top: 0; font-size: 1.8rem; font-weight: 800;'>🌍 {country_a}</h3>
                <p style='color: #2D5A43; font-size: 0.95rem; font-weight: 600;'>Climate Zone: <b style='color: #0F2D1E;'>{res_a.get('climate') or 'Unknown'}</b></p>
                <div style='display: flex; gap: 12px; margin: 14px 0;'>
                    <div style='background: #E4ECE5; padding: 12px; border-radius: 10px; flex: 1; border: 1.5px solid #B4CDBA;'>
                        <span style='font-size: 0.8rem; color: #2D5A43; font-weight: 800; text-transform: uppercase;'>Fit Score</span><br>
                        <b style='font-size: 1.4rem; color: #1A402E; font-family: "Playfair Display", serif;'>{fit_a}%</b>
                    </div>
                    <div style='background: #FEEDE4; padding: 12px; border-radius: 10px; flex: 1; border: 1.5px solid #F5BCA0;'>
                        <span style='font-size: 0.8rem; color: #9C3A10; font-weight: 800; text-transform: uppercase;'>Domestic / Import</span><br>
                        <b style='font-size: 1.4rem; color: #9C3A10; font-family: "Playfair Display", serif;'>{res_a['crop_dependency']['local_crops_used']} / {res_a['crop_dependency']['imported_crops_used']}</b>
                    </div>
                </div>
                <div style='font-weight: 800; color: #0F2D1E; font-size: 0.95rem; margin-top: 14px;'>Staple Crops in Cuisine:</div>
            """, unsafe_allow_html=True)
            tagify(res_a["crop_dependency"]["dominant_crops"][:5])

            st.markdown("<div style='font-weight: 800; color: #0F2D1E; font-size: 0.95rem; margin-top: 14px;'>Key Traditional Dishes:</div>", unsafe_allow_html=True)
            tagify(res_a["recipes"][:4], highlight=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Country B Bento Card
        with col_comp2:
            fit_b = int(res_b["climate_alignment"]["alignment_score"] * 100) if res_b.get("climate_alignment") else 0
            st.markdown(f"""
            <div class='bento-card bento-terracotta'>
                <h3 style='font-family: "Playfair Display", serif; color: #7B2D0C; margin-top: 0; font-size: 1.8rem; font-weight: 800;'>🌍 {country_b}</h3>
                <p style='color: #9C3A10; font-size: 0.95rem; font-weight: 600;'>Climate Zone: <b style='color: #7B2D0C;'>{res_b.get('climate') or 'Unknown'}</b></p>
                <div style='display: flex; gap: 12px; margin: 14px 0;'>
                    <div style='background: #E4ECE5; padding: 12px; border-radius: 10px; flex: 1; border: 1.5px solid #B4CDBA;'>
                        <span style='font-size: 0.8rem; color: #2D5A43; font-weight: 800; text-transform: uppercase;'>Fit Score</span><br>
                        <b style='font-size: 1.4rem; color: #1A402E; font-family: "Playfair Display", serif;'>{fit_b}%</b>
                    </div>
                    <div style='background: #FEEDE4; padding: 12px; border-radius: 10px; flex: 1; border: 1.5px solid #F5BCA0;'>
                        <span style='font-size: 0.8rem; color: #9C3A10; font-weight: 800; text-transform: uppercase;'>Domestic / Import</span><br>
                        <b style='font-size: 1.4rem; color: #9C3A10; font-family: "Playfair Display", serif;'>{res_b['crop_dependency']['local_crops_used']} / {res_b['crop_dependency']['imported_crops_used']}</b>
                    </div>
                </div>
                <div style='font-weight: 800; color: #7B2D0C; font-size: 0.95rem; margin-top: 14px;'>Staple Crops in Cuisine:</div>
            """, unsafe_allow_html=True)
            tagify(res_b["crop_dependency"]["dominant_crops"][:5])

            st.markdown("<div style='font-weight: 800; color: #7B2D0C; font-size: 0.95rem; margin-top: 14px;'>Key Traditional Dishes:</div>", unsafe_allow_html=True)
            tagify(res_b["recipes"][:4], highlight=True)
            st.markdown("</div>", unsafe_allow_html=True)
