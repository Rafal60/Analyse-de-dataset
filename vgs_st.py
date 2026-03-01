import pandas as pd
import streamlit as st
import plotly.express as px

# Configuration page
st.set_page_config(
    page_title="Video Games Sales Dashboard",
    layout="wide"
)

# Chargement données
@st.cache_data
def load_data():
    df = pd.read_csv("video_games_sales.csv")
    df = df.dropna(subset=["year", "global_sales"])
    df["year"] = df["year"].astype(int)

    # assign nouvelle colonne
    df = df.assign(
        eu_ratio = df["eu_sales"] / df["global_sales"]
    )

    # apply nouvelle colonne
    def classify_sales(x):
        if x > 10:
            return "Blockbuster"
        elif x > 1:
            return "Hit"
        else:
            return "Normal"

    df["success"] = df["global_sales"].apply(classify_sales)

    return df

df = load_data()


# Titre
st.title("🎮 Video Games Sales Dashboard")

st.sidebar.header("Filtres")

# slider dynamique années
min_year = int(df["year"].min())
max_year = int(df["year"].max())

year_range = st.sidebar.slider(
    "Choisir une période",
    min_year,
    max_year,
    (min_year, max_year)
)
st.write(f"Années sélectionnées : {year_range[0]} - {year_range[1]}")

# Filtre plateforme
platform = st.sidebar.multiselect(
    "Choisir plateforme",
    df["platform"].unique(),
    default=df["platform"].unique()
)

# Filtre genre
genre = st.sidebar.multiselect(
    "Choisir genre",
    df["genre"].unique(),
    default=df["genre"].unique()
)

df_filtered = df[
    (df["platform"].isin(platform)) &
    (df["genre"].isin(genre)) &
    (df["year"].between(year_range[0], year_range[1]))
]

add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Dataset
st.subheader("Dataset filtré")
st.dataframe(df_filtered)

# KPI
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total ventes",
    f"{df_filtered['global_sales'].sum():.2f} M"
)

col2.metric(
    "Moyenne ventes",
    f"{df_filtered['global_sales'].mean():.2f} M"
)

col3.metric(
    "Nombre jeux",
    len(df_filtered)
)

# groupby sum
sales_platform = df_filtered.groupby("platform")["global_sales"].sum().reset_index()

# Graphique bar
fig_bar = px.bar(
    sales_platform.sort_values("global_sales", ascending=False),
    x="platform",
    y="global_sales",
    title="Ventes par plateforme"
)

st.plotly_chart(fig_bar, use_container_width=True)

# groupby mean
sales_year = df_filtered.groupby("year")["global_sales"].sum().reset_index()

# Graphique courbe
fig_line = px.line(
    sales_year,
    x="year",
    y="global_sales",
    title="Evolution des ventes par année"
)

st.plotly_chart(fig_line, use_container_width=True)

# Ventes par genre
sales_genre = df_filtered.groupby("genre", as_index=False)["global_sales"].sum()

fig_pie = px.pie(
    sales_genre,
    values="global_sales",
    names="genre",
    title="Répartition des ventes par genre"
)

st.plotly_chart(fig_pie, use_container_width=True)

# value_counts
st.subheader("Nombre de jeux par plateforme")
st.write(df_filtered["platform"].value_counts())

# groupby mean et std
st.subheader("Statistiques par genre")

stats = df_filtered.groupby("genre")["global_sales"].agg(
    ["mean", "sum", "std"]
)

st.dataframe(stats)

# Top jeux
st.subheader("Top 10 jeux")
top_games = df_filtered.sort_values(
    "global_sales",
    ascending=False
).head(10)

st.dataframe(top_games)