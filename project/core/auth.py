from pytz import timezone
from typing import Optional,List
from datetime import datetime,timedelta
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.user_model import UserModel
from core.configs import settings
from core.security import verify_password
from pydantic import EmailStr

outh2_schema = OAuth2AuthorizationCodeBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login",
    authorizationUrl=f"{settings.API_V1_STR}/users/login"
)

async def authenticate(email:EmailStr,password:str,db:AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)

        result = await session.execute(query)

        user:UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None
        
        if not verify_password(password=password,password_hash=user.password):
            return None
        
        return user
    
def _create_token(token_type:str,lifetime:timedelta,sub:str) -> str:
    payload = {}

    sp = timezone('America/Sao_Paulo')
    expire = datetime.now(tz=sp) + lifetime

    payload['type'] = token_type
    payload['exp'] = expire
    payload['iat'] = datetime.now(tz=sp)
    payload['sub'] = str(sub) 

    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.ALGORITHM)

def create_token_access(sub:str):
    return _create_token(token_type='access_token',lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),sub=sub)

    
