import pandas as pd
import matplotlib.pyplot as plt
# | rank | name | platform | year | genre | publisher | na_sales | eu_sales | jp_sales| other_sales | global_sales |

df = pd.read_csv("video_games_sales.csv")
df.head()


saleGlobalConsole=df.groupby("publisher").sum(["global_sales"]).sort_values("global_sales", ascending=False)
salesUs=df.groupby("publisher")["na_sales"].sum().sort_values(ascending=False)
saleEu=df.groupby("platform")["eu_sales"].sum().sort_values(ascending=False)
saleJp=df.groupby("platform")["jp_sales"].sum().sort_values(ascending=False)

groupbyGenre=df.groupby("genre")["global_sales"].sum().sort_values(ascending=False)



def ventesGlobalconsole(tableauConsole):
    top = tableauConsole.head(10)
    ax = top.plot(kind="bar", color="tab:blue")
    ax.set_title("Top plateformes par ventes globales")
    ax.set_xlabel("Plateforme")
    ax.set_ylabel("Ventes globales (millions)")
    plt.tight_layout()
    plt.show()

def ventesUsConsole(tableauConsole):
    top=tableauConsole.head(10)
    ax = top.plot(kind="bar", color="tab:orange")
    ax.set_title("Top plateformes par ventes aux USA")
    ax.set_xlabel("Plateforme")
    ax.set_ylabel("Ventes USA (millions)")
    plt.tight_layout()
    plt.show()
    
def ventesEuConsole(tableauConsole):
    top=tableauConsole.head(len(tableauConsole)-10)
    ax = top.plot(kind="bar", color="tab:green")
    ax.set_title("Top plateformes par ventes en Europe")
    ax.set_xlabel("Plateforme")
    ax.set_ylabel("Ventes Europe (millions)")
    plt.tight_layout()
    plt.show()  
    
def ventesJpConsole(tableauConsole):
    top=tableauConsole.head(len(tableauConsole)-10)
    ax = top.plot(kind="bar", color="tab:red")
    ax.set_title("Top plateformes par ventes au Japon")
    ax.set_xlabel("Plateforme")
    ax.set_ylabel("Ventes Japon (millions)")
    plt.tight_layout()
    plt.show()
    
def ventesGenreConsole(tableauGenre):
    top=tableauGenre
    ax = top.plot(kind="bar", color="tab:purple")
    ax.set_title("Top genres par ventes globales")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Ventes globales (millions)")
    plt.tight_layout()
    plt.show()

print(ventesUsConsole(salesUs))