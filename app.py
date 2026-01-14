import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract
import cv2
import numpy as np

# -------- TESSERACT PATH --------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -------- PAGE CONFIG --------
st.set_page_config(
    page_title="Receipt and Invoice Digitizer",
    layout="wide"
)

st.title("🧾 Receipt and Invoice Digitizer")

# ---------- SIDEBAR ----------
st.sidebar.header("🔐 Authentication")
st.sidebar.text_input("API Key", type="password")
st.sidebar.button("Clear All Records")

# ---------- UPLOAD ----------
st.subheader("📤 Upload Receipt / Invoice")

uploaded_file = st.file_uploader(
    "Upload Image (JPG / PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    processed = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    st.subheader("🖼️ Image Processing Comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("*Original Image*")
        st.image(image, use_container_width=True)

    with col2:
        st.markdown("*Processed Image (For OCR)*")
        st.image(processed, use_container_width=True)

    text = pytesseract.image_to_string(processed)
    st.subheader("📄 Extracted Text")
    st.text_area("OCR Output", text, height=220)

# =====================================================
# 📦 PERSISTENT STORAGE (DRILL-DOWN VIEW)
# =====================================================
st.subheader("📦 Persistent Storage (Drill-Down View)")

data = {
    "merchant": [
        "Walmart", "Walmart", "Walmart",
        "Amazon",
        "DMart"
    ],
    "category": [
        "Grocery", "Electronics", "Clothing",
        "Electronics",
        "Grocery"
    ],
    "total": [
        450, 1299, 799,
        1599,
        320
    ]
}

df = pd.DataFrame(data)

# ---- MERCHANT SELECTION ----
selected_merchant = st.selectbox(
    "Select Merchant",
    df["merchant"].unique()
)

merchant_df = df[df["merchant"] == selected_merchant]

# ---- CATEGORY SELECTION ----
selected_category = st.selectbox(
    "Select Category",
    merchant_df["category"].unique()
)

category_df = merchant_df[
    merchant_df["category"] == selected_category
]

# ---- SHOW COST ----
cost = category_df["total"].values[0]

st.success(
    f"💰 **{selected_merchant} → {selected_category} cost: ₹{cost}**"
)

st.dataframe(category_df, use_container_width=True)

# =====================================================
# 📊 ANALYTICS DASHBOARD
# =====================================================
st.subheader("📊 Analytics Dashboard")

col1, col2 = st.columns(2)

# -------- BAR CHART (WALMART) --------
with col1:
    st.markdown("*Walmart – Category-wise Spend*")

    walmart_df = df[df["merchant"] == "Walmart"]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(
        walmart_df["category"],
        walmart_df["total"]
    )
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    ax.set_title("Walmart – Category-wise Spend")

    st.pyplot(fig)

# -------- PIE CHART (ALL MERCHANTS) --------
with col2:
    st.markdown("*Category-wise Distribution*")

    fig2, ax2 = plt.subplots()
    ax2.pie(
        df.groupby("category")["total"].sum(),
        labels=df["category"].unique(),
        autopct="%1.1f%%"
    )
    ax2.set_title("Overall Category Distribution")

    st.pyplot(fig2)
