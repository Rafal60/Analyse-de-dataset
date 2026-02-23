import pandas as pd

# | rank | name | platform | year | genre | publisher | na_sales | eu_sales | jp_sales| other_sales | global_sales |

df = pd.read_csv("video_games_sales.csv")
df.head()

