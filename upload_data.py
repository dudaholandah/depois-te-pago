from pessoa import Pessoa
from role import Role
import pandas as pd
import json

def popular_dados():

  pessoas : list[Pessoa] = [Pessoa("Bruno", 0, 0, 0), Pessoa("Duda", 0, 0, 0)]
  roles : list[Role] = [Role(0, "cachorro quente", pessoas[0], 30, pessoas)]

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

def criar_pessoa_from_dict(d):
  return Pessoa(**d)

def criar_role_from_dict(d : Role):
  envolvidos = [criar_pessoa_from_dict(p) for p in d["envolvidos"]]
  transferiu = [criar_pessoa_from_dict(p) for p in d["transferiu"]]
  pagou = criar_pessoa_from_dict(d["pagou"])
  return Role(d["idx"], d["nome"], pagou, d["valor"], envolvidos, transferiu, d["cada"])

def upload_pessoas():
  with open('data/pessoas.json', 'r') as json_file:
    pessoas_json = json.load(json_file)

  return [criar_pessoa_from_dict(d) for d in pessoas_json]

def pessoas_to_df():
  pessoas = upload_pessoas()
  
  data = [{"nome": pessoa.nome,
        "pago por voce": f"R$ {pessoa.saldo_pagou:.2f}",
        "sua parte": f"R$ {pessoa.saldo_envolvido:.2f}",
        "saldo recebido": f"R$ {pessoa.saldo_recebido:.2f}"} 
        for pessoa in pessoas]

  df = pd.DataFrame(data)
  if not df.empty:
    df.set_index('nome', inplace=True)

  return df 
  

def upload_roles():
  with open('data/roles.json', 'r') as json_file:
    roles_json = json.load(json_file)

  return [criar_role_from_dict(d) for d in roles_json]

def roles_to_df():
  roles = upload_roles()

  data = [{"nome": role.nome,
          "valor": f"R$ {role.valor:.2f}",
          "pagou": role.pagou.nome,
          "envolvidos": [pessoa.nome for pessoa in role.envolvidos],
          "transferiu": [pessoa.nome for pessoa in role.transferiu]}
          for role in roles]

  df = pd.DataFrame(data)
  if not df.empty:
    df.set_index('nome', inplace=True)

  return df

  