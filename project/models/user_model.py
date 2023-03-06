from core.configs import settings
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship

class UserModel(settings.DBBaseModel):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,autoincrement=True, nullable=False)
    name = Column(String(70),nullable=True)
    surname = Column(String(100),nullable=True)
    email = Column(String(100),index=True,nullable=False,unique=True)
    password = Column(String(256),nullable=False)
    is_admin = Column(Boolean,default=False)
    games = relationship("GameModel",cascade="all, delete-orphan",back_populates="criador",uselist=True,lazy="joined")
