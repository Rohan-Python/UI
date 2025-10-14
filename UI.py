import streamlit as st
import webbrowser

# ---------------------- COMPANY & PRODUCT DATA ----------------------
COMPANY = {
    "website": "https://www.brllp.in",
    "email": "info@brllp.in",
    "phone": "+91 7104 281000",
}
GSTIN = "GSTIN: 27ABCDE1234F1Z5"

PRODUCTS = {
    "Bajaj Guard": {
        "fiber_type": "Fibrillated Polypropylene Microfiber (6 mm)",
        "dosage_range": (0.6, 1.0),
        "rate": 180.0,
        "use_for": "Shrinkage / finish control (plaster, screed, light slabs)",
    },
    "Bajaj Fibre Tuff": {
        "fiber_type": "Macro Synthetic Polymer Fiber (36–54 mm)",
        "dosage_range": (2.5, 9.0),
        "rate": 350.0,
        "use_for": "Structural reinforcement (floors, pavements, runways, precast)",
    },
}

LOGIC = {
    "Plaster / Screed / Finishing": "Bajaj Guard",
    "Residential / Decorative Floor": "Bajaj Guard",
    "Industrial Floor": "Bajaj Fibre Tuff",
    "Pavement / Road": "Bajaj Fibre Tuff",
    "Runway / Airfield": "Bajaj Fibre Tuff",
    "Tunnel Lining / Shotcrete": "Bajaj Fibre Tuff",
    "Precast Element": "Bajaj Fibre Tuff",
}


# ---------------------- STREAMLIT LAYOUT ----------------------
st.set_page_config(page_title="Bajaj Reinforcements - Fiber Dosage Assistant", layout="wide")

st.markdown("<h1 style='color:red;'>Bajaj Reinforcements</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:grey;margin-top:-15px;'>Muscle to your concrete</h3>", unsafe_allow_html=True)
st.markdown(f"**{GSTIN}**")
st.write("---")

tab1, tab2 = st.tabs(["🧮 Dosage Suggestion", "📦 Order & Delivery"])

# ---------------------- TAB 1 ----------------------
with tab1:
    st.header("Project / Concrete Details")

    col1, col2 = st.columns(2)
    with col1:
        ctype = st.selectbox("Type of Construction", list(LOGIC.keys()), index=2)
        grade = st.selectbox("Concrete Grade", ["M20","M25","M30","M35","M40","M45","M50"], index=2)
    with col2:
        strength = st.selectbox("Structural Requirement", ["Low Toughness","Medium Toughness","High Toughness"], index=1)
        volume = st.number_input("Application Volume (m³)", min_value=0.0, value=10.0, step=1.0)

    # Suggestion logic
    if st.button("Suggest Dosage", use_container_width=True, type="primary"):
        product = LOGIC.get(ctype, "Bajaj Fibre Tuff")
        p = PRODUCTS[product]
        mn, mx = p["dosage_range"]

        if strength == "High Toughness":
            typical = round(mn + (mx - mn) * 0.7, 2)
        elif strength == "Low Toughness":
            typical = round(mn + (mx - mn) * 0.3, 2)
        else:
            typical = round((mn + mx) / 2, 2)

        total_qty = round(typical * volume, 2)
        est_cost = round(total_qty * p["rate"], 2)

        suggestion = {
            "product": product,
            "fiber_type": p["fiber_type"],
            "dosage": typical,
            "volume": volume,
            "total_qty": total_qty,
            "rate": p["rate"],
            "est_cost": est_cost
        }

        st.success(f"**Suggestion Ready!**")
        st.write(f"**Product:** {product}")
        st.write(f"**Fiber Type:** {p['fiber_type']}")
        st.write(f"**Suggested Dosage:** {typical} kg/m³")
        st.write(f"**Total Quantity:** {total_qty} kg")
        st.write(f"**Estimated Cost:** ₹{est_cost:,.2f}")

        st.session_state["suggestion"] = suggestion

# ---------------------- TAB 2 ----------------------
with tab2:
    st.header("Order & Rate Details")
    suggestion = st.session_state.get("suggestion", None)

    if suggestion:
        st.table({
            "Field": [
                "Product", "Type of Fiber", "Dosage (kg/m³)",
                "Application Volume (m³)", "Total Quantity (kg)",
                "Rate (₹/kg)", "Estimated Cost (₹)"
            ],
            "Value": [
                suggestion["product"], suggestion["fiber_type"], suggestion["dosage"],
                suggestion["volume"], suggestion["total_qty"], suggestion["rate"], suggestion["est_cost"]
            ]
        })
    else:
        st.info("No dosage suggestion yet. Please use the first tab to generate a suggestion.")

# ---------------------- FOOTER ----------------------
st.write("---")
st.markdown(
    f"""
    **Quick Links:**  
    🔗 [Visit Website]({COMPANY["website"]}) | 📧 [{COMPANY["email"]}](mailto:{COMPANY["email"]}) | ☎️ {COMPANY["phone"]}
    """
)
