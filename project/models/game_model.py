from core.configs import settings
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship

class GameModel(settings.DBBaseModel):
    __tablename__ = 'games'

    id:int = Column(Integer,primary_key=True,autoincrement=True)
    nome:str = Column(String(50))
    ano_lancamento:int = Column(Integer)
    nota:int = Column(Integer)
    lista_desejo:bool = Column(Boolean,nullable=True)
    genero:str = Column(String(30))
    classificacao_indicativa:str = Column(String(3))
    criador_id = Column(Integer,ForeignKey('users.id'))
    criador = relationship("UserModel",back_populates='games',lazy="joined")

