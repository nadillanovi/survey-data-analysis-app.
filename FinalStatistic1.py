import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# KONFIGURASI HALAMAN
# ---------------------------------------------------------
st.set_page_config(
    page_title="Survey Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CSS TEMA INDUSTRIAL (SINGKAT, RAPIH)
# ---------------------------------------------------------
industrial_css = """
<style>
/* Background utama cerah */
[data-testid="stAppViewContainer"] {
    background-color: #f4f5f7;
}

/* Sidebar abu muda */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    color: #333333 !important;
    box-shadow: 4px 0 12px rgba(0,0,0,0.08);
}

/* Card besar tengah */
.main-wrapper {
    background: #ffffff;
    border-radius: 18px;
    padding: 2.3rem 2.3rem 2rem 2.3rem;
    margin: 1.5rem 2rem;
    box-shadow: 0 14px 32px rgba(15, 23, 42, 0.18);
}

/* Judul utama */
.app-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #222222;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    text-align: center;
}
.app-title-dot {
    display: inline-block;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    margin-right: 10px;
    background: radial-gradient(circle at 30% 30%, #ffe0e0 0, #ff5252 45%, #c62828 100%);
}

/* Garis judul */
.title-separator {
    height: 3px;
    width: 160px;
    margin: 0.6rem auto 1.6rem auto;
    border-radius: 999px;
    background: linear-gradient(90deg, #ff9800, #ffc107, #ff9800);
}

/* Judul section */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #333333;
    margin-bottom: 0.7rem;
}

/* Card kecil */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.1rem 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.12);
    border: 1px solid #e5e7eb;
}
.card-title {
    font-weight: 700;
    font-size: 1.05rem;
    color: #111827;
    margin-bottom: 0.4rem;
}

/* Tabel dan metric */
.stDataFrame { border-radius: 10px; overflow: hidden; }
[data-testid="stMetric"] {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.12);
}

/* Sedikit rapikan label */
label, .stMarkdown, .stRadio, .stSelectbox {
    color: #111827 !important;
}
</style>
"""

st.markdown(industrial_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA PROFIL TETAP (HARD-CODE)
# ---------------------------------------------------------
members = [
    {
        "name": "Nadilla Novi Anggraini",
        "role": "Leader",
        "photo_path": "poto dilla.jpeg"
    },
    {
        "name": "Ahmad Arda Syafi",
        "role": "Member",
        "photo_path": "poto arda.jpeg"
    },
    {
        "name": "Laurensius Mahendra Wisnu Wardana",
        "role": "Member",
        "photo_path": "poto wisnu.jpeg"
    }
]


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    lang = st.selectbox(
        "Pilih Bahasa / Choose Language",
        ["Indonesia", "English"],
        key="lang_select"
    )
    st.subheader("Play Music")
    audio = st.file_uploader("Upload Audio", type=["mp3", "wav"])
    if audio:
        st.audio(audio)

# ---------------------------------------------------------
# WRAPPER UTAMA
# ---------------------------------------------------------
st.markdown("<div class='main-wrapper'>", unsafe_allow_html=True)
st.markdown(
    "<div class='app-title'><span class='app-title-dot'></span>Survey Data Analysis Application</div>",
    unsafe_allow_html=True
)
st.markdown("<div class='title-separator'></div>", unsafe_allow_html=True)

# ======================= PROFIL KELOMPOK (FIX) =======================
st.markdown("<div class='section-title'>👥 Group Profile</div>", unsafe_allow_html=True)

cols = st.columns(3)
for col, m in zip(cols, members):
    with col:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-title'>{m['name']}</div>", unsafe_allow_html=True)

        # FOTO TETAP, TIDAK ADA UPLOADER
        st.image(m["photo_path"], width=170)

        # ROLE TETAP, TIDAK BISA DIKETIK
        st.markdown(f"**Role in Group:** {m['role']}")

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ======================= ANALISIS DATA =======================
st.markdown("<div class='section-title'>Survey Data Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='card'>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"], key="data_upload")

if uploaded_file is None:
    st.info("Silakan upload file Excel (.xlsx) untuk memulai analisis.")
else:
    df = pd.read_excel(uploaded_file)
    st.markdown("**Data Preview**")
    st.dataframe(df.head(), use_container_width=True)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if not numeric_cols:
        st.warning("Tidak ada kolom numerik ditemukan dalam data.")
    else:
        col_left, col_right = st.columns([1, 1.3])

        with col_left:
            menu = st.radio(
                "Choose Analysis Type",
                ["Descriptive Analysis", "Correlation Analysis"],
                key="analysis_menu"
            )

        with col_right:
            if menu == "Descriptive Analysis":
                st.markdown("**Descriptive Statistics**")
                selected = st.multiselect(
                    "Select numeric variables",
                    numeric_cols,
                    default=numeric_cols,
                    key="desc_vars"
                )
                if selected:
                    st.dataframe(df[selected].describe(), use_container_width=True)
                else:
                    st.info("Select at least one numeric variable.")
            else:
                st.markdown("**Correlation Analysis**")
                c1, c2 = st.columns(2)
                with c1:
                    var1 = st.selectbox("Variable X", numeric_cols, key="corr_var1")
                with c2:
                    var2 = st.selectbox("Variable Y", numeric_cols, key="corr_var2")

                method = st.selectbox(
                    "Correlation Method",
                    ["pearson", "spearman"],
                    key="corr_method"
                )

                corr = df[[var1, var2]].corr(method=method).iloc[0, 1]
                st.metric("Correlation Value", f"{corr:.4f}")

                fig, ax = plt.subplots(figsize=(6, 4))
                ax.scatter(df[var1], df[var2], color="#ffb300", alpha=0.8, edgecolor="#111")
                ax.set_xlabel(var1)
                ax.set_ylabel(var2)
                ax.set_title(f"{var1} vs {var2}")
                ax.grid(True, alpha=0.3)

                fig.patch.set_facecolor("white")
                ax.set_facecolor("white")

                st.pyplot(fig) 


st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
