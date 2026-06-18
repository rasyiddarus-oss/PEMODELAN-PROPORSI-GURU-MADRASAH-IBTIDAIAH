import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Pemodelan Proporsi Guru Madrasah Ibtidaiah",
    page_icon="📊",
    layout="wide"
)

df = pd.read_excel(
    "Hasil_Analisis_Guru_MI.xlsx"
)

menu = st.sidebar.selectbox(
    "Pilih Menu",
    [
        "Dashboard",
        "Visualisasi Data",
        "Pemodelan Regresi",
        "Prediksi Jumlah Guru",
        "Analisis Gap",
        "Klasifikasi",
        "Laporan"
    ]
)

if menu == "Dashboard":

    st.title(
        "Dashboard Data Pendidikan MI"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Guru",
            int(df["Jumlah_Guru"].sum())
        )

    with col2:
        st.metric(
            "Total Siswa",
            int(df["Jumlah_Siswa"].sum())
        )

    with col3:
        st.metric(
            "Total Sekolah",
            int(df["Jumlah_Sekolah"].sum())
        )

    st.subheader(
        "Data Pendidikan MI"
    )

    st.dataframe(df.head(10))

elif menu == "Visualisasi Data":

    st.title(
        "Visualisasi Data Pendidikan MI"
    )

    guru_tahun = (
        df.groupby("Tahun")
        ["Jumlah_Guru"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        guru_tahun,
        x="Tahun",
        y="Jumlah_Guru",
        title="Jumlah Guru per Tahun"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

elif menu == "Pemodelan Regresi":

    st.title(
        "Pemodelan Regresi Linear Berganda"
    )

    st.latex(
        r'''
        Y =
        267.5792
        +
        0.0487X_1
        -
        0.3058X_2
        '''
    )

    st.write(
        "R² : 0.965"
    )

    st.write(
        "Adjusted R² : 0.965"
    )

    st.write(
        "MAE : 180.86"
    )

    st.write(
        "RMSE : 234.83"
    )

elif menu == "Prediksi Jumlah Guru":

    st.title(
        "Prediksi Jumlah Guru"
    )

    st.dataframe(
        df[
            [
                "Tahun",
                "Kota",
                "Jumlah_Guru",
                "Guru_Prediksi"
            ]
        ]
    )

elif menu == "Analisis Gap":

    st.title(
        "Analisis Gap Proporsi Guru"
    )

    st.dataframe(
        df[
            [
                "Tahun",
                "Kota",
                "Guru_Ideal",
                "Jumlah_Guru",
                "Gap"
            ]
        ]
    )

elif menu == "Klasifikasi":

    st.title(
        "Klasifikasi Kondisi Distribusi Guru"
    )

    st.dataframe(
        df[
            [
                "Tahun",
                "Kota",
                "Gap",
                "Kondisi"
            ]
        ]
    )

    st.subheader(
        "Distribusi Kondisi"
    )

    st.bar_chart(
        df["Kondisi"]
        .value_counts()
    )

elif menu == "Laporan":

    st.title(
        "Laporan Hasil Analisis"
    )

    with open(
        "Hasil_Analisis_Guru_MI.xlsx",
        "rb"
    ) as file:

        st.download_button(
            label="Download Laporan",
            data=file,
            file_name="Hasil_Analisis_Guru_MI.xlsx"
        )

