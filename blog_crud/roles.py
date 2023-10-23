from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {'criar_posts' : True, 'editar_posts' : True,}

class Convidado(AbstractUserRole):
    available_permissions = { 'acessar_posts': True, 'ver_posts' : True}