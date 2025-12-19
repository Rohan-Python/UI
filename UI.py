import streamlit as st
from datetime import date

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
        "use_for": "Shrinkage crack control, plaster, screed, decorative & light slabs",
        "image": "guard_fiber.png"
    },
    "Bajaj Fibre Tuff": {
        "fiber_type": "Macro Synthetic Polymer Fiber (36–54 mm)",
        "dosage_range": (2.5, 9.0),
        "rate": 350.0,
        "use_for": "Structural reinforcement, industrial floors, pavements, precast",
        "image": "tuff_fiber.png"
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

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Bajaj Reinforcements - Fiber Dosage Assistant", layout="wide")

# ---------------------- HEADER ----------------------
st.markdown("<h1 style='text-align:center;color:red;'>Bajaj Reinforcements</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:grey;margin-top:-10px;'>Muscle to your concrete</h4>", unsafe_allow_html=True)
st.markdown(f"**{GSTIN}**")
st.write("---")

# ---------------------- SECTION SWITCH BUTTONS ----------------------
if "active_section" not in st.session_state:
    st.session_state.active_section = "Bajaj Guard"

c1, c2 = st.columns(2)
with c1:
    if st.button("🧪 Bajaj Guard Fiber", use_container_width=True):
        st.session_state.active_section = "Bajaj Guard"
with c2:
    if st.button("🏗️ Bajaj Tuff Fiber", use_container_width=True):
        st.session_state.active_section = "Bajaj Fibre Tuff"

st.write("---")

# ---------------------- ACTIVE SECTION ----------------------
active_product = st.session_state.active_section
pdata = PRODUCTS[active_product]

st.subheader(f"{active_product}")
st.caption(pdata["use_for"])

img_col, info_col = st.columns([1, 2])
with img_col:
    st.image(pdata["image"], caption=f"{active_product} – actual fiber view", use_container_width=True)
with info_col:
    st.markdown(f"""
    **Fiber Type:** {pdata["fiber_type"]}  
    **Recommended Dosage Range:** {pdata["dosage_range"][0]} – {pdata["dosage_range"][1]} kg/m³  
    **Typical Applications:** {pdata["use_for"]}
    """)

st.write("---")

# ---------------------- DOSAGE SUGGESTION ----------------------
st.header("🧮 Dosage Suggestion")

c1, c2 = st.columns(2)
with c1:
    ctype = st.selectbox("Type of Construction", list(LOGIC.keys()), index=2)
    grade = st.selectbox("Concrete Grade", ["M20","M25","M30","M35","M40","M45","M50"], index=2)
with c2:
    strength = st.selectbox("Structural Requirement", ["Low Toughness","Medium Toughness","High Toughness"], index=1)
    volume = st.number_input("Application Volume (m³)", min_value=0.0, value=10.0, step=1.0)

if st.button("Suggest Dosage", type="primary", use_container_width=True):
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

    st.session_state["suggestion"] = {
        "product": product,
        "fiber_type": p["fiber_type"],
        "dosage": typical,
        "volume": volume,
        "total_qty": total_qty,
        "rate": p["rate"],
        "est_cost": est_cost
    }

    st.success("### ✅ Suggested Solution")
    st.markdown(f"""
    **Recommended Product:** {product}  
    **Fiber Type:** {p["fiber_type"]}  
    **Dosage:** {typical} kg/m³  
    **Total Quantity:** {total_qty} kg  
    **Estimated Cost:** ₹{est_cost:,.2f}
    """)

# ---------------------- ORDER TAB ----------------------
st.write("---")
st.header("📦 Order & Delivery")

suggestion = st.session_state.get("suggestion")
if suggestion:
    st.table({
        "Field": [
            "Product", "Type of Fiber", "Dosage (kg/m³)",
            "Volume (m³)", "Total Qty (kg)", "Rate (₹/kg)", "Cost (₹)"
        ],
        "Value": [
            suggestion["product"], suggestion["fiber_type"], suggestion["dosage"],
            suggestion["volume"], suggestion["total_qty"], suggestion["rate"], suggestion["est_cost"]
        ]
    })
else:
    st.info("Generate dosage suggestion above to proceed with order.")

# ---------------------- FOOTER ----------------------
st.write("---")
st.markdown(
    f"""
    **Quick Links:**  
    🔗 [Visit Website]({COMPANY["website"]}) |
    📧 [{COMPANY["email"]}](mailto:{COMPANY["email"]}) |
    ☎️ {COMPANY["phone"]}
    """
)
