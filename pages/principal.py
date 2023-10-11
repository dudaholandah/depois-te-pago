import streamlit as st
from st_pages import Page, show_pages, add_page_title
from services.upload_data import *
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

add_page_title(layout="wide")

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
  
  df = df.copy()

  modification_container = st.container()
  with modification_container:
    to_filter_columns = st.multiselect("Defina um filtro:", df.columns)

  for column in to_filter_columns:
    left, right = st.columns((1, 20))
    left.write("↳")

    if is_numeric_dtype(df[column]):
      _min = float(0)
      _max = float(df[column].max())
      step = (_max - _min) / 100
      user_num_input = right.slider(
        f"Valores para {column}",
        min_value=_min,
        max_value=_max,
        value=(_min, _max),
        step=step,
      )
      df = df[df[column].between(*user_num_input)]
    elif not df[column].empty and isinstance(df[column].iloc[0], list):
      values = []

      for mlist in df[column]:
        for p in mlist:
          if p not in values: 
            values.append(p)

      user_cat_input = right.multiselect(
          f"Valores para {column}",
          values,
          default=list(values),
      )
    else:
      user_cat_input = right.multiselect(
          f"Valores para {column}",
          df[column].unique(),
          default=list(df[column].unique()),
      )
      df = df[df[column].isin(user_cat_input)]

  return df

def write_df(df : pd.DataFrame):
  if not df.empty:
    df.set_index('nome', inplace=True)

  df = df.copy()

  for column in df.columns:
    if is_numeric_dtype(df[column]):
      df[column] = df[column].map(lambda x : f"R$ {x:.2f}" if x >= 0 else f"- R$ {abs(x):.2f}")

  st.write(df)

def main():
  
  st.subheader(":running: Tabela de roles")
  
  df_roles = roles_to_df()
  df_roles = filter_dataframe(df_roles)

  write_df(df_roles)

  st.subheader(":money_with_wings: Tabela de saldos individuais")
  
  df_individual = pessoas_to_df()
  df_individual = filter_dataframe(df_individual)

  write_df(df_individual)


if __name__ == "__main__":
  main()