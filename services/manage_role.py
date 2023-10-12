from entity.role import Role
from services.manage_pessoa import *

def role_name_to_obj(nome : str, roles : list[Role]):
  for role in roles:
    if role.nome == nome:
      return role
    
  raise Exception("Nome nao encontrado no banco de dados.")

def role_obj_to_dict(role : Role):
  return {"idx": role.idx,
          "nome": role.nome,
          "pagou": pessoa_obj_to_dict(role.pagou),
          "valor": role.valor,
          "envolvidos": [pessoa_obj_to_dict(item) for item in role.envolvidos],
          "transferiu": [pessoa_obj_to_dict(item) for item in role.transferiu],
          "cada": role.cada} 

def copy_role(r1 : Role, r2 : Role):
  r1.idx = r2.idx
  r1.nome = r2.nome
  r1.pagou = r2.pagou
  r1.valor = r2.valor
  r1.envolvidos = r2.envolvidos
  r1.transferiu = r2.transferiu
  r1.cada = r2.cada

def atualizar_role(role : Role):
  roles = upload_roles()

  for r in roles:
    if r.nome == role.nome:
      copy_role(r, role)

  dict_roles = [role_obj_to_dict(r) for r in roles]

  with open('data/roles.json', 'w') as json_file:
    json.dump(dict_roles, json_file, indent=2)           