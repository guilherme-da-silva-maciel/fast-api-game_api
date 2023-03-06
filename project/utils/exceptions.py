class EqualEmailError(Exception):
    def __init__(self,email) -> None:
      self.message = f"Este email já esta cadastrado a um usuario!\nPor favor tente um email diferente ou acesse a aba de login"
      print(self.message)
