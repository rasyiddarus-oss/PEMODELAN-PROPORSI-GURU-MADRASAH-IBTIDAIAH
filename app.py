import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================

st.set_page_config(
    page_title="Pemodelan Proporsi Guru MI",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main {
    background-color: #c9040b;
}

[data-testid="stMetric"] {
    background-color: Red;
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #2563eb;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}

section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: white;
}

h1, h2, h3 {
    color: #1e293b;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    df = pd.read_excel(
        "Hasil_Analisis_Guru_MI.xlsx"
    )

    return df

df = load_data()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title(
    "📚 Menu Analisis"
)

menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "Dashboard",
        "Visualisasi Data",
        "Pemodelan Regresi",
        "Simulasi Prediksi",
        "Monitoring Distribusi",
        "What-If Analysis",
        "Analisis Gap",
        "Klasifikasi",
        "Laporan"
    ]
)

# ==================================================
# FILTER GLOBAL
# ==================================================

st.sidebar.markdown("---")

tahun_list = sorted(
    df["Tahun"].unique()
)

kota_list = sorted(
    df["Kota"].unique()
)

tahun_filter = st.sidebar.selectbox(
    "📅 Filter Tahun",
    ["Semua"] + list(tahun_list)
)

kota_filter = st.sidebar.selectbox(
    "🏙️ Filter Kota",
    ["Semua"] + list(kota_list)
)

# ==================================================
# DATA FILTER
# ==================================================

df_filter = df.copy()

if tahun_filter != "Semua":

    df_filter = df_filter[
        df_filter["Tahun"] == tahun_filter
    ]

if kota_filter != "Semua":

    df_filter = df_filter[
        df_filter["Kota"] == kota_filter
    ]

# ==================================================
# INFORMASI SIDEBAR
# ==================================================

st.sidebar.markdown("---")

st.sidebar.info(
"""
Pemodelan Proporsi Guru Madrasah Ibtidaiyah
Menggunakan Regresi Linear Berganda
dan Analisis Gap
Provinsi Jawa Barat
"""
)
