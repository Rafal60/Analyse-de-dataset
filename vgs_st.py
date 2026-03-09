import pandas as pd
import matplotlib.pyplot as plt

# Lecture des données
df = pd.read_csv("video_games_sales.csv")

# --- PRÉPARATION DES DONNÉES ---
# Correction : groupement par "platform" pour être cohérent avec le nom de tes fonctions
saleGlobalConsole = df.groupby("platform")["global_sales"].sum().sort_values(ascending=False)
salesUs = df.groupby("platform")["na_sales"].sum().sort_values(ascending=False)
saleEu = df.groupby("platform")["eu_sales"].sum().sort_values(ascending=False)
saleJp = df.groupby("platform")["jp_sales"].sum().sort_values(ascending=False)

groupbyGenre = df.groupby("genre")["global_sales"].sum().sort_values(ascending=False)

# --- FONCTIONS D'AFFICHAGE ---
def ventesGlobalconsole(tableauConsole):
    top = tableauConsole.head(10)
    ax = top.plot(kind="bar", color="tab:blue")
    ax.set_title("Top plateformes par ventes globales")
    ax.set_xlabel("Plateforme")
    ax.set_ylabel("Ventes globales (millions)")
    plt.tight_layout()
    plt.show()

def ventesUsConsole(tableauConsole):
    top = tableauConsole.head(10)
    ax = top.plot(kind="bar", color="tab:orange")
    ax.set_title("Top plateformes par ventes aux USA")
    ax.set_xlabel("Plateforme")
    ax.set_ylabel("Ventes USA (millions)")
    plt.tight_layout()
    plt.show()
    
def ventesEuConsole(tableauConsole):
    # Remplacé par head(10) pour avoir vraiment les 10 meilleurs
    top = tableauConsole.head(10)
    ax = top.plot(kind="bar", color="tab:green")
    ax.set_title("Top plateformes par ventes en Europe")
    ax.set_xlabel("Plateforme")
    ax.set_ylabel("Ventes Europe (millions)")
    plt.tight_layout()
    plt.show()  
    
def ventesJpConsole(tableauConsole):
    # Remplacé par head(10) pour avoir vraiment les 10 meilleurs
    top = tableauConsole.head(10)
    ax = top.plot(kind="bar", color="tab:red")
    ax.set_title("Top plateformes par ventes au Japon")
    ax.set_xlabel("Plateforme")
    ax.set_ylabel("Ventes Japon (millions)")
    plt.tight_layout()
    plt.show()
    
def ventesGenreConsole(tableauGenre):
    top = tableauGenre
    ax = top.plot(kind="bar", color="tab:purple")
    ax.set_title("Top genres par ventes globales")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Ventes globales (millions)")
    plt.tight_layout()
    plt.show()

def topJeuparGenre():
    # 1. On trouve la ligne du jeu le plus vendu pour chaque genre
    idx = df.groupby("genre")["global_sales"].idxmax()
    top = df.loc[idx].copy()
    
    # 2. On crée une belle étiquette combinant le genre et le nom du jeu
    top["label"] = top["genre"] + "\n(" + top["name"] + ")"
    top.set_index("label", inplace=True)
    
    # 3. Création du camembert avec "global_sales" en Y
    ax = top.plot(
        y="global_sales", 
        kind="pie", 
        color="tab:cyan", 
        autopct='%1.1f%%', # Affiche les pourcentages
        legend=False, 
        figsize=(10, 8)    # Agrandit la figure pour la lisibilité
    )
    
    ax.set_title("Jeu le plus vendu par genre")
    ax.set_ylabel("") # Supprime le texte "global_sales" à gauche du camembert
    plt.tight_layout()
    plt.show()
    
# --- EXÉCUTION ---
# On appelle les fonctions sans 'print()'
# ventesGlobalconsole(saleGlobalConsole)
topJeuparGenre()