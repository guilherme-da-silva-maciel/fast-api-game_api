from typing import Optional

from pydantic import BaseModel as SCBaseModel

class GameSchema(SCBaseModel):
    nome: str
    ano_lancamento: int
    nota:int
    lista_desejo:Optional[bool] = ...
    genero:str
    classificacao_indicativa:str
    criador_id:str
    # criador:str

    class Config:
        orm_mode = True
