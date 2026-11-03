
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
    "Headphones": {"icon": "🎧", "tint": "#eef2ff"},
    "Accessories": {"icon": "⌨️", "tint": "#ecfeff"},
    "Wearables": {"icon": "⌚", "tint": "#ecfdf5"},
}

STOP_WORDS = {"a", "an", "and", "for", "the", "to", "of", "with", "in", "on", "my"}

QUICK_SEARCHES = [
    "headphones for office calls",
    "fitness earbuds",
    "work from home setup",
    "travel gadgets",
]

GITHUB_URL = (
    "https://github.com/nidhiprajapati4/"
    "smartshop-product-recommendation-ai-agent"
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp, .stApp input, .stApp button, .stApp label { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1080px; }
#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"],
[data-testid="stToolbarActions"],
[data-testid="stAppDeployButton"],
[data-testid="stMainMenu"],
[data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent; height: 0; }

/* Nav */
.nav { display: flex; justify-content: space-between; align-items: center; padding: .4rem 0 2.2rem; }
.logo { font-weight: 800; font-size: 1.15rem; letter-spacing: -.01em; display: flex; align-items: center; gap: .5rem; }
.logo-mark { width: 30px; height: 30px; border-radius: 9px; display: inline-flex; align-items: center;
    justify-content: center; background: linear-gradient(135deg, #6366f1, #a855f7); color: #fff; font-size: .95rem; }
.nav a { color: inherit !important; text-decoration: none; font-size: .88rem; font-weight: 600;
    padding: .45rem .9rem; border: 1px solid rgba(128,128,128,.25); border-radius: 999px; }
.nav a:hover { border-color: #6366f1; color: #6366f1 !important; }

/* Hero */
.hero { text-align: center; margin-bottom: 1.6rem; }
.hero h1 { font-size: 3rem; font-weight: 800; letter-spacing: -.035em; line-height: 1.08; margin: 0 0 .7rem; padding: 0; }
.grad { background: linear-gradient(90deg, #6366f1, #a855f7 60%, #ec4899);
    -webkit-background-clip: text; background-clip: text; color: transparent; }
.hero p { font-size: 1.1rem; opacity: .65; margin: 0; }

/* Search */
[data-testid="stTextInputRootElement"] { height: 3.1rem; border-radius: 14px; }
div[data-testid="stTextInput"] input { font-size: 1rem; padding-left: 1.1rem; }
div[data-testid="stButton"] button { border-radius: 999px; font-weight: 600; }
div[data-testid="stButton"] button[kind="primary"] {
    height: 3.1rem; border-radius: 14px; border: none;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    box-shadow: 0 10px 24px -12px rgba(99,102,241,.9);
}
div[data-testid="stButton"] button[kind="secondary"] {
    font-size: .82rem; min-height: 2.1rem; padding: .2rem .8rem;
    background: transparent; border: 1px solid rgba(128,128,128,.25);
}
div[data-testid="stButton"] button[kind="secondary"]:hover { border-color: #6366f1; color: #6366f1; }

/* Filters */
div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 18px; }

/* Results header */
.results-head { display: flex; justify-content: space-between; align-items: baseline;
    margin: 1.8rem 0 .9rem; gap: 1rem; flex-wrap: wrap; }
.results-head h3 { font-size: 1.3rem; font-weight: 700; margin: 0; padding: 0; }
.results-meta { font-size: .85rem; opacity: .6; }

/* Cards */
.card { border: 1px solid rgba(128,128,128,.2); border-radius: 18px; padding: 1.1rem;
    height: 100%; background: var(--background-color);
    transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease; }
.card:hover { transform: translateY(-3px); border-color: rgba(99,102,241,.5);
    box-shadow: 0 18px 36px -20px rgba(99,102,241,.55); }
.card.top { border-color: rgba(99,102,241,.55); box-shadow: 0 0 0 3px rgba(99,102,241,.12); }
.card-top { display: flex; justify-content: space-between; align-items: flex-start; }
.icon { width: 54px; height: 54px; border-radius: 14px; display: flex; align-items: center;
    justify-content: center; font-size: 1.7rem; }
.badge { font-size: .72rem; font-weight: 700; padding: .25rem .6rem; border-radius: 999px;
    background: rgba(128,128,128,.12); }
.badge.best { background: linear-gradient(90deg, #6366f1, #a855f7); color: #fff; }
.card-cat { font-size: .72rem; font-weight: 700; color: #6366f1; text-transform: uppercase;
    letter-spacing: .07em; margin-top: 1rem; }
.card-name { font-size: 1.15rem; font-weight: 700; margin: .15rem 0 .2rem; }
.card-desc { font-size: .88rem; opacity: .65; min-height: 2.5rem; margin-bottom: .8rem; }
.card-meta { display: flex; justify-content: space-between; align-items: center; }
.price { font-size: 1.3rem; font-weight: 800; }
.rating { font-size: .85rem; font-weight: 600; }
.rating span { color: #f59e0b; }
.score { margin-top: .9rem; }
.score-label { display: flex; justify-content: space-between; font-size: .78rem;
    font-weight: 600; opacity: .8; margin-bottom: .3rem; }
.score-track { background: rgba(128,128,128,.16); border-radius: 999px; height: 6px; overflow: hidden; }
.score-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #6366f1, #ec4899); }
.chips { margin-top: .8rem; display: flex; flex-wrap: wrap; gap: .3rem; }
.chip { font-size: .72rem; font-weight: 600; padding: .18rem .55rem; border-radius: 999px;
    background: rgba(99,102,241,.1); color: #6366f1; }
.chip.muted { background: rgba(128,128,128,.12); color: inherit; opacity: .6; }

.empty { text-align: center; padding: 2.6rem 1rem; border-radius: 18px;
    border: 1.5px dashed rgba(128,128,128,.3); }
.empty div { font-size: 2.2rem; }
.empty p { opacity: .6; margin: .3rem 0 0; }

/* Footer */
.foot { margin-top: 2.6rem; padding-top: 1.4rem; border-top: 1px solid rgba(128,128,128,.18);
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: .8rem;
    font-size: .82rem; }
.pills { display: flex; gap: .4rem; flex-wrap: wrap; }
.pill { padding: .25rem .7rem; border-radius: 999px; background: rgba(99,102,241,.08); color: #4f46e5;
    font-weight: 600; opacity: .85; }
.foot a { color: inherit !important; opacity: .7; }

@media (max-width: 700px) {
    .hero h1 { font-size: 2.1rem; }
}
</style>
"""


def product_card(p, rank):
    style = CATEGORY_STYLE.get(p["category"], {"icon": "🛒", "tint": "#eef2ff"})
    terms = [t for t in p["matched"] if t not in STOP_WORDS]
    chips = "".join(
        f'<span class="chip">{html.escape(t)}</span>' for t in terms
    ) or '<span class="chip muted">no keyword match</span>'
    badge = (
        '<span class="badge best">Best match</span>' if rank == 1
        else f'<span class="badge">#{rank}</span>'
    )
    return f"""
<div class="card{' top' if rank == 1 else ''}">
  <div class="card-top">
    <div class="icon" style="background:{style['tint']}">{style['icon']}</div>{badge}
  </div>
  <div class="card-cat">{p['category']}</div>
  <div class="card-name">{p['name']}</div>
  <div class="card-desc">{p['description']}</div>
  <div class="card-meta">
    <span class="price">₹{p['price']:,}</span>
    <span class="rating"><span>★</span> {p['rating']}</span>
  </div>
  <div class="score">
    <div class="score-label"><span>Match</span><span>{p['score']:.0f}%</span></div>
    <div class="score-track"><div class="score-fill" style="width:{min(p['score'], 100)}%"></div></div>
  </div>
  <div class="chips">{chips}</div>
</div>
"""


def use_quick_search(text):
    st.session_state["query"] = text


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "query" not in st.session_state:
    st.session_state["query"] = QUICK_SEARCHES[0]

st.markdown(f"""
<div class="nav">
  <div class="logo"><span class="logo-mark">✦</span>SmartShop AI</div>
  <a href="{GITHUB_URL}" target="_blank">View code ↗</a>
</div>
<div class="hero">
  <h1>Find the <span class="grad">right product</span>,<br>in seconds.</h1>
  <p>Describe what you need. Get ranked, explained picks.</p>
</div>
""", unsafe_allow_html=True)

search_col, button_col = st.columns([5, 1], vertical_alignment="bottom")
with search_col:
    query = st.text_input(
        "What are you looking for?",
        key="query",
        placeholder="e.g. wireless earbuds for the gym",
        label_visibility="collapsed",
    )
with button_col:
    st.button("Search", type="primary", use_container_width=True)

chip_cols = st.columns(len(QUICK_SEARCHES))
for col, text in zip(chip_cols, QUICK_SEARCHES):
    col.button(
        text.capitalize(),
        key=f"quick_{text}",
        on_click=use_quick_search,
        args=(text,),
        use_container_width=True,
    )

with st.container(border=True):
    f1, f2, f3, f4 = st.columns([1.2, 1.4, 1.4, 0.8])
    category = f1.selectbox(
        "Category", ["All", "Headphones", "Accessories", "Wearables"]
    )
    budget = f2.slider("Budget (₹)", 1000, 10000, 5000, step=500)
    min_rating = f3.slider("Min rating", 3.0, 5.0, 4.0, step=0.1)
    top_n = f4.segmented_control("Show", [3, 5], default=3) or 3

results = recommend_products(query, budget, category, min_rating, top_n)
passing = sum(
    1 for p in PRODUCTS
    if p["price"] <= budget and p["rating"] >= min_rating
    and (category == "All" or p["category"] == category)
)

st.markdown(f"""
<div class="results-head">
  <h3>Top picks</h3>
  <span class="results-meta">{passing} of {len(PRODUCTS)} products fit your filters</span>
</div>
""", unsafe_allow_html=True)

if not results:
    st.markdown("""
<div class="empty"><div>🔍</div><b>No matches</b>
<p>Try a higher budget or a lower rating.</p></div>
""", unsafe_allow_html=True)
else:
    per_row = 3
    for start in range(0, len(results), per_row):
        cols = st.columns(per_row)
        for offset, p in enumerate(results[start:start + per_row]):
            cols[offset].markdown(
                product_card(p, start + offset + 1), unsafe_allow_html=True
            )
        st.write("")

    with st.expander("Compare side by side"):
        st.dataframe(
            [
                {
                    "Product": p["name"],
                    "Category": p["category"],
                    "Price": p["price"],
                    "Rating": p["rating"],
                    "Match": p["score"],
                }
                for p in results
            ],
            column_config={
                "Price": st.column_config.NumberColumn(format="₹%d"),
                "Rating": st.column_config.NumberColumn(format="%.1f ★"),
                "Match": st.column_config.ProgressColumn(
                    min_value=0, max_value=100, format="%.0f%%"
                ),
            },
            use_container_width=True,
            hide_index=True,
        )

st.markdown(f"""
<div class="foot">
  <div class="pills">
    <span class="pill">Relevance 70%</span>
    <span class="pill">Rating 20%</span>
    <span class="pill">Price 10%</span>
  </div>
  <a href="{GITHUB_URL}" target="_blank">Built by Np · Python · Streamlit</a>
</div>
""", unsafe_allow_html=True)
