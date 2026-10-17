import requests
from functools import lru_cache

try:
    import streamlit as st
    cache_decorator = st.cache_data(ttl=3600)
except Exception:
    cache_decorator = lru_cache(maxsize=128)

def country_code_to_flag_emoji(code):
    if not code or len(code) != 2:
        return "🌍"
    return "".join(chr(127397 + ord(c.upper())) for c in code)

@cache_decorator
def fetch_country_geocoding(country_name):
    """
    Fetches latitude, longitude, country code, timezone, and population
    via Open-Meteo's open Geocoding API (free, no API key).
    Docs: https://open-meteo.com/en/docs/geocoding-api
    """
    if not country_name:
        return None
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": country_name.strip(),
        "count": 1,
        "language": "en",
        "format": "json"
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data and "results" in data and len(data["results"]) > 0:
                res = data["results"][0]
                cc = res.get("country_code", "").upper()
                return {
                    "name": res.get("name"),
                    "country_code": cc,
                    "flag": country_code_to_flag_emoji(cc),
                    "flag_url": f"https://flagcdn.com/w80/{cc.lower()}.png" if cc else None,
                    "latitude": res.get("latitude"),
                    "longitude": res.get("longitude"),
                    "timezone": res.get("timezone", "UTC"),
                    "population": res.get("population")
                }
    except Exception:
        pass
    return None

@cache_decorator
def fetch_live_weather(latitude, longitude):
    """
    Fetches current temperature, humidity, and precipitation
    via Open-Meteo's open Forecast API (free, no API key).
    Docs: https://open-meteo.com/en/docs
    """
    if latitude is None or longitude is None:
        return None
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation"
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200:
            current = resp.json().get("current", {})
            return {
                "temp_c": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "precipitation": current.get("precipitation")
            }
    except Exception:
        pass
    return None

def get_country_live_terroir(country_name):
    """
    Convenience orchestrator returning unified geographic and real-time weather metadata.
    """
    geo = fetch_country_geocoding(country_name)
    if not geo:
        return None
    weather = fetch_live_weather(geo["latitude"], geo["longitude"])
    return {
        "geo": geo,
        "weather": weather
    }
