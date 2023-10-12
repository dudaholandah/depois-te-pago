from entity.pessoa import Pessoa
class Role:
  def __init__(self, idx, nome, pagou : Pessoa, valor, envolvidos : list[Pessoa], transferiu : list[Pessoa], cada):
    self.idx = idx
    self.nome = nome
    self.pagou = pagou
    self.valor = valor
    self.envolvidos = envolvidos
    self.transferiu = transferiu
    self.cada = cada

  def atualizar_pessoas(self):
    self.pagou.saldo_pagou += self.valor
    self.pagou.saldo_envolvido += self.cada 
    
    for each in self.envolvidos:
      if each != self.pagou:
        each.saldo_envolvido += self.cada