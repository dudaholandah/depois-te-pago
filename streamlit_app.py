import streamlit as st
from st_pages import Page, show_pages, add_page_title
from upload_data import *

show_pages(
  [
    Page("streamlit_app.py", "Depois te pago", "🏠"),
    Page("adicionar_role.py", "Adicionar role", ":heavy_plus_sign:"),
    Page("transferir_valor.py", "Transferir valor", ":heavy_dollar_sign:")
  ]
)

add_page_title(layout="wide")

def main():
  
  df_roles = roles_to_df()

  st.subheader(":running: Tabela de roles")
  st.write(df_roles) 

  df_individual = pessoas_to_df()

  st.subheader(":money_with_wings: Tabela de saldos individuais")
  st.write(df_individual)  


if __name__ == "__main__":
  main()