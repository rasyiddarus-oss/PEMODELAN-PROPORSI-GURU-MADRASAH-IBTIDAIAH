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

# ==================================================
# DASHBOARD
# ==================================================

if menu == "Dashboard":

    st.title(
        "📊 Dashboard Pendidikan MI Jawa Barat"
    )

    st.markdown(
        "Ringkasan data guru, siswa, dan sekolah Madrasah Ibtidaiyah di Provinsi Jawa Barat."
    )

    # ==========================================
    # KPI
    # ==========================================

    total_guru = int(
        df_filter["Jumlah_Guru"].sum()
    )

    total_siswa = int(
        df_filter["Jumlah_Siswa"].sum()
    )

    total_sekolah = int(
        df_filter["Jumlah_Sekolah"].sum()
    )

    rata_rasio = round(
        df_filter["Rasio_Siswa_Guru"].mean(),
        2
    )

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric(
            "👨‍🏫 Total Guru",
            f"{total_guru:,}"
        )

    with col2:
        st.metric(
            "🎓 Total Siswa",
            f"{total_siswa:,}"
        )

    with col3:
        st.metric(
            "🏫 Total Sekolah",
            f"{total_sekolah:,}"
        )

    with col4:
        st.metric(
            "📈 Rasio Siswa-Guru",
            rata_rasio
        )

    st.markdown("---")

    col1,col2 = st.columns(2)

    with col1:

        kondisi = (
            df_filter["Kondisi"]
            .value_counts()
            .reset_index()
        )

        kondisi.columns = [
            "Kondisi",
            "Jumlah"
        ]

        fig_kondisi = px.pie(
            kondisi,
            values="Jumlah",
            names="Kondisi",
            hole=0.45,
            title="Distribusi Kondisi Guru"
        )

        fig_kondisi.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig_kondisi,
            use_container_width=True
        )

    with col2:

        guru_tahun = (
            df.groupby("Tahun")
            ["Jumlah_Guru"]
            .sum()
            .reset_index()
        )

        fig_guru = px.line(
            guru_tahun,
            x="Tahun",
            y="Jumlah_Guru",
            markers=True,
            title="Perkembangan Jumlah Guru"
        )

        fig_guru.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig_guru,
            use_container_width=True
        )

    st.markdown("---")

    col1,col2 = st.columns(2)

    with col1:

        siswa_tahun = (
            df.groupby("Tahun")
            ["Jumlah_Siswa"]
            .sum()
            .reset_index()
        )

        fig_siswa = px.bar(
            siswa_tahun,
            x="Tahun",
            y="Jumlah_Siswa",
            title="Jumlah Siswa per Tahun"
        )

        fig_siswa.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig_siswa,
            use_container_width=True
        )

    with col2:

        sekolah_tahun = (
            df.groupby("Tahun")
            ["Jumlah_Sekolah"]
            .sum()
            .reset_index()
        )

        fig_sekolah = px.bar(
            sekolah_tahun,
            x="Tahun",
            y="Jumlah_Sekolah",
            title="Jumlah Sekolah per Tahun"
        )

        fig_sekolah.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig_sekolah,
            use_container_width=True
        )
    st.markdown("---")

    # ==========================================
    # TOP 10 KEKURANGAN GURU
    # ==========================================

    st.subheader(
        "🔴 Top 10 Kekurangan Guru Tahun 2025"
    )

    data_2025 = df[
        df["Tahun"] == 2025
    ]

    top_kurang = (
        data_2025[
            data_2025["Gap"] > 0
        ]
        .sort_values(
            by="Gap",
            ascending=False
        )
        .head(10)
    )

    top_kurang["Gap_Label"] = (
        top_kurang["Gap"]
        .round(0)
        .astype(int)
    )

    fig_kurang = px.bar(
        top_kurang,
        x="Gap",
        y="Kota",
        orientation="h",
        color="Gap",
        text="Gap_Label",
        title="Top 10 Kekurangan Guru Tahun 2025"
    )

    fig_kurang.update_layout(
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        fig_kurang,
        use_container_width=True
    )

    st.dataframe(
        top_kurang[
            [
                "Kota",
                "Jumlah_Guru",
                "Guru_Ideal",
                "Gap"
            ]
        ],
        use_container_width=True
    )

    # ==========================================
    # TOP 10 KELEBIHAN GURU
    # ==========================================

    st.subheader(
        "🟢 Top 10 Kelebihan Guru Tahun 2025"
    )

    top_lebih = (
        data_2025[
            data_2025["Gap"] < 0
        ]
        .sort_values(
            by="Gap"
        )
        .head(10)
    )

    top_lebih["Gap_Label"] = (
        top_lebih["Gap"]
        .round(0)
        .astype(int)
    )

    fig_lebih = px.bar(
        top_lebih,
        x="Gap",
        y="Kota",
        orientation="h",
        color="Gap",
        text="Gap_Label",
        title="Top 10 Kelebihan Guru Tahun 2025"
    )

    fig_lebih.update_layout(
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        fig_lebih,
        use_container_width=True
    )

    st.dataframe(
        top_lebih[
            [
                "Kota",
                "Jumlah_Guru",
                "Guru_Ideal",
                "Gap"
            ]
        ],
        use_container_width=True
    )
    st.markdown("---")

    st.subheader(
        "📋 Ringkasan Dataset"
    )

    st.dataframe(
        df_filter,
        use_container_width=True
    )

elif menu == "Visualisasi Data":

    st.title(
        "📈 Visualisasi Data Pendidikan MI"
    )

    st.markdown(
        "Eksplorasi hubungan jumlah siswa, jumlah sekolah, jumlah guru, dan proporsi guru."
    )

    st.subheader(
        "Hubungan Jumlah Siswa dan Jumlah Guru"
    )

    fig = px.scatter(
        df,
        x="Jumlah_Siswa",
        y="Jumlah_Guru",
        color="Tahun",
        size="Jumlah_Sekolah",
        hover_name="Kota",
        title="Jumlah Siswa vs Jumlah Guru"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Hubungan Jumlah Sekolah dan Jumlah Guru"
    )

    fig = px.scatter(
        df,
        x="Jumlah_Sekolah",
        y="Jumlah_Guru",
        color="Tahun",
        hover_name="Kota",
        title="Jumlah Sekolah vs Jumlah Guru"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Top 10 Kota dengan Jumlah Guru Terbanyak"
    )

    top_guru = (
        df[
            df["Tahun"] == 2025
        ]
        .sort_values(
            by="Jumlah_Guru",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_guru,
        x="Jumlah_Guru",
        y="Kota",
        orientation="h",
        color="Jumlah_Guru",
        title="Top 10 Kota dengan Guru Terbanyak Tahun 2025"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Top 10 Kota dengan Jumlah Siswa Terbanyak"
    )

    top_siswa = (
        df[
            df["Tahun"] == 2025
        ]
        .sort_values(
            by="Jumlah_Siswa",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_siswa,
        x="Jumlah_Siswa",
        y="Kota",
        orientation="h",
        color="Jumlah_Siswa",
        title="Top 10 Kota dengan Jumlah Siswa Terbanyak Tahun 2025"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Distribusi Rasio Siswa-Guru"
    )

    fig = px.histogram(
        df,
        x="Rasio_Siswa_Guru",
        nbins=20,
        title="Distribusi Rasio Siswa-Guru"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Top 10 Rasio Siswa-Guru Tertinggi"
    )

    top_rasio = (
        df[
            df["Tahun"] == 2025
        ]
        .sort_values(
            by="Rasio_Siswa_Guru",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_rasio[
            [
                "Kota",
                "Jumlah_Siswa",
                "Jumlah_Guru",
                "Rasio_Siswa_Guru"
            ]
        ],
        use_container_width=True
    )

    st.markdown("---")

    st.success(f"""
    Insight Data Tahun 2025:

    • Kota dengan jumlah guru terbanyak:
      {top_guru.iloc[0]['Kota']}

    • Kota dengan jumlah siswa terbanyak:
      {top_siswa.iloc[0]['Kota']}

    • Rasio siswa-guru tertinggi:
      {top_rasio.iloc[0]['Kota']}
      ({top_rasio.iloc[0]['Rasio_Siswa_Guru']:.2f})
    """)

# ==================================================
# PEMODELAN REGRESI
# ==================================================

elif menu == "Pemodelan Regresi":

    st.title(
        "🧮 Pemodelan Regresi Linear Berganda"
    )

    st.markdown("""
    Model regresi digunakan untuk memodelkan hubungan
    antara jumlah siswa dan jumlah sekolah terhadap
    jumlah guru Madrasah Ibtidaiyah.
    """)

    st.subheader(
        "Persamaan Regresi"
    )

    st.latex(
        r'''
        Y =
        175.3598
        +
        0.0222X_1
        +
        4.7393X_2
        '''
    )

    st.markdown("---")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric(
            "R²",
            "0.929"
        )

    with col2:
        st.metric(
            "Adj R²",
            "0.927"
        )

    with col3:
        st.metric(
            "Variabel Signifikan",
            "2"
        )

    with col4:
        st.metric(
            "Observasi",
            "108"
        )

    st.markdown("---")

    st.subheader(
        "Interpretasi Koefisien"
    )

    interpretasi = pd.DataFrame({

        "Variabel":[
            "Jumlah Siswa",
            "Jumlah Sekolah"
        ],

        "Koefisien":[
            0.0222,
            4.7393
        ],

        "Interpretasi":[
            "Setiap kenaikan 1 siswa meningkatkan jumlah guru sebesar 0.0222",
            "Setiap kenaikan 1 sekolah meningkatkan jumlah guru sebesar 4.7393"
        ]

    })

    st.dataframe(
        interpretasi,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader(
        "Aktual vs Prediksi"
    )

    fig = px.scatter(
        df,
        x="Jumlah_Guru",
        y="Guru_Prediksi",
        color="Tahun",
        hover_name="Kota",
        title="Perbandingan Guru Aktual dan Prediksi"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Distribusi Error Prediksi"
    )

    df_error = df.copy()

    df_error["Error"] = (
        df_error["Jumlah_Guru"]
        -
        df_error["Guru_Prediksi"]
    )

    fig = px.histogram(
        df_error,
        x="Error",
        nbins=20,
        title="Distribusi Error Prediksi"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader(
        "Korelasi Variabel"
    )

    corr = df[
        [
            "Jumlah_Siswa",
            "Jumlah_Sekolah",
            "Jumlah_Guru"
        ]
    ].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Matriks Korelasi"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    st.success("""
    Kesimpulan Model:

    • Model mampu menjelaskan 92,9% variasi jumlah guru.

    • Jumlah siswa berpengaruh positif terhadap jumlah guru.

    • Jumlah sekolah berpengaruh positif terhadap jumlah guru.

    • Model layak digunakan untuk analisis kebutuhan guru MI.
    """)

