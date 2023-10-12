import streamlit as st
from st_pages import add_page_title
from entity.pessoa import Pessoa
from entity.role import Role
import pandas as pd
from services.upload_data import *
from streamlit_extras.switch_page_button import switch_page
from services.dataframe import *
from services.manage_role import *
from services.manage_pessoa import *

add_page_title(layout="wide")

def atualizar_dados(pessoa_transferiu : Pessoa, roles : list[Role]):
  
  for role in roles:
    valor = role.cada
    pessoa_recebeu = role.pagou

    pessoa_transferiu.saldo_pagou += valor
    pessoa_recebeu.saldo_recebido += valor
    role.transferiu.append(pessoa_transferiu)

    atualizar_pessoa(pessoa_transferiu)
    atualizar_pessoa(pessoa_recebeu)
    atualizar_role(role)


def main():
  roles = upload_roles()
  roles_df = roles_to_df()
  pessoas = upload_pessoas()

  ### seleciona a pessoa
  pessoa = st.selectbox("Escolha a pessoa que ira transferir: ", [p.nome for p in pessoas])
  pessoa_obj = pessoa_name_to_obj(pessoa, pessoas)


  ### define quais roles ela ainda nao transferiu
  roles_validos = []
  for i, role in roles_df.iterrows():
    if pessoa in role['envolvidos'] and pessoa not in role['transferiu'] and pessoa != role['pagou']:
      roles_validos.append(role)

  ### seleciona o role
  choice_role = st.multiselect("Selecione qual ou quais roles voce gostaria de quitar as dividas:", [r.nome for r in roles_validos])
  choice_roles_obj = [role_name_to_obj(x, roles) for x in choice_role]

  ### calcula a divida -> (pessoa, quantidade)
  transf = {}
  for r in choice_role:
    for i, each in roles_df.iterrows():
      if each['nome'] == r:
        if each['pagou'] not in transf: transf[each['pagou']] = each['valor para cada']
        else: transf[each['pagou']] += each['valor para cada']

  ### mostra o valor da divida e para quem deve
  ans = True
  for key, value in transf.items():
    choice = st.radio(f":ballot_box_with_check: O valor para quitar a divida com **{key}** eh **R$ {value:.2f}**. Deseja transferir essa valor?", ["Sim", "Nao"])
    ans &= (choice == "Sim")

  ### se confirma a transacao, atualiza os dados
  if ans:
    if st.button("Enviar"): 
      atualizar_dados(pessoa_obj, choice_roles_obj)
      switch_page("Depois te pago")
  ### se nao confirma recebe um warning
  else:
    st.button("Enviar", disabled=st.session_state.get("disabled", True))
    st.error("Eh preciso confirmar as transacoes para finalizar.")

      
if __name__ == "__main__":
  main()