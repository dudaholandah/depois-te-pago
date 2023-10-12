import streamlit as st
import pandas as pd
from pandas.api.types import is_numeric_dtype

def write_df(df : pd.DataFrame):
  if not df.empty:
    df.set_index('nome', inplace=True)

  df = df.copy()

  for column in df.columns:
    if is_numeric_dtype(df[column]):
      df[column] = df[column].map(lambda x : f"R$ {x:.2f}" if x >= 0 else f"- R$ {abs(x):.2f}")

  st.write(df)