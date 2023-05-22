from aiohttp import web
from db import Manufacturers, Sweets, SweetsTypes, ManufacturersStorehouses, Storehouses
from detabase import AsyncDatabase
import aiohttp_jinja2, jinja2, os
from utils import Utils
import json, logging

logging.basicConfig(filename='log.log', level=logging.DEBUG)

utils = Utils()

app = web.Application()
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)



app_db = AsyncDatabase('postgresql+asyncpg://alex:12345@localhost/mybase')


@aiohttp_jinja2.template("index.html")
async def home(request):
    title = 'Главная строница'
    # sw = await app_db.select(Sweets)
    return {'title': title}



@aiohttp_jinja2.template("sweets.html")
async def sweets(request):
    title = "Сладости"
    errors = []
    res = []
    sw = await app_db.select(Sweets)
    if sw and len(sw)>0:
        res = await utils.tuple_to_list(sw)
        res = await utils.convert_string(res)
    else:
        errors.append('Запись не найдена')
    # print(result)
    return {'title':title, 'errors':errors, 'res': res}

async def sweetsInfo(request):
    error, sw_type, mn_type = '', '', ''
    try:
        sw_type = await app_db.select(SweetsTypes)
        mn_type = await app_db.select(Manufacturers)
        sw_type = [row._asdict() for row in sw_type]
        mn_type = [row._asdict() for row in mn_type]
    except Exception as e:
        error = e
    data = {'error': error, 'sw_type':sw_type, 'mn_type': mn_type}
    return web.json_response(data)



async def add_sweets(request):
    error, res = '', False
    data = await request.post()
    if not data['cost'].isdigit() or not data['weight'].isdigit():
        error='Некоректный вес или цена'
        return web.json_response({'error': error, 'res': res})
    try:
        new_data = data.copy() 
        new_data['production_date'] = await utils.convert_today(data['production_date'])
        new_data['expiration_date'] = await utils.convert_today(data['expiration_date'])
        new_data['with_sugar'] = await utils.convert_bool(data['with_sugar'])
        new_data['requires_freezing'] = await utils.convert_bool(data['requires_freezing'])
        new_data['sweets_types_id'] = int(data['sweets_types_id'])
        new_data['manufacturer_id'] = int(data['manufacturer_id'])
    except Exception as e:
        logging.error(e)
        error='Некоректная дата'
        return web.json_response({'error': error, 'res': res})
    try:
        res = await app_db.add(Sweets, **new_data)
        if res.id:
            res=True
        logging.info(res)
    except Exception as e:
        logging.error(e)
        error='Ошибка в добавлениеи'
        return web.json_response({'error': error, 'res': res})
    data = {'error': error, 'res': res}
    return web.json_response(data)


@aiohttp_jinja2.template("manufacturers.html")
async def manufacturers(request):
    title = "Производство"
    errors = []
    res = []
    if request.method == 'POST':
        data = await request.post()
        res = await app_db.add(Manufacturers, **data)
    try:
        res = await app_db.select(Manufacturers)
        # print(res)
    except Exception as e:
        errors.append(e)
    return {'title':title, 'errors':errors, 'res': res}





app.add_routes([web.get('/', home, name='home')])
app.add_routes([web.get('/sweets', sweets, name='sweets')])
app.add_routes([web.get('/sweetsInfo', sweetsInfo, name='sweetsInfo')])
app.add_routes([web.post('/add_sweets', add_sweets, name='add_sweets')])
app.add_routes([web.get('/manufacturers', manufacturers, name='manufacturers')])
app.add_routes([web.post('/manufacturers', manufacturers, name='manufacturers')])
app.router.add_static("/static/", path="static", name="static")

if __name__ == '__main__':
    web.run_app(app)


# from abc import ABC, abstractmethod


# class Animal(ABC):

#     @abstractmethod
#     def dog(slef):
#         raise NotImplemented
    

# class Dog:

#     def __init__(self, drink, each):
#         self.__drink = drink
#         self.each = each
        

#     run = 'run'


#     @classmethod
#     def dog2(cls, run):
#         return cls.run
    
# # print(Dog.dog2)


#     @staticmethod
#     def dog3(at):
#         return at*2
    
#     def getterdrink(self):
#         return self.__drink 
    
#     def setterdrink(self, tr):
#         self.__drink = tr

#     @property
#     def drink(self):
#         return self.__drink
    
#     @drink.setter
#     def drink(self, ty):
#         self.__drink = ty


# Dog.dog3(2)

        
# ad = Dog('pit', 'et')

# print(ad.drink)
# ad.drink = 'dsgh'


# import time
# import re

# def timer_deko(func):
#     def wrapper(*args, **kwargs):
#         time_start = time.time()
#         st = func(*args, **kwargs)
#         time_stop = time.time() - time_start
#         print(time_stop)
#         return st
#     return wrapper


# @timer_deko
# def time_sleep():
#     time.sleep(2)


# def phone(mobel):
#     patern = r"^(375|\\+375|8\\s?0)(29|25|33|44)(\\d{7})"
#     res = re.search(patern, mobel)
#     return bool(res)
    

