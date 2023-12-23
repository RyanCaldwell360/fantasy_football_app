import pandas as pd
import streamlit as st

df = pd.read_csv('../backend/data_extraction/data/matchup_results.csv', nrows=10)

st.write('Sample of weekly matchups')
st.dataframe(df)