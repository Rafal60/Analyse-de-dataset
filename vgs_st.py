import pandas as pd
import streamlit as st

st.write("Streamlit demo")

df = pd.read_csv("video_games_sales.csv")
st.write(df)