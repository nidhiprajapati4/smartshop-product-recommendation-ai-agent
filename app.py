
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


st.title("🛍️ SmartShop AI")
st.subheader("Your personal product recommendation agent")
st.write(
    "Describe what you need. SmartShop ranks matching products "
    "by feature relevance, rating, and budget."
)

with st.sidebar:
    st.header("Your preferences")
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
    top_n = st.selectbox("Recommendations", [3, 5], index=0)

st.markdown("### What are you shopping for?")
query = st.text_input(
    "Describe your needs",
    value="wireless headphones for office calls and travel",
    placeholder="e.g. fitness earbuds under ₹3000",
)

if st.button("Find my best matches", type="primary"):
    st.session_state["last_query"] = query
    st.session_state["last_budget"] = budget
    st.session_state["last_category"] = category
    st.session_state["last_rating"] = min_rating
    st.session_state["last_n"] = top_n

if "last_query" not in st.session_state:
    st.session_state["last_query"] = query
    st.session_state["last_budget"] = budget
    st.session_state["last_category"] = category
    st.session_state["last_rating"] = min_rating
    st.session_state["last_n"] = top_n

results = recommend_products(
    st.session_state["last_query"],
    st.session_state["last_budget"],
    st.session_state["last_category"],
    st.session_state["last_rating"],
    st.session_state["last_n"],
)

st.markdown("---")
st.markdown("### Your recommendations")

if not results:
    st.warning(
        "No products match these preferences. Try increasing your "
        "budget or lowering the minimum rating."
    )
else:
    st.caption(
        f"{len(results)} matches | "
        f"Budget: ₹{st.session_state['last_budget']:,} | "
        "Sample catalog; prices and ratings are illustrative."
    )

    cols = st.columns(min(3, len(results)))
    for i, p in enumerate(results):
        with cols[i % len(cols)]:
            st.markdown(f"#### {p['name']}")
            st.metric("Price", f"₹{p['price']:,}")
            st.write(f"⭐ {p['rating']} / 5 (sample rating)")
            st.progress(min(p["score"] / 100, 1.0))
            st.caption(f"Match score: {p['score']} / 100")
            st.write(p["description"])
            st.write(f"**Why it matched:** {p['pros']}")
            if p["matched"]:
                st.write("**Matched terms:** " + ", ".join(p["matched"]))
            else:
                st.write("**Matched terms:** No direct keyword overlap")
            st.write(f"Category: {p['category']}")

    st.markdown("### Compare your shortlist")
    st.dataframe(
        [
            {
                "Product": p["name"],
                "Category": p["category"],
                "Price (₹)": p["price"],
                "Rating": p["rating"],
                "Match score": p["score"],
            }
            for p in results
        ],
        use_container_width=True,
        hide_index=True,
    )

with st.expander("How does the recommendation engine work?"):
    st.markdown("""
    1. **Filter:** Exclude products above budget or below the
       minimum rating.
    2. **Match:** Compare words in the user's request with product
       names, features, and descriptions.
    3. **Rank:** Combine feature relevance (70%), rating (20%),
       and affordability (10%) into a heuristic score.
    4. **Explain:** Show matching terms and product characteristics.

    This is a transparent baseline recommender, not a trained ML
    model or an LLM-powered autonomous agent. The match score is a
    heuristic, not a probability that the user will buy the item.
    """)

st.markdown("---")
st.caption("Portfolio project • Python • Streamlit • Explainable ranking")
