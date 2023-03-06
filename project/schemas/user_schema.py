from typing import Optional,List
from pydantic import BaseModel,EmailStr
from schemas.game_schemas import GameSchema

class UserSchemaBase(BaseModel):
    id:Optional[int] = None
    name:str
    surname:str
    email:EmailStr
    is_admin:bool = False

    class Config:
        orm_mode = True

class UserSchemaCreate(UserSchemaBase):
    password:str

class UserSchemaGames(UserSchemaBase):
    games:Optional[List[GameSchema]]

class UserSchemaUp(UserSchemaBase):
    name:Optional[str]
    surname:Optional[str]
    email:Optional[EmailStr]
    password:Optional[str]
    is_admin:Optional[bool]
