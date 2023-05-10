from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import sessionmaker, Session, DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base
from db import Manufacturers, ManufacturersStorehouses, Sweets, SweetsTypes, Storehouses
from utils import Utils
import json, sys, asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import datetime
from typing import Type, List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import tracemalloc 

tracemalloc.start()
utils = Utils()

class AsyncDatabase:    
    def __init__(self, connection_string):
        self.engine = create_async_engine(connection_string)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)


    async def add(self, model, **data):
        async with self.session() as session:
            obj = model(**data)
            session.add(obj)
            await session.commit()
            return obj

    async def delete(self, model, id):
        async with self.session() as session:
            obj = await session.execute(f'delete from {model.__tablename__} where id=:id returning id', {"id": id})
            if obj:
                res = obj.fetchone()
                if res and res[0]:
                    await session.commit()
                    return res[0]
                return None
            return None

    async def update(self, model, id, **data):
        async with self.session() as session:
            result_proxy = await session.execute(
                model.__table__.update().where(model.id == id).values(**data)
            )
            rowcount = result_proxy.rowcount
            await session.commit()
            if rowcount == 1:
                obj = await session.execute(
                    model.__table__.select().where(model.id == id)
                )
                return obj.scalar_one()
            return None

    async def select(self, model):
        async with self.session() as session:
            result = await session.execute(f"SELECT * FROM {model.__tablename__}")
            return result.fetchall()

    async def select_by_id(self, model, id):
        async with self.session() as session:
            result = await session.execute(f"SELECT * FROM {model.__tablename__} WHERE id=:id", {"id": id})
            # print(result)
            # for i in result:
            #     print(i)
            return result.one_or_none()

# db = AsyncDatabase('postgresql+asyncpg://alex:12345@localhost/mybase')

# async def async_main():
#     # dic = name = 'Собакен2', phone = '78125748899', adress = '109235, г. Москва, Проектируемый проезд, д.15', city = 'Minsk', country = 'Belarus' 
#     db_main =  await db.update(Manufacturers, 2, name = 'Собакен123', phone = '78133348899')
#     print(db_main)

# asyncio.run(async_main())

# cveri = Connect('postgresql://alex:12345@localhost/mybase')
# db = cveri.select_all(Manufacturers)
# res = utils.convert_json([d.__dict__ for d in db])
# print(res)
# db = cveri.select_by_id(Sweets, 1)
# res = utils.convert_json([db.__dict__])
# print(res)
# cveri.updat_insert(Sweets(sweets_types_id = 1, name= "Мильтик", cost = '100', weight = '200', manufacturer_id = 1, production_date = datetime.date.fromisoformat("2023-12-23"), expiration_date = datetime.date.fromisoformat("2023-12-24"), with_sugar = True, requires_freezing = True) )
# sl = cveri.select_by_id(Sweets, 1)
# up = cveri.update(sl, name = 'newname2', with_sugar = True)
# cveri.delete_by_id(Sweets, 1)