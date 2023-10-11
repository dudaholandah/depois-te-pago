import streamlit as st
from st_pages import add_page_title
from services.upload_data import *
from entity.role import Role
from streamlit_extras.switch_page_button import switch_page

add_page_title(layout="wide")

def adicionar_role(role : Role):

  roles = upload_roles()
  roles.append(role)

  dict_roles = [{"idx": obj.idx,
                "nome": obj.nome,
                "pagou" : obj.pagou.__dict__,
                "valor" : obj.valor,
                "envolvidos" : [item.__dict__ for item in obj.envolvidos],
                "transferiu" : [item.__dict__ for item in obj.transferiu],
                "cada" : obj.cada} 
                for obj in roles]

  with open('data/roles.json', 'w') as json_file:
    json.dump(dict_roles, json_file, indent=2)

def atualizar_pessoa(role : Role):

  pessoas = upload_pessoas()

  for pessoa in pessoas:
    if pessoa.nome == role.pagou.nome:
      pessoa.saldo_pagou += role.valor
    
    if pessoa.nome in [each.nome for each in role.envolvidos]:
      pessoa.saldo_envolvido += role.cada

  dict_pessoas = [obj.__dict__ for obj in pessoas]

  with open('data/pessoas.json', 'w') as json_file:
    json.dump(dict_pessoas, json_file, indent=2)

def main():

  pessoas = upload_pessoas()

  nome = st.text_input("Nome:")
  valor = st.number_input("Valor:")
  pagou = st.selectbox("Quem pagou:", [pessoa.nome for pessoa in pessoas])
  envolvidos = st.multiselect("Envolvidos:", [pessoa.nome for pessoa in pessoas])

  pessoas_envolvidas = []

  for pessoa in pessoas:
    if pessoa.nome == pagou:
      pessoa_pagou = pessoa
    if pessoa.nome in envolvidos:
      pessoas_envolvidas.append(pessoa)
  
  cada = 0 if len(pessoas_envolvidas) == 0 else ( valor / len(pessoas_envolvidas) )
  role = Role(0, nome, pessoa_pagou, valor, pessoas_envolvidas, [], cada)

  if st.button("Enviar"):
    atualizar_pessoa(role)
    adicionar_role(role)
    switch_page("Depois te pago")

if __name__ == "__main__":
  main()