from entity.pessoa import Pessoa
from services.upload_data import *
import streamlit as st

def pessoa_name_to_obj(nome : str, pessoas : list[Pessoa]):

  for pessoa in pessoas:
    if pessoa.nome == nome:
      return pessoa
    
  raise Exception("Nome nao encontrado no banco de dados.")

def pessoa_obj_to_dict(pessoa : Pessoa):
  return pessoa.__dict__

def copy_pessoa(p1 : Pessoa, p2 : Pessoa):
  p1.nome = p2.nome
  p1.saldo_envolvido = p2.saldo_envolvido
  p1.saldo_pagou = p2.saldo_pagou
  p1.saldo_recebido = p2.saldo_recebido

def atualizar_pessoa(pessoa : Pessoa):
  pessoas = upload_pessoas()

  for p in pessoas:
    if p.nome == pessoa.nome:
      copy_pessoa(p, pessoa) 

  dict_pessoas = [pessoa_obj_to_dict(p) for p in pessoas]

  with open('data/pessoas.json', 'w') as json_file:
    json.dump(dict_pessoas, json_file, indent=2)