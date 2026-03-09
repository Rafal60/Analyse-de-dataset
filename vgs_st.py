import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Dashboard Gaming", page_icon="👾", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

/* Fond de l'application (style grille discrète sombre) */
.stApp {
    background-color: #121212;
    background-image: radial-gradient(#2b2b40 1px, transparent 1px);
    background-size: 20px 20px;
    color: #00FF41; /* Vert Matrix */
}

/* Style de la barre latérale */
[data-testid="stSidebar"] {
    background-color: #1a1a2e;
    border-right: 4px dashed #FF007F; /* Ligne pointillée rose fluo */
}

/* Les titres avec la police Pixel Art et une ombre portée */
h1, h2, h3 {
    font-family: 'Press Start 2P', cursive !important;
    color: #00FFFF !important; /* Cyan fluo */
    text-shadow: 3px 3px #FF007F; /* Ombre rose fluo */
    margin-bottom: 20px;
    line-height: 1.5;
}

/* Texte normal pour rester lisible */
p, .stMarkdown, .stText {
    font-family: 'Courier New', Courier, monospace;
    font-size: 16px;
    color: #E0E0E0;
}

/* Style des dataframes (tableaux) */
[data-testid="stDataFrame"] {
    border: 2px solid #00FFFF;
    box-shadow: 0 0 10px #00FFFF;
}
</style>
""", unsafe_allow_html=True)

# Application du thème sombre pour les graphiques Matplotlib
plt.style.use('dark_background')

@st.cache_data
def load_data():
    df = pd.read_csv("video_games_sales.csv")
    traduction_genres = {
        'Action': 'Action', 'Role-Playing': 'Jeu de Rôle', 'Sports': 'Sport',
        'Misc': 'Divers', 'Racing': 'Course', 'Shooter': 'Tir',
        'Platform': 'Plateforme', 'Fighting': 'Combat', 'Simulation': 'Simulation',
        'Adventure': 'Aventure', 'Strategy': 'Stratégie', 'Puzzle': 'Réflexion'
    }
    df['genre'] = df['genre'].map(traduction_genres).fillna(df['genre'])
    df = df.assign(ventes_hors_na = df['global_sales'] - df['na_sales'])
    return df

df = load_data()

st.sidebar.title("🕹️ MENU P1")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "SELECT STAGE:",
    ["🎮 Start: Stats", "🏆 Boss: Plateformes", "🚀 Bonus: Tendances", "🌍 World Map"]
)

if st.sidebar.button("INSERT COIN"):
    st.balloons()
    st.sidebar.success("1 Credit Added! Ready Player One.")

st.title("👾 ANALYSE VENTES JEUX VIDÉO 👾")

if menu == "🎮 Start: Stats":
    st.header(">> LEVEL 1 : STATS GLOBALES")
    st.write("Bienvenue dans l'arène des données. Voici les scores des meilleurs joueurs du marché.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("TOP 10 ÉDITEURS")
        top_editeurs = df['publisher'].value_counts().head(10)
        st.dataframe(top_editeurs, use_container_width=True)
        
    with col2:
        st.subheader("FIABILITÉ DES GENRES")
        stats_genre = df.groupby("genre")["global_sales"].agg(['mean', 'std']).sort_values(by='mean', ascending=False)
        st.dataframe(stats_genre.round(2), use_container_width=True)

elif menu == "🏆 Boss: Plateformes":
    st.header(">> LEVEL 2 : GUERRE DES CONSOLES")
    
    region = st.selectbox("CHOISIS TA RÉGION :", ["Globales", "Amérique du Nord", "Europe", "Japon"])
    
    if region == "Globales":
        data = df.groupby("platform")["global_sales"].sum().sort_values(ascending=False).head(10)
        couleur = "#00FFFF"
    elif region == "Amérique du Nord":
        data = df.groupby("platform")["na_sales"].sum().sort_values(ascending=False).head(10)
        couleur = "#FF007F" 
    elif region == "Europe":
        data = df.groupby("platform")["eu_sales"].sum().sort_values(ascending=False).head(10)
        couleur = "#39FF14" 
    else:
        data = df.groupby("platform")["jp_sales"].sum().sort_values(ascending=False).head(10)
        couleur = "#FFFF00" 

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')
    
    data.plot(kind="bar", color=couleur, ax=ax, edgecolor="white")
    ax.set_title(f"TOP 10 PLATEFORMES - {region}", color=couleur, fontweight='bold')
    ax.set_ylabel("Ventes (Millions)", color='white')
    ax.tick_params(colors='white')
    plt.xticks(rotation=45)
    
    st.pyplot(fig)

elif menu == "🚀 Bonus: Tendances":
    st.header(">> LEVEL 3 : TENDANCES & ÉVOLUTION")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("JEU TOP 1 PAR GENRE")
        idx = df.groupby("genre")["global_sales"].idxmax()
        top = df.loc[idx].copy()
        top["label"] = top["genre"] + "\n(" + top["name"] + ")"
        top.set_index("label", inplace=True)
        
        fig1, ax1 = plt.subplots(figsize=(8, 8))
        fig1.patch.set_facecolor('#121212')
        
        couleurs_neon = ['#FF007F', '#00FFFF', '#39FF14', '#FFFF00', '#FF4500', '#8A2BE2', '#FF1493', '#00FF00', '#00BFFF', '#FFD700', '#DC143C', '#9400D3']
        
        top.plot(y="global_sales", kind="pie", colors=couleurs_neon, autopct='%1.1f%%', legend=False, ax=ax1, textprops={'color':"white", 'weight':'bold'})
        ax1.set_ylabel("")
        st.pyplot(fig1)

    with col2:
        st.subheader("TIMELINE DES VENTES")
        col_year = 'year' if 'year' in df.columns else 'Year' if 'Year' in df.columns else None
        
        if col_year:
            ventes_par_an = df.groupby(col_year)["global_sales"].sum()
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            fig2.patch.set_facecolor('#121212')
            ax2.set_facecolor('#121212')
            
            ventes_par_an.plot(kind="line", marker='s', markersize=8, color="#39FF14", linewidth=3, ax=ax2)
            ax2.set_ylabel("Ventes (Millions)", color='white')
            ax2.tick_params(colors='white')
            ax2.grid(color='#333333', linestyle='--', linewidth=1)
            st.pyplot(fig2)

elif menu == "🌍 World Map":
    st.header(">> LEVEL 4 : WORLD MAP")
    st.write("Quel est le genre roi sur chaque continent ?")
    
    top_na = df.groupby("genre")["na_sales"].sum().idxmax()
    top_eu = df.groupby("genre")["eu_sales"].sum().idxmax()
    top_jp = df.groupby("genre")["jp_sales"].sum().idxmax()
    
    data_map = [
        {'Country_Code': 'USA', 'Region': 'Amérique du Nord', 'Top_Genre': top_na},
        {'Country_Code': 'CAN', 'Region': 'Amérique du Nord', 'Top_Genre': top_na},
        {'Country_Code': 'MEX', 'Region': 'Amérique du Nord', 'Top_Genre': top_na},
        {'Country_Code': 'FRA', 'Region': 'Europe', 'Top_Genre': top_eu},
        {'Country_Code': 'DEU', 'Region': 'Europe', 'Top_Genre': top_eu},
        {'Country_Code': 'GBR', 'Region': 'Europe', 'Top_Genre': top_eu},
        {'Country_Code': 'ITA', 'Region': 'Europe', 'Top_Genre': top_eu},
        {'Country_Code': 'ESP', 'Region': 'Europe', 'Top_Genre': top_eu},
        {'Country_Code': 'JPN', 'Region': 'Japon', 'Top_Genre': top_jp}
    ]
    df_map = pd.DataFrame(data_map)
    
    fig = px.choropleth(
        df_map, locations="Country_Code", color="Top_Genre", hover_name="Region",
        projection="natural earth", 
        color_discrete_sequence=px.colors.qualitative.Set1,
        template="plotly_dark" 
    )
    
    fig.update_layout(paper_bgcolor="#121212", geo_bgcolor="#121212")
    st.plotly_chart(fig, use_container_width=True)