import pandas as pd
import matplotlib.pyplot as plt
# | rank | name | platform | year | genre | publisher | na_sales | eu_sales | jp_sales| other_sales | global_sales |

df = pd.read_csv("video_games_sales.csv")
df.head()

saleByConsole=df.groupby("platform")["global_sales"].sum().sort_values(ascending=False)

top = saleByConsole
ax = top.plot(kind="bar", color="tab:blue")
ax.set_title("Top plateformes par ventes globales")
ax.set_xlabel("Plateforme")
ax.set_ylabel("Ventes globales (millions)")
plt.tight_layout()
plt.show()

