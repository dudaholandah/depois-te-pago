import streamlit as st
from st_pages import add_page_title
from entity.pessoa import Pessoa
from entity.role import Role
import pandas as pd
from services.upload_data import *
from streamlit_extras.switch_page_button import switch_page


add_page_title(layout="wide")

def atualizar_pessoa(transferiu : Pessoa, recebeu : Pessoa, role: Role, valor):

  pessoas = upload_pessoas()
  roles = upload_roles()

  for pessoa in pessoas:
    if pessoa.nome == transferiu.nome:
      pessoa.saldo_pagou += valor
    elif pessoa.nome == recebeu.nome:
      pessoa.saldo_recebido += valor


  for each in roles:
    if each.nome == role.nome:
      each.transferiu.append(transferiu)

  dict_pessoas = [obj.__dict__ for obj in pessoas]
  dict_roles = [{"idx": obj.idx,
                "nome": obj.nome,
                "pagou" : obj.pagou.__dict__,
                "valor" : obj.valor,
                "envolvidos" : [item.__dict__ for item in obj.envolvidos],
                "transferiu" : [item.__dict__ for item in obj.transferiu],
                "cada" : obj.cada} 
                for obj in roles]

  with open('data/pessoas.json', 'w') as json_file:
    json.dump(dict_pessoas, json_file, indent=2)

  with open('data/roles.json', 'w') as json_file:
    json.dump(dict_roles, json_file, indent=2)


def main():
  roles = upload_roles()
  pessoas = upload_pessoas()

  if len(roles) == 0:
    st.write("Voce nao criou ainda nenhum role.")
  else:
    role = st.selectbox("Selecione um role:", [role.nome for role in roles])

    for each in roles:
      if each.nome == role:
        role_obj = each

    pessoas_validas = []

    for pessoa in pessoas:
      if pessoa.nome != role_obj.pagou.nome and pessoa.nome not in [p.nome for p in role_obj.transferiu]:
        pessoas_validas.append(pessoa.nome)

    pessoa = st.selectbox("Escolha a pessoa que ira transferir:", pessoas_validas)

    for each in pessoas:
      if each.nome == pessoa:
        pessoa_obj = each

    choice = st.radio(f"O valor para quitar a divida eh R$ {role_obj.cada:.2f}. Deseja transferir essa valor?", ["Sim", "Nao"])

    if choice == "Nao":
      valor = st.number_input("Digite o valor que deseja transferir.")
    else:
      valor = role_obj.cada

    if st.button("Enviar"):
      atualizar_pessoa(pessoa_obj, role_obj.pagou, role_obj, valor)
      switch_page("Depois te pago")
      
if __name__ == "__main__":
  main()