import React, { useState, useEffect } from 'react';
import { 
  Search, Globe, Utensils, Sprout, Flame, Clock, Users, 
  ArrowRight, CloudSun, Compass, ShieldCheck, Scale, Loader2 
} from 'lucide-react';

const API_BASE = "http://localhost:8000";

export default function App() {
  const [activeTab, setActiveTab] = useState("explorer");
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [searchResult, setSearchResult] = useState(null);
  const [error, setError] = useState(null);

  // Comparison State
  const [countryList, setCountryList] = useState([]);
  const [compareA, setCompareA] = useState("Italy");
  const [compareB, setCompareB] = useState("Japan");
  const [compareData, setCompareData] = useState(null);
  const [compareLoading, setCompareLoading] = useState(false);

  // Load available countries for comparison
  useEffect(() => {
    fetch(`${API_BASE}/api/meta`)
      .then(res => res.json())
      .then(data => {
        if (data && data.countries) {
          setCountryList(data.countries);
        }
      })
      .catch(() => {});
  }, []);

  const handleSearch = async (term) => {
    const q = term || searchQuery;
    if (!q.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(q)}`);
      if (!res.ok) {
        throw new Error("No matching country or culinary dish found.");
      }
      const data = await res.json();
      setSearchResult(data);
    } catch (err) {
      setError(err.message);
      setSearchResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleCompare = async () => {
    setCompareLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/compare?country_a=${encodeURIComponent(compareA)}&country_b=${encodeURIComponent(compareB)}`);
      const data = await res.json();
      setCompareData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setCompareLoading(false);
    }
  };

  return (
    <div className="bento-container">
      {/* Top Header */}
      <header style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
        <div style={{ display: 'inline-block', marginBottom: '0.6rem' }}>
          <span className="brand-badge">
            <Sprout size={15} /> Agro-Cultural Intelligence
          </span>
        </div>
        <h1 className="font-serif" style={{ fontSize: '3rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
          Food Diversity & Cultural Analysis
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem', maxWidth: '680px', margin: '0 auto' }}>
          Mapping the convergence of global climate zones, agricultural crop yields, and traditional culinary terroirs.
        </p>

        {/* Tab Switcher */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: '12px', marginTop: '1.8rem' }}>
          <button 
            onClick={() => setActiveTab("explorer")}
            style={{
              padding: '10px 24px',
              borderRadius: '12px',
              fontWeight: 700,
              fontSize: '0.95rem',
              cursor: 'pointer',
              border: activeTab === "explorer" ? '2px solid var(--sage-main)' : '1.5px solid var(--sage-border)',
              background: activeTab === "explorer" ? '#FFFFFF' : 'var(--sage-light)',
              color: 'var(--text-primary)',
              boxShadow: activeTab === "explorer" ? '0 4px 14px rgba(26,64,46,0.1)' : 'none',
              transition: 'all 0.15s ease'
            }}
          >
            🔍 Explorer & Bento Dashboard
          </button>
          <button 
            onClick={() => {
              setActiveTab("compare");
              if (!compareData) handleCompare();
            }}
            style={{
              padding: '10px 24px',
              borderRadius: '12px',
              fontWeight: 700,
              fontSize: '0.95rem',
              cursor: 'pointer',
              border: activeTab === "compare" ? '2px solid var(--sage-main)' : '1.5px solid var(--sage-border)',
              background: activeTab === "compare" ? '#FFFFFF' : 'var(--sage-light)',
              color: 'var(--text-primary)',
              boxShadow: activeTab === "compare" ? '0 4px 14px rgba(26,64,46,0.1)' : 'none',
              transition: 'all 0.15s ease'
            }}
          >
            ⚖️ Cross-Culture Comparison
          </button>
        </div>
      </header>

      {/* ========================================================= */}
      {/* TAB 1: EXPLORER DASHBOARD */}
      {/* ========================================================= */}
      {activeTab === "explorer" && (
        <div>
          {/* Quick Suggestions & Search Bar */}
          <div style={{ marginBottom: '2rem' }}>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', alignItems: 'center', marginBottom: '0.8rem' }}>
              <span style={{ fontSize: '0.88rem', fontWeight: 800, color: 'var(--sage-main)' }}>💡 Quick Explorations:</span>
              {[
                { name: "Italy", label: "🇮🇹 Italy" },
                { name: "India", label: "🇮🇳 India" },
                { name: "Mexico", label: "🇲🇽 Mexico" },
                { name: "Japan", label: "🇯🇵 Japan" },
                { name: "Classic Margherita Pizza", label: "🍕 Pizza" },
                { name: "Spicy Kimchi Fried Rice", label: "🍲 Kimchi" }
              ].map(item => (
                <button
                  key={item.name}
                  className="chip-btn"
                  onClick={() => {
                    setSearchQuery(item.name);
                    handleSearch(item.name);
                  }}
                >
                  {item.label}
                </button>
              ))}
            </div>

            <form 
              onSubmit={(e) => {
                e.preventDefault();
                handleSearch();
              }}
              className="search-bar-wrap"
            >
              <Search 
                size={22} 
                style={{ position: 'absolute', left: '18px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} 
              />
              <input 
                type="text"
                className="search-input"
                placeholder="Search any country (e.g. Italy, India, Mexico) or dish (e.g. Pizza, Curry)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </form>
          </div>

          {loading && (
            <div style={{ textAlign: 'center', padding: '4rem 0' }}>
              <Loader2 size={36} className="animate-spin" style={{ color: 'var(--sage-main)', margin: '0 auto 1rem auto' }} />
              <p style={{ fontWeight: 700, color: 'var(--text-secondary)' }}>Analyzing agricultural & cultural terroir datasets...</p>
            </div>
          )}

          {error && (
            <div className="bento-card bento-terracotta" style={{ textAlign: 'center', padding: '2rem' }}>
              <h3 style={{ color: 'var(--terracotta-dark)', marginBottom: '0.5rem' }}>Search Notice</h3>
              <p style={{ color: '#7B2D0C' }}>{error}</p>
            </div>
          )}

          {/* EMPTY LANDING CARDS */}
          {!searchResult && !loading && !error && (
            <div className="bento-grid">
              <div className="bento-card bento-hero" style={{ gridColumn: 'span 5' }}>
                <span style={{ fontSize: '2.4rem' }}>🌍</span>
                <h3 className="card-title" style={{ marginTop: '0.6rem' }}>Country Agro-Terroir</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '1.2rem' }}>
                  Analyze national climate zones, evaluate local farming yields, and measure culinary alignment against regional terroir.
                </p>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <span className="brand-badge">192 Nations</span>
                  <span className="brand-badge brand-badge-terracotta">Live Terroir API</span>
                </div>
              </div>

              <div className="bento-card" style={{ gridColumn: 'span 4' }}>
                <span style={{ fontSize: '2.4rem' }}>🍽</span>
                <h3 className="card-title" style={{ marginTop: '0.6rem' }}>Culinary Lineage</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '1.2rem' }}>
                  Deconstruct traditional recipes back to botanical crops, ingredient dependencies, and nutritional densities.
                </p>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <span className="brand-badge">Crop Mapping</span>
                  <span className="brand-badge">Nutritional Stats</span>
                </div>
              </div>

              <div className="bento-card bento-terracotta" style={{ gridColumn: 'span 3' }}>
                <span style={{ fontSize: '2.4rem' }}>🌾</span>
                <h3 className="card-title" style={{ marginTop: '0.6rem', color: 'var(--terracotta-dark)' }}>Trade Autonomy</h3>
                <p style={{ color: '#7B2D0C', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '1.2rem' }}>
                  Measure domestic crop independence vs. trade network reliance.
                </p>
                <span className="brand-badge brand-badge-terracotta">Climate Fit Score</span>
              </div>
            </div>
          )}

          {/* RESULTS: COUNTRY BENTO DASHBOARD */}
          {searchResult && searchResult.type === "country" && (
            <div>
              {/* Hero Banner */}
              <div className="bento-card bento-hero" style={{ marginBottom: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '10px' }}>
                  <div>
                    <span className="brand-badge">National Profile</span>
                    <h1 className="font-serif" style={{ fontSize: '2.8rem', color: 'var(--text-primary)', margin: '6px 0 10px 0' }}>
                      {searchResult.terroir?.geo?.flag || "🌍"} {searchResult.terroir?.geo?.name || searchQuery}
                    </h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '1.05rem', fontWeight: 600 }}>
                      Climatic Zone: <span style={{ background: '#D5E2D7', color: 'var(--text-primary)', padding: '4px 12px', borderRadius: '8px' }}>{searchResult.data.climate}</span>
                    </p>
                  </div>
                </div>
              </div>

              {/* Live Terroir Weather Banner */}
              {searchResult.terroir?.weather && (
                <div className="weather-banner">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <CloudSun size={24} style={{ color: 'var(--terracotta-main)' }} />
                    <span style={{ fontWeight: 800, color: 'var(--terracotta-dark)' }}>Live Agricultural Terroir (Open-Meteo API):</span>
                    <span style={{ color: '#381A0B', fontWeight: 600 }}>
                      Temp: <b style={{ color: 'var(--terracotta-dark)' }}>{searchResult.terroir.weather.temp_c}°C</b> | 
                      Humidity: <b style={{ color: 'var(--terracotta-dark)' }}>{searchResult.terroir.weather.humidity}%</b> | 
                      Precipitation: <b style={{ color: 'var(--terracotta-dark)' }}>{searchResult.terroir.weather.precipitation} mm</b>
                    </span>
                  </div>
                  <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--terracotta-dark)' }}>
                    📍 {searchResult.terroir.geo?.timezone || "Local"}
                  </span>
                </div>
              )}

              {/* 3 KPI Cards */}
              <div className="bento-grid" style={{ marginBottom: '1.25rem' }}>
                <div className="bento-card" style={{ gridColumn: 'span 4', textAlign: 'center' }}>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.88rem', fontWeight: 800, textTransform: 'uppercase' }}>Domestic Crops</div>
                  <div className="font-serif" style={{ fontSize: '2.8rem', fontWeight: 800, color: 'var(--sage-main)', margin: '4px 0' }}>
                    {searchResult.data.crop_dependency.local_crops_used}
                  </div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.82rem', fontWeight: 600 }}>Produced locally within domestic territory</div>
                </div>

                <div className="bento-card bento-terracotta" style={{ gridColumn: 'span 4', textAlign: 'center' }}>
                  <div style={{ color: 'var(--terracotta-dark)', fontSize: '0.88rem', fontWeight: 800, textTransform: 'uppercase' }}>Imported Crops</div>
                  <div className="font-serif" style={{ fontSize: '2.8rem', fontWeight: 800, color: 'var(--terracotta-dark)', margin: '4px 0' }}>
                    {searchResult.data.crop_dependency.imported_crops_used}
                  </div>
                  <div style={{ color: '#7B2D0C', fontSize: '0.82rem', fontWeight: 600 }}>Historically sourced via international trade</div>
                </div>

                <div className="bento-card" style={{ gridColumn: 'span 4', textAlign: 'center' }}>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.88rem', fontWeight: 800, textTransform: 'uppercase' }}>Climate Alignment</div>
                  <div className="font-serif" style={{ fontSize: '2.8rem', fontWeight: 800, color: 'var(--sage-main)', margin: '4px 0' }}>
                    {Math.round(searchResult.data.climate_alignment.alignment_score * 100)}%
                  </div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.82rem', fontWeight: 600 }}>Cuisine compatibility with regional climate</div>
                </div>
              </div>

              {/* Middle Row: Cultural Narrative & Signature Dishes */}
              <div className="bento-grid" style={{ marginBottom: '1.25rem' }}>
                <div className="bento-card" style={{ gridColumn: 'span 7' }}>
                  <h3 className="card-title">✨ Cultural Terroir & Agrarian Narrative</h3>
                  <p style={{ color: 'var(--text-primary)', fontSize: '1.02rem', lineHeight: 1.8, fontWeight: 500 }}>
                    {searchResult.data.analysis_summary}
                  </p>
                </div>

                <div className="bento-card bento-terracotta" style={{ gridColumn: 'span 5' }}>
                  <h3 className="card-title" style={{ color: 'var(--terracotta-dark)' }}>🍲 Signature Traditional Recipes</h3>
                  <div>
                    {searchResult.data.recipes.map(recipe => (
                      <span key={recipe} className="tag-pill tag-terracotta">{recipe}</span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Bottom Row: Climate-Aligned Crops vs Recipe Crops */}
              <div className="bento-grid">
                <div className="bento-card" style={{ gridColumn: 'span 6' }}>
                  <h3 className="card-title">🌱 Climate-Aligned Native Crops</h3>
                  <div>
                    {searchResult.data.suitable_crops.slice(0, 16).map(crop => (
                      <span key={crop} className="tag-pill">{crop}</span>
                    ))}
                  </div>
                </div>

                <div className="bento-card" style={{ gridColumn: 'span 6' }}>
                  <h3 className="card-title">🌾 Key Crops Sourced in Cuisine</h3>
                  <div>
                    {searchResult.data.crop_dependency.dominant_crops.map(crop => (
                      <span key={crop} className="tag-pill tag-terracotta">{crop}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* RESULTS: RECIPE BENTO DASHBOARD */}
          {searchResult && searchResult.type === "recipe" && (
            <div>
              <div className="bento-card bento-hero" style={{ marginBottom: '1.25rem' }}>
                <span className="brand-badge brand-badge-terracotta">Culinary Dish Profile</span>
                <h1 className="font-serif" style={{ fontSize: '2.8rem', color: 'var(--text-primary)', margin: '6px 0 10px 0' }}>
                  🍽 {searchResult.query.toUpperCase()}
                </h1>
              </div>

              {/* Recipe Metrics */}
              <div className="bento-grid" style={{ marginBottom: '1.25rem' }}>
                <div className="bento-card" style={{ gridColumn: 'span 3', textAlign: 'center' }}>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontWeight: 800 }}>🔥 CALORIES</div>
                  <div className="font-serif" style={{ fontSize: '2.4rem', fontWeight: 800, color: 'var(--sage-main)' }}>
                    {searchResult.data.calories ? `${searchResult.data.calories} kcal` : "N/A"}
                  </div>
                </div>
                <div className="bento-card" style={{ gridColumn: 'span 3', textAlign: 'center' }}>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontWeight: 800 }}>⏱ PREP TIME</div>
                  <div className="font-serif" style={{ fontSize: '2.4rem', fontWeight: 800, color: 'var(--sage-main)' }}>
                    {searchResult.data.prep_time ? `${searchResult.data.prep_time}m` : "N/A"}
                  </div>
                </div>
                <div className="bento-card" style={{ gridColumn: 'span 3', textAlign: 'center' }}>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontWeight: 800 }}>🍳 COOK TIME</div>
                  <div className="font-serif" style={{ fontSize: '2.4rem', fontWeight: 800, color: 'var(--sage-main)' }}>
                    {searchResult.data.cook_time ? `${searchResult.data.cook_time}m` : "N/A"}
                  </div>
                </div>
                <div className="bento-card" style={{ gridColumn: 'span 3', textAlign: 'center' }}>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontWeight: 800 }}>👥 SERVINGS</div>
                  <div className="font-serif" style={{ fontSize: '2.4rem', fontWeight: 800, color: 'var(--sage-main)' }}>
                    {searchResult.data.servings || "N/A"}
                  </div>
                </div>
              </div>

              {/* Dietary Tags */}
              {searchResult.data.dietary && searchResult.data.dietary.length > 0 && (
                <div style={{ marginBottom: '1.25rem' }}>
                  {searchResult.data.dietary.map(d => (
                    <span key={d} className="brand-badge brand-badge-terracotta" style={{ marginRight: '8px' }}>
                      🌱 {d.toUpperCase()}
                    </span>
                  ))}
                </div>
              )}

              {/* Ingredients & Crops Breakdown */}
              <div className="bento-grid">
                <div className="bento-card" style={{ gridColumn: 'span 6' }}>
                  <h3 className="card-title">🛒 Ingredients Breakdown</h3>
                  <div>
                    {searchResult.data.ingredients.map(ing => (
                      <span key={ing} className="tag-pill">{ing}</span>
                    ))}
                  </div>
                </div>

                <div className="bento-card bento-terracotta" style={{ gridColumn: 'span 6' }}>
                  <h3 className="card-title" style={{ color: 'var(--terracotta-dark)' }}>🌾 Botanical Crops Sourced</h3>
                  <div>
                    {searchResult.data.crops.map(crop => (
                      <span key={crop} className="tag-pill tag-terracotta">{crop}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ========================================================= */}
      {/* TAB 2: CROSS-CULTURE COMPARISON */}
      {/* ========================================================= */}
      {activeTab === "compare" && (
        <div>
          <div className="bento-card bento-hero" style={{ marginBottom: '1.5rem' }}>
            <h2 className="card-title" style={{ fontSize: '1.5rem' }}>⚖️ Cross-Culture Bento Comparison</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '1rem', margin: 0 }}>
              Compare agricultural autonomy, climatic compatibility, and staple food traditions between two global cultures.
            </p>

            <div style={{ display: 'flex', gap: '16px', alignItems: 'center', marginTop: '1.5rem', flexWrap: 'wrap' }}>
              <div style={{ flex: 1, minWidth: '220px' }}>
                <label style={{ display: 'block', fontWeight: 800, color: 'var(--sage-main)', marginBottom: '6px' }}>Culture A:</label>
                <select 
                  value={compareA} 
                  onChange={(e) => setCompareA(e.target.value)}
                  style={{ width: '100%', padding: '12px 16px', borderRadius: '12px', border: '1.5px solid var(--sage-border)', fontSize: '1rem', fontWeight: 600 }}
                >
                  {countryList.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>

              <div style={{ flex: 1, minWidth: '220px' }}>
                <label style={{ display: 'block', fontWeight: 800, color: 'var(--terracotta-dark)', marginBottom: '6px' }}>Culture B:</label>
                <select 
                  value={compareB} 
                  onChange={(e) => setCompareB(e.target.value)}
                  style={{ width: '100%', padding: '12px 16px', borderRadius: '12px', border: '1.5px solid var(--terracotta-border)', fontSize: '1rem', fontWeight: 600 }}
                >
                  {countryList.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>

              <div style={{ marginTop: '22px' }}>
                <button 
                  onClick={handleCompare}
                  style={{
                    padding: '12px 28px',
                    borderRadius: '12px',
                    background: 'var(--sage-main)',
                    color: '#FFFFFF',
                    fontWeight: 800,
                    fontSize: '1rem',
                    border: 'none',
                    cursor: 'pointer',
                    boxShadow: '0 4px 12px rgba(26,64,46,0.18)'
                  }}
                >
                  {compareLoading ? "Comparing..." : "Generate Comparison"}
                </button>
              </div>
            </div>
          </div>

          {compareData && (
            <div className="bento-grid">
              {/* Country A */}
              <div className="bento-card" style={{ gridColumn: 'span 6' }}>
                <h2 className="font-serif" style={{ fontSize: '2.2rem', color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
                  {compareData.country_a.terroir?.geo?.flag || "🌍"} {compareData.country_a.name}
                </h2>
                <p style={{ color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '1rem' }}>
                  Climate Zone: <b>{compareData.country_a.data.climate}</b>
                </p>

                <div style={{ display: 'flex', gap: '12px', marginBottom: '1.2rem' }}>
                  <div style={{ flex: 1, background: 'var(--sage-light)', padding: '12px', borderRadius: '12px', textAlign: 'center' }}>
                    <div style={{ fontSize: '0.8rem', fontWeight: 800, color: 'var(--sage-main)' }}>FIT SCORE</div>
                    <div className="font-serif" style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--sage-main)' }}>
                      {Math.round(compareData.country_a.data.climate_alignment.alignment_score * 100)}%
                    </div>
                  </div>
                  <div style={{ flex: 1, background: 'var(--terracotta-light)', padding: '12px', borderRadius: '12px', textAlign: 'center' }}>
                    <div style={{ fontSize: '0.8rem', fontWeight: 800, color: 'var(--terracotta-dark)' }}>DOMESTIC / IMPORT</div>
                    <div className="font-serif" style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--terracotta-dark)' }}>
                      {compareData.country_a.data.crop_dependency.local_crops_used} / {compareData.country_a.data.crop_dependency.imported_crops_used}
                    </div>
                  </div>
                </div>

                <div style={{ fontWeight: 800, color: 'var(--text-primary)', marginBottom: '6px' }}>Staple Crops in Cuisine:</div>
                <div style={{ marginBottom: '1rem' }}>
                  {compareData.country_a.data.crop_dependency.dominant_crops.slice(0, 5).map(c => (
                    <span key={c} className="tag-pill">{c}</span>
                  ))}
                </div>

                <div style={{ fontWeight: 800, color: 'var(--text-primary)', marginBottom: '6px' }}>Signature Traditional Dishes:</div>
                <div>
                  {compareData.country_a.data.recipes.slice(0, 5).map(r => (
                    <span key={r} className="tag-pill tag-terracotta">{r}</span>
                  ))}
                </div>
              </div>

              {/* Country B */}
              <div className="bento-card bento-terracotta" style={{ gridColumn: 'span 6' }}>
                <h2 className="font-serif" style={{ fontSize: '2.2rem', color: 'var(--terracotta-dark)', marginBottom: '0.4rem' }}>
                  {compareData.country_b.terroir?.geo?.flag || "🌍"} {compareData.country_b.name}
                </h2>
                <p style={{ color: '#9C3A10', fontWeight: 600, marginBottom: '1rem' }}>
                  Climate Zone: <b>{compareData.country_b.data.climate}</b>
                </p>

                <div style={{ display: 'flex', gap: '12px', marginBottom: '1.2rem' }}>
                  <div style={{ flex: 1, background: '#FFFFFF', padding: '12px', borderRadius: '12px', textAlign: 'center', border: '1.5px solid var(--terracotta-border)' }}>
                    <div style={{ fontSize: '0.8rem', fontWeight: 800, color: 'var(--sage-main)' }}>FIT SCORE</div>
                    <div className="font-serif" style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--sage-main)' }}>
                      {Math.round(compareData.country_b.data.climate_alignment.alignment_score * 100)}%
                    </div>
                  </div>
                  <div style={{ flex: 1, background: 'var(--terracotta-light)', padding: '12px', borderRadius: '12px', textAlign: 'center', border: '1.5px solid var(--terracotta-border)' }}>
                    <div style={{ fontSize: '0.8rem', fontWeight: 800, color: 'var(--terracotta-dark)' }}>DOMESTIC / IMPORT</div>
                    <div className="font-serif" style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--terracotta-dark)' }}>
                      {compareData.country_b.data.crop_dependency.local_crops_used} / {compareData.country_b.data.crop_dependency.imported_crops_used}
                    </div>
                  </div>
                </div>

                <div style={{ fontWeight: 800, color: 'var(--terracotta-dark)', marginBottom: '6px' }}>Staple Crops in Cuisine:</div>
                <div style={{ marginBottom: '1rem' }}>
                  {compareData.country_b.data.crop_dependency.dominant_crops.slice(0, 5).map(c => (
                    <span key={c} className="tag-pill">{c}</span>
                  ))}
                </div>

                <div style={{ fontWeight: 800, color: 'var(--terracotta-dark)', marginBottom: '6px' }}>Signature Traditional Dishes:</div>
                <div>
                  {compareData.country_b.data.recipes.slice(0, 5).map(r => (
                    <span key={r} className="tag-pill tag-terracotta">{r}</span>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
