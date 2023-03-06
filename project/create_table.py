from core.configs import settings
from sqlalchemy.orm.session import Session
from core.database import engine

async def create_tables() -> None:
    import models.__all_models
    print('Criando as tabelas no banco de dados')

    # session: Session = Connection().get_session()

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
        print('Tabela(s) criada com sucesso')


if __name__ == '__main__':
    import asyncio
    asyncio.run(create_tables())
