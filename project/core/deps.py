from typing import Generator,Optional
from fastapi import Depends,HTTPException,status
from jose import jwt,JWTError
from sqlalchemy.future import select
from core.auth import outh2_schema
from core.configs import settings
from pydantic import BaseModel
from models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session

class TokenData(BaseModel):
    username: Optional[str] = None


async def get_session() -> Generator:
    session:AsyncSession = Session()

    try:
        yield session
    
    finally:
        await session.close()

  
async def get_current_user(db: Session = Depends(get_session),token:str = Depends(outh2_schema)) -> UserModel:
    credantial_exception:HTTPException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Credenciais inválidas, por favor tente novamente",headers={"WWW-Bearer"})

    try:
        payload = jwt.decode(token,settings.JWT_SECRET,algorithms=[settings.ALGORITHM],options={"verify_aud":False})

        username:str = payload.get("sub")

        if username is None:
            raise credantial_exception
        
        token_data:TokenData = TokenData(username=username)

    except JWTError:
        raise credantial_exception
    
    async with db as session:
        query = select(UserModel).filter(UserModel.id == int(token_data.username))
        result = await session.execute(query)

        user:UserModel = result.scalars().unique().one_or_none() 

        if user is None:
            raise credantial_exception
        
        return user

