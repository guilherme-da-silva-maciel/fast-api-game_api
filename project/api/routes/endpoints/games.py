from typing import List
from fastapi import APIRouter,status,Depends,HTTPException,Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.game_model import GameModel
from models.user_model import UserModel
from schemas.game_schemas import GameSchema
from core.deps import get_current_user,get_session
from fastapi_limiter.depends import RateLimiter

router = APIRouter()

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[GameSchema])
async def get_games(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(GameModel)
        result = await session.execute(query)
        games:List[GameModel] = result.scalars().unique().all()

        return games


@router.get('/{game_id}',status_code=status.HTTP_200_OK,response_model=GameSchema)
async def get_game(game_id:int,db:AsyncSession = Depends(get_session)):
    async with db as session:
      query = select(GameModel).filter(GameModel.id == game_id)
      result = await session.execute(query)
      game:GameModel = result.scalars().unique().one_or_none()

      if game:
          return game
      else :
          raise HTTPException(detail="Game não encontrado",status_code=status.HTTP_404_NOT_FOUND)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=GameSchema)
async def post_game(game:GameSchema,user_logged:UserModel = Depends(get_current_user),db:AsyncSession = Depends(get_session)):
    new_game = GameModel(nome=game.nome,ano_lancamento=game.ano_lancamento,nota=game.nota,lista_desejo=game.lista_desejo,genero=game.genero,classificacao_indicativa=game.classificacao_indicativa,criador_id=user_logged.id)

    db.add(new_game)
    await db.commit()

    return new_game

@router.put('/{game_id}',status_code=status.HTTP_202_ACCEPTED,response_model=GameSchema)
async def put_game(game_id:int,game:GameSchema,db:AsyncSession=Depends(get_session),user_logged:UserModel=Depends(get_current_user)):
    async with db as session:
        query = select(GameModel).filter(GameModel.id == game_id).filter(UserModel.id == user_logged.id)
        result = await session.execute(query)
        game_updated:GameModel = result.scalars().unique().one_or_none()

        if game_updated:
          game_updated = game
          await session.commit()

          return game_updated
        
        else:
            HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Game não encontrado')

@router.delete('/{game_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id:int,db:AsyncSession = Depends(get_session),user_logged:UserModel=Depends(get_current_user)):
        async with db as session:
          query = select(GameModel).filter(GameModel.id == game_id).filter(UserModel.id == user_logged.id)
          result = await session.execute(query) 
          game_deleted:GameModel = result.scalars().unique().one_or_none()

          if game_deleted:
                await session.delete(game_deleted)
                await session.commit()
                return Response(status_code=status.HTTP_204_NO_CONTENT)
          
          else:
              raise HTTPException(detail="Game não encontrado",status_code=status.HTTP_404_NOT_FOUND)
          

