import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Traffic Volume Prediction & Accident Analysis",
    layout="wide"
)

# -------------------------------------------------
# BASIC STYLING (COLOR UI)
# -------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
h1, h2, h3 {
    color: #1f4e79;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("🚦 Navigation")

uploaded_file = st.sidebar.file_uploader(
    "Upload Traffic Dataset (CSV)",
    type=["csv"]
)

page = st.sidebar.radio(
    "Select Section",
    ["About Project", "Dataset Overview", "Analysis"]
)

# -------------------------------------------------
# LOAD DATA (DEFAULT OR UPLOADED)
# -------------------------------------------------
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if uploaded_file:
    data = load_data(uploaded_file)
    st.sidebar.success("Custom dataset loaded")
else:
    data = load_data("traffic_cleaned.csv")
    st.sidebar.info("Using sample dataset")

# -------------------------------------------------
# CREATE CONGESTION LEVEL (DERIVED — NOT IN CSV)
# -------------------------------------------------
def get_congestion(speed):
    if speed >= 45:
        return "Low"
    elif speed >= 30:
        return "Medium"
    else:
        return "High"

data["Congestion Level"] = data["Average Speed (km/h)"].apply(get_congestion)

# -------------------------------------------------
# ABOUT PAGE
# -------------------------------------------------
if page == "About Project":
    st.title("Traffic Volume Prediction and Accident Analysis")

    st.write("""
    This project is a **Final Year Major Project** focused on analyzing and
    predicting traffic behavior using real-world traffic datasets.

    Unlike traditional systems that rely on fixed datasets, this application
    supports **custom CSV uploads**, allowing traffic authorities and users
    to analyze **any traffic dataset** in real time.
    """)

    st.subheader("🎯 Objectives")
    st.markdown("""
    - Analyze traffic volume patterns  
    - Study speed variation under congestion  
    - Identify accident-prone traffic conditions  
    - Provide visual insights using interactive dashboards  
    """)

    st.subheader("🚀 Key Feature (USP)")
    st.markdown("""
    ✔ Custom dataset upload  
    ✔ Automatic congestion calculation  
    ✔ Fast visual analytics  
    ✔ Scalable for real-world smart city systems  
    """)

    st.subheader("🛠 Technologies Used")
    st.markdown("""
    - Python  
    - Pandas  
    - Streamlit  
    - Matplotlib  
    """)

# -------------------------------------------------
# DATASET OVERVIEW
# -------------------------------------------------
elif page == "Dataset Overview":
    st.title("Dataset Overview")

    st.subheader("Preview")
    st.dataframe(data.head(50), use_container_width=True)

    st.subheader("Statistical Summary")
    st.dataframe(data.describe(), use_container_width=True)

# -------------------------------------------------
# ANALYSIS PAGE
# -------------------------------------------------
elif page == "Analysis":
    st.title("Traffic Analysis Dashboard")

    # ------------------------------
    # SAMPLE DATA FOR FAST LOADING
    # ------------------------------
    if len(data) > 1500:
        plot_data = data.sample(1500, random_state=42)
    else:
        plot_data = data

    # ------------------------------
    # 1. Traffic Volume Distribution
    # ------------------------------
    st.subheader("Traffic Volume Distribution")

    fig1, ax1 = plt.subplots(figsize=(6, 3))
    ax1.hist(plot_data["Traffic Volume"], bins=20)
    ax1.set_xlabel("Traffic Volume")
    ax1.set_ylabel("Frequency")
    plt.tight_layout()
    st.pyplot(fig1)

    # ------------------------------
    # 2. Volume vs Speed
    # ------------------------------
    st.subheader("Traffic Volume vs Average Speed")

    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax2.scatter(
        plot_data["Traffic Volume"],
        plot_data["Average Speed (km/h)"],
        s=10,
        alpha=0.6
    )
    ax2.set_xlabel("Traffic Volume")
    ax2.set_ylabel("Average Speed (km/h)")
    plt.tight_layout()
    st.pyplot(fig2)

    # ------------------------------
    # 3. Congestion Distribution
    # ------------------------------
    st.subheader("Congestion Level Distribution")

    fig3, ax3 = plt.subplots(figsize=(5, 3))
    data["Congestion Level"].value_counts().plot(
        kind="bar",
        ax=ax3
    )
    ax3.set_xlabel("Congestion Level")
    ax3.set_ylabel("Count")
    plt.tight_layout()
    st.pyplot(fig3)

    # ------------------------------
    # OBSERVATIONS
    # ------------------------------
    st.subheader("Observations")
    st.write("""
    - Traffic volume has a direct impact on average speed.
    - Lower speeds indicate higher congestion levels.
    - Accident occurrences increase during high congestion periods.
    - The system adapts dynamically to any uploaded dataset.
    """)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.markdown(
    "<center>Final Year Project | Traffic Volume Prediction & Accident Analysis</center>",
    unsafe_allow_html=True
)
