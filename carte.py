import pandas as pd
import plotly.express as px

# (Assure-toi que df est bien chargé avec ton pd.read_csv avant ça)

def carteMondialeGenres(df):
    # 1. On calcule le genre qui a généré le plus de ventes pour chaque région
    top_na = df.groupby("genre")["na_sales"].sum().idxmax()
    top_eu = df.groupby("genre")["eu_sales"].sum().idxmax()
    top_jp = df.groupby("genre")["jp_sales"].sum().idxmax()
    
    # 2. On crée un tableau artificiel pour lier ces régions à des vrais pays 
    # Plotly a besoin des codes pays en 3 lettres (ISO-3) pour dessiner la carte.
    data_map = [
        # Amérique du Nord
        {'Country_Code': 'USA', 'Region': 'Amérique du Nord', 'Top_Genre': top_na},
        {'Country_Code': 'CAN', 'Region': 'Amérique du Nord', 'Top_Genre': top_na},
        {'Country_Code': 'MEX', 'Region': 'Amérique du Nord', 'Top_Genre': top_na},
        # Europe (quelques pays principaux pour l'exemple)
        {'Country_Code': 'FRA', 'Region': 'Europe', 'Top_Genre': top_eu},
        {'Country_Code': 'DEU', 'Region': 'Europe', 'Top_Genre': top_eu}, # Allemagne
        {'Country_Code': 'GBR', 'Region': 'Europe', 'Top_Genre': top_eu}, # Royaume-Uni
        {'Country_Code': 'ITA', 'Region': 'Europe', 'Top_Genre': top_eu},
        {'Country_Code': 'ESP', 'Region': 'Europe', 'Top_Genre': top_eu},
        # Japon
        {'Country_Code': 'JPN', 'Region': 'Japon', 'Top_Genre': top_jp}
    ]
    
    # On transforme notre petit dictionnaire en DataFrame
    df_map = pd.DataFrame(data_map)
    
    # 3. Création de la carte mondiale
    fig = px.choropleth(
        df_map,
        locations="Country_Code",   # La colonne avec les codes pays (USA, FRA...)
        color="Top_Genre",          # La colonne qui va déterminer la couleur
        hover_name="Region",        # Le texte qui s'affiche quand on passe la souris
        title="Genre de jeux vidéo le plus populaire par grande région",
        projection="natural earth", # Un style de carte plus arrondi et naturel
        color_discrete_sequence=px.colors.qualitative.Pastel # Des couleurs douces
    )
    
    # On affiche la carte dans le navigateur web
    fig.write_html("ma_carte.html")
    print("La carte a été générée avec succès ! Ouvre le fichier 'ma_carte.html'.")

# --- Exécution ---
#carteMondialeGenres(df)