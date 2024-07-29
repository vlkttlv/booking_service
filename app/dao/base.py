from sqlalchemy import delete, select, insert
from app.database import async_session_maker

# DAO - Data Access Object;  абстрагируем работу с БД

class BaseDAO: # класс, от кот-го будут наследоваться модели, нужен , т.к. для каждой модели будут одинаковые методы

    model = None
    
    @classmethod
    async def find_by_id(cls, model_id: int): # выводим информацию из БД по идентификатору
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod 
    async def find_all(cls,**filter_by): # выводим информацию из БД по условиям
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by) # select * from bookigs
            result = await session.execute(query)
            return result.scalars().all() # result.mappings().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit() # фиксирует изменения в БД, обязательно

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
