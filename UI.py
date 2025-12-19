import streamlit as st
from datetime import date

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Bajaj Reinforcements – Fiber Assistant",
    layout="wide"
)

# ---------------------- SESSION STATE ----------------------
if "active_section" not in st.session_state:
    st.session_state.active_section = "Bajaj Guard"

if "suggestion" not in st.session_state:
    st.session_state.suggestion = None

if "cart" not in st.session_state:
    st.session_state.cart = None

if "page" not in st.session_state:
    st.session_state.page = "browse"

# ---------------------- COMPANY DATA ----------------------
COMPANY = {
    "website": "https://www.brllp.in",
    "email": "info@brllp.in",
    "phone": "+91 7104 281000",
}
GSTIN = "GSTIN: 27ABCDE1234F1Z5"

# ---------------------- PRODUCT DATA ----------------------
PRODUCTS = {
    "Bajaj Guard": {
        "fiber_type": "Fibrillated Polypropylene Microfiber (6 mm)",
        "dosage_range": (0.6, 1.0),
        "rate": 180,
        "use_for": "Shrinkage crack control, plaster, screed, decorative slabs",
        "image": "guard_fiber.png"
    },
    "Bajaj Fibre Tuff": {
        "fiber_type": "Macro Synthetic Polymer Fiber (36–54 mm)",
        "dosage_range": (2.5, 9.0),
        "rate": 350,
        "use_for": "Structural reinforcement, industrial floors, pavements, precast",
        "image": "tuff_fiber.png"
    }
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

# ====================== HEADER ======================
st.markdown("<h1 style='text-align:center;color:red;'>Bajaj Reinforcements</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:grey;margin-top:-10px;'>Muscle to your concrete</h4>", unsafe_allow_html=True)
st.markdown(f"**{GSTIN}**")
st.write("---")

# ====================== TOP SECTION BUTTONS ======================
c1, c2 = st.columns(2)
with c1:
    if st.button("🧪 Bajaj Guard Fiber", use_container_width=True):
        st.session_state.active_section = "Bajaj Guard"
with c2:
    if st.button("🏗️ Bajaj Tuff Fiber", use_container_width=True):
        st.session_state.active_section = "Bajaj Fibre Tuff"

st.write("---")

# ====================== FIBER SECTION ======================
active = st.session_state.active_section
pdata = PRODUCTS[active]

st.subheader(active)
st.caption(pdata["use_for"])

col_img, col_info = st.columns([1, 2])
with col_img:
    st.image(pdata["image"], caption="Actual fiber (zoomed view)", use_container_width=True)

with col_info:
    st.markdown(f"""
    **Fiber Type:** {pdata["fiber_type"]}  
    **Recommended Dosage Range:** {pdata["dosage_range"][0]} – {pdata["dosage_range"][1]} kg/m³  
    **Typical Applications:** {pdata["use_for"]}
    """)

# ---------------- BUY / CART BUTTONS ----------------
b1, b2 = st.columns(2)
with b1:
    if st.button("🛒 Add to Cart", use_container_width=True):
        st.session_state.cart = {"product": active, "rate": pdata["rate"]}
        st.success("Added to cart")

with b2:
    if st.button("⚡ Buy Now", type="primary", use_container_width=True):
        st.session_state.cart = {"product": active, "rate": pdata["rate"]}
        st.session_state.page = "checkout"
        st.experimental_rerun()

st.write("---")

# ====================== DOSAGE SUGGESTION ======================
st.header("🧮 Dosage Suggestion")

c1, c2 = st.columns(2)
with c1:
    ctype = st.selectbox("Type of Construction", list(LOGIC.keys()), index=2)
    grade = st.selectbox("Concrete Grade", ["M20","M25","M30","M35","M40","M45","M50"], index=2)
with c2:
    strength = st.selectbox("Structural Requirement", ["Low Toughness","Medium Toughness","High Toughness"], index=1)
    volume = st.number_input("Application Volume (m³)", min_value=1.0, value=10.0)

if st.button("Suggest Dosage", type="primary", use_container_width=True):
    product = LOGIC.get(ctype)
    p = PRODUCTS[product]
    mn, mx = p["dosage_range"]

    if strength == "High Toughness":
        dosage = mn + (mx - mn) * 0.7
    elif strength == "Low Toughness":
        dosage = mn + (mx - mn) * 0.3
    else:
        dosage = (mn + mx) / 2

    total_qty = round(dosage * volume, 2)
    cost = round(total_qty * p["rate"], 2)

    st.session_state.suggestion = {
        "product": product,
        "fiber_type": p["fiber_type"],
        "dosage": round(dosage,2),
        "volume": volume,
        "total_qty": total_qty,
        "rate": p["rate"],
        "cost": cost
    }

    st.success("### ✅ Suggested Solution")
    st.markdown(f"""
    **Product:** {product}  
    **Fiber Type:** {p["fiber_type"]}  
    **Dosage:** {dosage:.2f} kg/m³  
    **Total Quantity:** {total_qty} kg  
    **Estimated Cost:** ₹{cost:,.2f}
    """)

# ====================== CHECKOUT PAGE ======================
if st.session_state.page == "checkout":
    st.write("---")
    st.header("📦 Delivery & Checkout")

    cart = st.session_state.cart
    suggestion = st.session_state.suggestion

    if suggestion and suggestion["product"] == cart["product"]:
        qty = suggestion["total_qty"]
        rate = suggestion["rate"]
    else:
        qty = st.number_input("Enter Quantity (kg)", min_value=1.0)
        rate = cart["rate"]

    total = qty * rate

    st.subheader("🧾 Order Summary")
    st.markdown(f"""
    **Product:** {cart["product"]}  
    **Quantity:** {qty} kg  
    **Rate:** ₹{rate}/kg  
    **Total Amount:** ₹{total:,.2f}
    """)

    st.write("---")
    st.subheader("🚚 Delivery Address")

    with st.form("delivery"):
        name = st.text_input("Full Name *")
        phone = st.text_input("Mobile Number *")
        email = st.text_input("Email")

        c1, c2 = st.columns(2)
        with c1:
            house = st.text_input("Flat / House No *")
            area = st.text_input("Street / Area *")
            landmark = st.text_input("Landmark")
        with c2:
            city = st.text_input("City *")
            state = st.text_input("State *")
            pincode = st.text_input("PIN Code *")

        delivery_date = st.date_input("Preferred Delivery Date", value=date.today())
        instructions = st.text_area("Delivery Instructions")

        submit = st.form_submit_button("✅ Place Order", type="primary")

        if submit:
            if not all([name, phone, house, area, city, state, pincode]):
                st.error("Please fill all required fields.")
            else:
                st.success("🎉 Order Placed Successfully!")
                st.info("Our team will contact you shortly for confirmation and dispatch.")

# ====================== FOOTER ======================
st.write("---")
st.markdown(
    f"""
    **Quick Links:**  
    🔗 [Visit Website]({COMPANY["website"]}) |
    📧 [{COMPANY["email"]}](mailto:{COMPANY["email"]}) |
    ☎️ {COMPANY["phone"]}
    """
)
