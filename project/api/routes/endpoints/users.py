from typing import List,Optional,Any
from fastapi import APIRouter,status,Depends,HTTPException,Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase,UserSchemaCreate,UserSchemaUp,UserSchemaGames
from core.deps import get_current_user,get_session
from core.security import generate_hash_password
from core.auth import authenticate,create_token_access
from utils.exceptions import EqualEmailError

router = APIRouter()

@router.get('/logged',response_model=UserSchemaBase)
def get_logged(user_logged:UserModel = Depends(get_current_user)):
    return user_logged

@router.post('/signup',status_code=status.HTTP_201_CREATED,response_model=UserSchemaBase)
async def post_user(user:UserSchemaCreate,db:AsyncSession = Depends(get_session)):
    new_user:UserModel = UserModel(name=user.name,surname=user.surname,email=user.email,password=generate_hash_password(user.password),is_admin=user.is_admin)

    async with db as session:
        query = select(UserModel).filter(UserModel.email == user.email)
        result = await session.execute(query)
        email = result.scalars().unique().one_or_none()

        if email:
            raise HTTPException(detail="Este email já esta cadastrado a um usuario!\nPor favor tente um email diferente ou acesse a aba de login",status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        else:
            session.add(new_user)
            await session.commit()

            return new_user

@router.get('/',response_model=List[UserSchemaBase],status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_session),user_logged:UserModel = Depends(get_current_user)):
    async with db as session:
        if user_logged.is_admin == True:
            query = select(UserModel)
            result = await session.execute(query)
            users:List[UserSchemaBase] = result.scalars().unique().all()

            return users
        
        else :
            raise HTTPException(detail="Você não tem permissão para acessar este recurso\npor favor contate a administração se achar isso um erro",status_code=status.HTTP_403_FORBIDDEN)
        
@router.get('/{user_id}',status_code=status.HTTP_200_OK,response_model=UserSchemaGames)
async def get_user(user_id:int,db:AsyncSession = Depends(get_session),user_logged:UserModel = Depends(get_current_user)):
    async with db as session:        
        if user_logged.is_admin == True or user_logged.id == user_id:
            query = select(UserModel).filter(UserModel.id == user_id)
            result = await session.execute(query)
            user:UserSchemaGames = result.scalars().unique().one_or_none()

            if user:
                return user
            
            else:
                raise HTTPException(detail="Usuario não encontrado",status_code=status.HTTP_404_NOT_FOUND)
        
        else:
            raise HTTPException(detail="Você não tem permissão para acessar este recurso,por favor contate a administração se achar isso um erro",status_code=status.HTTP_403_FORBIDDEN)
        
@router.put('/{user_id}',status_code=status.HTTP_202_ACCEPTED,response_model=UserSchemaUp)
async def put_user(user:UserSchemaUp,user_id:int,db:AsyncSession=Depends(get_session),user_logged:UserModel=Depends(get_current_user)):
    async with db as session:
        if user_logged.is_admin == True or user_logged.id == user_id:
            query = select(UserModel).filter(UserModel.id == user_id)
            result = await session.execute(query)
            user_updated:UserSchemaUp = result.scalars().unique().one_or_none()

            if user_updated:
                if user.password:
                    user.password = generate_hash_password(user.password)
                user_updated = user
                await session.commit()

                return user_updated

            else:
                raise HTTPException(detail="Usuario não encontrado",status_code=status.HTTP_404_NOT_FOUND)
        
        else :
            raise HTTPException(detail="Você não tem permissão para acessar este recurso\npor favor contate a administração se achar isso um erro",status_code=status.HTTP_403_FORBIDDEN)
@router.delete('/{user_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int,db:AsyncSession=Depends(get_session),user_logged:UserModel=Depends(get_current_user)):
    async with db as session:
        if user_logged.is_admin == True or user_logged.id == user_id:
            query = select(UserModel).filter(UserModel.id == user_id)
            result = await session.execute(query)
            user_deleted:UserSchemaBase = result.scalars().unique().one_or_none()

            if user_deleted:
                session.delete(user_deleted)
                await session.commit()

                return Response(status_code=status.HTTP_204_NO_CONTENT)

            else:
                raise HTTPException(detail="Usuario não encontrado",status_code=status.HTTP_404_NOT_FOUND)
        
        else :
            raise HTTPException(detail="Você não tem permissão para acessar este recurso\npor favor contate a administração se achar isso um erro",status_code=status.HTTP_403_FORBIDDEN)

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db:AsyncSession = Depends(get_session)):
    user = await authenticate(email=form_data.username,password=form_data.password,db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Credenciais invalidas!!")
    

    return JSONResponse(content={"access_token":create_token_access(sub=user.id),"token_type":"bearer"},status_code=status.HTTP_200_OK)

