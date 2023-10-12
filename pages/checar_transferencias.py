from st_pages import add_page_title
from services.upload_data import *
import streamlit as st
from services.dataframe import *

add_page_title(layout="wide")

def filter_pessoa(df : pd.DataFrame, df_role : pd.DataFrame):

  df = df.copy()
  column = 'nome'

  input = st.selectbox(
          f"Escolha a pessoa que voce deseja checar as transferencias:",
          df[column].unique(),
      )
  
  df = filtrar_roles_por_nome(df_role, input)  

  return df, input

def filtrar_roles_por_nome(df, nome):
  condicao = (df['envolvidos'].apply(lambda x: nome in x))
  df_filtered = df[condicao]
  return df_filtered

def write_transferencias(df : pd.DataFrame, pessoa : str):

  transf = {}
  for i, each in df.iterrows():
    if pessoa != each['pagou'] and pessoa not in each['transferiu']:
      if each['pagou'] not in transf: transf[each['pagou']] = each['valor para cada']
      else: transf[each['pagou']] += each['valor para cada']
      

  st.caption(":ballot_box_with_check: Saldo para transferir:")
  for key, value in transf.items():
    st.write(key, "⟶", f"R$ {value:.2f}")



def main():
  df_pessoas = pessoas_to_df()
  df_roles = roles_to_df()

  df_pessoa, pessoa = filter_pessoa(df_pessoas, df_roles)
  
  st.divider()
  
  write_df(df_pessoa)
  
  st.divider()

  write_transferencias(df_pessoa, pessoa)


if __name__ == "__main__":
  main()