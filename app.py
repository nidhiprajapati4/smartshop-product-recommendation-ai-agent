
import html
import re
import streamlit as st

st.set_page_config(
    page_title="SmartShop AI",
    page_icon="🛍️",
    layout="wide",
)

PRODUCTS = [
    {"name": "SoundBeat Pro", "category": "Headphones",
     "price": 3999, "rating": 4.6,
     "features": ["wireless", "noise cancellation", "travel", "music"],
     "description": "Wireless headphones for travel and daily listening.",
     "pros": "Comfortable, wireless, travel-friendly"},
    {"name": "CallClear Lite", "category": "Headphones",
     "price": 2499, "rating": 4.4,
     "features": ["wireless", "microphone", "office", "calls"],
     "description": "Lightweight headset designed for office calls.",
     "pros": "Affordable, lightweight, call-focused"},
    {"name": "BassMax X", "category": "Headphones",
     "price": 4499, "rating": 4.7,
     "features": ["wireless", "bass", "music", "travel"],
     "description": "Wireless headphones with a bass-focused sound profile.",
     "pros": "Strong bass, high sample rating"},
    {"name": "WorkMate Keyboard", "category": "Accessories",
     "price": 1899, "rating": 4.5,
     "features": ["office", "typing", "wireless", "productivity"],
     "description": "Wireless keyboard for a home or office workspace.",
     "pros": "Compact, practical, productivity-focused"},
    {"name": "FitTrack Watch", "category": "Wearables",
     "price": 3499, "rating": 4.3,
     "features": ["fitness", "health tracking", "travel", "wireless"],
     "description": "Smartwatch-style wearable for everyday activity tracking.",
     "pros": "Activity tracking, everyday use"},
    {"name": "PocketBuds Air", "category": "Headphones",
     "price": 1799, "rating": 4.2,
     "features": ["wireless", "portable", "travel", "music"],
     "description": "Compact wireless earbuds for commuting.",
     "pros": "Portable, low-cost, easy to carry"},
    {"name": "VisionView Monitor", "category": "Accessories",
     "price": 7999, "rating": 4.6,
     "features": ["office", "productivity", "display", "work"],
     "description": "External monitor for a desk-based work setup.",
     "pros": "Larger workspace, productivity-focused"},
    {"name": "PowerGo Bank", "category": "Accessories",
     "price": 1299, "rating": 4.4,
     "features": ["travel", "portable", "battery", "charging"],
     "description": "Portable power bank for charging on the go.",
     "pros": "Portable, budget-friendly"},
    {"name": "StudyTone Headset", "category": "Headphones",
     "price": 2999, "rating": 4.5,
     "features": ["wireless", "microphone", "study", "office", "calls"],
     "description": "Wireless headset for online classes and meetings.",
     "pros": "Versatile for study and meetings"},
    {"name": "MoveFit Buds", "category": "Headphones",
     "price": 2799, "rating": 4.4,
     "features": ["wireless", "fitness", "portable", "travel", "music"],
     "description": "Compact earbuds for workouts and commuting.",
     "pros": "Portable, suited to active use"},
]


def recommend_products(query, budget, category, min_rating, top_n=3):
    query_words = set(re.findall(r"[a-z]+", query.lower()))
    scored = []

    for p in PRODUCTS:
        if p["price"] > budget or p["rating"] < min_rating:
            continue
        if category != "All" and p["category"] != category:
            continue

        feature_words = set(" ".join(p["features"]).split())
        name_words = set(re.findall(r"[a-z]+", p["name"].lower()))
        description_words = set(
            re.findall(r"[a-z]+", p["description"].lower())
        )
        matched = query_words & (
            feature_words | name_words | description_words
        )

        # Transparent heuristic: feature overlap + rating + affordability.
        relevance = min(len(matched) / 4, 1.0) * 70
        rating_score = p["rating"] / 5 * 20
        budget_score = (1 - p["price"] / budget) * 10
        score = relevance + rating_score + budget_score

        scored.append({
            **p,
            "score": round(score, 1),
            "matched": sorted(matched),
        })

    return sorted(
        scored,
        key=lambda p: (p["score"], p["rating"]),
        reverse=True,
    )[:top_n]


CATEGORY_STYLE = {
    "Headphones": {"icon": "🎧", "gradient": "#6366f1, #a855f7"},
    "Accessories": {"icon": "⌨️", "gradient": "#0ea5e9, #6366f1"},
    "Wearables": {"icon": "⌚", "gradient": "#10b981, #0ea5e9"},
}

STOP_WORDS = {"a", "an", "and", "for", "the", "to", "of", "with", "in", "on", "my"}

QUICK_SEARCHES = [
    "wireless headphones for office calls and travel",
    "fitness earbuds for workouts",
    "productivity setup for working from home",
    "portable gadgets for travel",
]

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp, .stApp input, .stApp button {
    font-family: 'Inter', sans-serif;
}
.block-container { padding-top: 2rem; max-width: 1200px; }
#MainMenu, footer { visibility: hidden; }
/* Hide the top-right toolbar (Share, star, GitHub, edit, menu) but keep
   the sidebar expand control usable. */
[data-testid="stToolbarActions"],
[data-testid="stAppDeployButton"],
[data-testid="stMainMenu"],
[data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent; }

.hero {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #db2777 100%);
    border-radius: 24px;
    padding: 2.6rem 2.4rem;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 45px -20px rgba(79, 70, 229, .6);
    margin-bottom: 1.6rem;
}
.hero::after {
    content: "";
    position: absolute;
    width: 340px; height: 340px;
    right: -90px; top: -120px;
    background: radial-gradient(circle, rgba(255,255,255,.28), transparent 65%);
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,.18);
    border: 1px solid rgba(255,255,255,.35);
    padding: .3rem .8rem;
    border-radius: 999px;
    font-size: .8rem;
    font-weight: 600;
    letter-spacing: .02em;
}
.hero h1 {
    color: #fff;
    font-size: 2.6rem;
    font-weight: 800;
    margin: .8rem 0 .4rem;
    padding: 0;
    line-height: 1.15;
}
.hero p { font-size: 1.08rem; opacity: .92; margin: 0; max-width: 640px; }

.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 0 0 1.6rem; }
.stat {
    background: var(--secondary-background-color);
    border: 1px solid rgba(128,128,128,.18);
    border-radius: 16px;
    padding: 1rem 1.2rem;
}
.stat-value { font-size: 1.5rem; font-weight: 800; }
.stat-label { font-size: .8rem; opacity: .65; text-transform: uppercase; letter-spacing: .05em; }

.section-title { font-size: 1.35rem; font-weight: 700; margin: 1.6rem 0 .2rem; }
.section-sub { opacity: .65; margin-bottom: 1rem; font-size: .92rem; }

.card {
    background: var(--background-color);
    border: 1px solid rgba(128,128,128,.2);
    border-radius: 20px;
    overflow: hidden;
    height: 100%;
    transition: transform .2s ease, box-shadow .2s ease;
    box-shadow: 0 4px 18px -10px rgba(15, 23, 42, .25);
}
.card:hover { transform: translateY(-4px); box-shadow: 0 16px 34px -14px rgba(79, 70, 229, .45); }
.card-visual {
    height: 120px;
    display: flex; align-items: center; justify-content: center;
    font-size: 3.4rem;
    position: relative;
}
.rank {
    position: absolute; top: 12px; left: 12px;
    background: rgba(255,255,255,.92); color: #312e81;
    font-weight: 800; font-size: .78rem;
    padding: .25rem .65rem; border-radius: 999px;
}
.best { position: absolute; top: 12px; right: 12px; background: #facc15; color: #422006;
    font-weight: 700; font-size: .72rem; padding: .25rem .6rem; border-radius: 999px; }
.card-body { padding: 1.1rem 1.25rem 1.3rem; }
.card-cat { font-size: .72rem; font-weight: 700; color: #7c3aed; text-transform: uppercase; letter-spacing: .06em; }
.card-name { font-size: 1.2rem; font-weight: 700; margin: .2rem 0 .35rem; }
.card-meta { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: .6rem; }
.price { font-size: 1.35rem; font-weight: 800; }
.stars { color: #f59e0b; font-size: .9rem; font-weight: 600; }
.card-desc { font-size: .9rem; opacity: .78; min-height: 2.6rem; }
.score-label { display: flex; justify-content: space-between; font-size: .8rem; font-weight: 600; margin: .9rem 0 .3rem; }
.score-track { background: rgba(128,128,128,.18); border-radius: 999px; height: 8px; overflow: hidden; }
.score-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #6366f1, #db2777); }
.why { font-size: .85rem; margin-top: .9rem; }
.chips { margin-top: .55rem; display: flex; flex-wrap: wrap; gap: .35rem; }
.chip { font-size: .74rem; font-weight: 600; padding: .2rem .6rem; border-radius: 999px;
    background: rgba(99,102,241,.12); color: #6366f1; border: 1px solid rgba(99,102,241,.25); }
.chip.muted { background: rgba(128,128,128,.12); color: inherit; opacity: .7; border-color: transparent; }

.empty {
    text-align: center; padding: 2.4rem 1rem; border-radius: 20px;
    border: 2px dashed rgba(128,128,128,.3);
}
.empty-icon { font-size: 2.6rem; }

.step-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.step { border-radius: 16px; padding: 1rem; background: var(--secondary-background-color); }
.step-num { width: 28px; height: 28px; border-radius: 50%; background: #6366f1; color: #fff;
    display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .85rem; }
.step h4 { margin: .6rem 0 .2rem; font-size: 1rem; padding: 0; }
.step p { font-size: .84rem; opacity: .75; margin: 0; }

.footer { text-align: center; opacity: .55; font-size: .82rem; margin-top: 2.4rem; }

div[data-testid="stButton"] button {
    border-radius: 999px;
    font-weight: 600;
}
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    border: none;
    box-shadow: 0 8px 20px -10px rgba(79, 70, 229, .8);
}
section[data-testid="stSidebar"] h2 { font-size: 1.1rem; }

@media (max-width: 900px) {
    .stat-row, .step-grid { grid-template-columns: repeat(2, 1fr); }
    .hero h1 { font-size: 2rem; }
}
</style>
"""


def stars(rating):
    full = int(rating)
    return "★" * full + "☆" * (5 - full)


def product_card(p, rank):
    style = CATEGORY_STYLE.get(
        p["category"], {"icon": "🛒", "gradient": "#6366f1, #a855f7"}
    )
    terms = [t for t in p["matched"] if t not in STOP_WORDS]
    if terms:
        chips = "".join(
            f'<span class="chip">{html.escape(term)}</span>'
            for term in terms
        )
    else:
        chips = '<span class="chip muted">No direct keyword overlap</span>'
    best = '<span class="best">Top pick</span>' if rank == 1 else ""
    return f"""
<div class="card">
  <div class="card-visual" style="background: linear-gradient(135deg, {style['gradient']});">
    <span class="rank">#{rank}</span>{best}{style['icon']}
  </div>
  <div class="card-body">
    <div class="card-cat">{p['category']}</div>
    <div class="card-name">{p['name']}</div>
    <div class="card-meta">
      <span class="price">₹{p['price']:,}</span>
      <span class="stars">{stars(p['rating'])} {p['rating']}</span>
    </div>
    <div class="card-desc">{p['description']}</div>
    <div class="score-label"><span>Match score</span><span>{p['score']} / 100</span></div>
    <div class="score-track"><div class="score-fill" style="width:{min(p['score'], 100)}%"></div></div>
    <div class="why"><b>Why it matched:</b> {p['pros']}</div>
    <div class="chips">{chips}</div>
  </div>
</div>
"""


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "query" not in st.session_state:
    st.session_state["query"] = QUICK_SEARCHES[0]

st.markdown("""
<div class="hero">
  <span class="hero-badge">✨ Explainable recommendation engine</span>
  <h1>Find the right product,<br>not just any product.</h1>
  <p>Tell SmartShop what you need in plain English. It filters by your
  budget and standards, then ranks every match with a transparent score.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎯 Your preferences")
    category = st.selectbox(
        "Product category",
        ["All", "Headphones", "Accessories", "Wearables"],
    )
    budget = st.slider(
        "Maximum budget (₹)", 1000, 10000, 5000, step=500
    )
    min_rating = st.slider(
        "Minimum rating", 3.0, 5.0, 4.0, step=0.1
    )
    top_n = st.segmented_control(
        "Recommendations", [3, 5], default=3
    ) or 3
    st.divider()
    st.caption(
        "Sample catalog of 10 products. Prices and ratings are "
        "illustrative, not live retail offers."
    )

st.markdown(
    '<div class="section-title">What are you shopping for?</div>',
    unsafe_allow_html=True,
)
search_col, button_col = st.columns([5, 1], vertical_alignment="bottom")
with search_col:
    query = st.text_input(
        "Describe your needs",
        key="query",
        placeholder="e.g. fitness earbuds under ₹3000",
        label_visibility="collapsed",
    )
with button_col:
    st.button("Search", type="primary", use_container_width=True)


def use_quick_search(text):
    st.session_state["query"] = text


st.caption("Try a quick search")
chip_cols = st.columns(len(QUICK_SEARCHES))
for col, text in zip(chip_cols, QUICK_SEARCHES):
    col.button(
        text.capitalize(),
        key=f"quick_{text}",
        on_click=use_quick_search,
        args=(text,),
        use_container_width=True,
    )

results = recommend_products(query, budget, category, min_rating, top_n)

in_budget = [
    p for p in PRODUCTS
    if p["price"] <= budget and p["rating"] >= min_rating
    and (category == "All" or p["category"] == category)
]
best_score = f"{results[0]['score']}" if results else "–"
avg_price = (
    f"₹{sum(p['price'] for p in results) // len(results):,}"
    if results else "–"
)
st.markdown(f"""
<div class="stat-row" style="margin-top:1.4rem">
  <div class="stat"><div class="stat-value">{len(PRODUCTS)}</div><div class="stat-label">Products scanned</div></div>
  <div class="stat"><div class="stat-value">{len(in_budget)}</div><div class="stat-label">Pass your filters</div></div>
  <div class="stat"><div class="stat-value">{best_score}</div><div class="stat-label">Best match score</div></div>
  <div class="stat"><div class="stat-value">{avg_price}</div><div class="stat-label">Avg. shortlist price</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Your recommendations</div>'
    f'<div class="section-sub">Ranked for “{html.escape(query)}” '
    f'within ₹{budget:,}</div>',
    unsafe_allow_html=True,
)

if not results:
    st.markdown("""
<div class="empty">
  <div class="empty-icon">🔍</div>
  <h4>No products match these preferences</h4>
  <p>Try increasing your budget, lowering the minimum rating,
  or choosing “All” categories.</p>
</div>
""", unsafe_allow_html=True)
else:
    per_row = 3
    for start in range(0, len(results), per_row):
        row = results[start:start + per_row]
        cols = st.columns(per_row)
        for offset, p in enumerate(row):
            with cols[offset]:
                st.markdown(
                    product_card(p, start + offset + 1),
                    unsafe_allow_html=True,
                )
        st.write("")

    st.markdown(
        '<div class="section-title">Compare your shortlist</div>'
        '<div class="section-sub">Side by side on the factors '
        'that drive the ranking.</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(
        [
            {
                "Product": p["name"],
                "Category": p["category"],
                "Price": p["price"],
                "Rating": p["rating"],
                "Match score": p["score"],
            }
            for p in results
        ],
        column_config={
            "Price": st.column_config.NumberColumn(format="₹%d"),
            "Rating": st.column_config.NumberColumn(format="%.1f ⭐"),
            "Match score": st.column_config.ProgressColumn(
                min_value=0, max_value=100, format="%.1f"
            ),
        },
        use_container_width=True,
        hide_index=True,
    )

st.markdown(
    '<div class="section-title">How the engine works</div>'
    '<div class="section-sub">A transparent baseline recommender. '
    'The score is a heuristic, not a purchase probability.</div>',
    unsafe_allow_html=True,
)
st.markdown("""
<div class="step-grid">
  <div class="step"><div class="step-num">1</div><h4>Filter</h4>
    <p>Drop products above budget, below the minimum rating, or outside the category.</p></div>
  <div class="step"><div class="step-num">2</div><h4>Match</h4>
    <p>Compare words in your request with product names, features, and descriptions.</p></div>
  <div class="step"><div class="step-num">3</div><h4>Rank</h4>
    <p>Combine relevance (70%), rating (20%), and affordability (10%).</p></div>
  <div class="step"><div class="step-num">4</div><h4>Explain</h4>
    <p>Show the matched terms and why each product made the list.</p></div>
</div>
<div class="footer">SmartShop AI · Portfolio project · Python · Streamlit · Explainable ranking</div>
""", unsafe_allow_html=True)
