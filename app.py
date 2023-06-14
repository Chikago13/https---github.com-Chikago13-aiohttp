from aiohttp import web
from db import Manufacturers, Sweets, SweetsTypes, ManufacturersStorehouses, Storehouses
from detabase import AsyncDatabase
import aiohttp_jinja2
import jinja2
import os
from utils import Utils
import json
import logging

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
    if sw and len(sw) > 0:
        res = await utils.tuple_to_list(sw)
        res = await utils.convert_string(res)
    else:
        errors.append('Запись не найдена')
    # print(result)
    return {'title': title, 'errors': errors, 'res': res}


async def sweetsInfo(request):
    error, sw_type, mn_type, st_type, sw_ty_type= '', '', '', '', ''
    try:
        sw_type = await app_db.select(SweetsTypes)
        mn_type = await app_db.select(Manufacturers)
        st_type = await app_db.select(Storehouses)
        sw_ty_type = await app_db.select(SweetsTypes)
        sw_type = [row._asdict() for row in sw_type]
        mn_type = [row._asdict() for row in mn_type]
        st_type = [row._asdict() for row in st_type]
        sw_ty_type = [row._asdict() for row in sw_ty_type]
    except Exception as e:
        error = e
    data = {'error': error, 'sw_type': sw_type, 'mn_type': mn_type, 'st_type': st_type, 'sw_ty_type':sw_ty_type}
    return web.json_response(data)


async def add_sweets(request):
    error, res = '', False
    data = await request.post()
    if not data['cost'].isdigit() or not data['weight'].isdigit():
        error = 'Некоректный вес или цена'
        return web.json_response({'error': error, 'res': res})
    new_data = await utils.utils_sweets(data)
    # try:
    #     new_data = data.copy()
    #     new_data['production_date'] = await utils.convert_today(data['production_date'])
    #     new_data['expiration_date'] = await utils.convert_today(data['expiration_date'])
    #     new_data['with_sugar'] = await utils.convert_bool(data['with_sugar'])
    #     new_data['requires_freezing'] = await utils.convert_bool(data['requires_freezing'])
    #     new_data['sweets_types_id'] = int(data['sweets_types_id'])
    #     new_data['manufacturer_id'] = int(data['manufacturer_id'])
    # except Exception as e:
    #     logging.error(e)
    #     error = 'Некоректная дата'
    #     return web.json_response({'error': error, 'res': res})
    try:
        res = await app_db.add(Sweets, **new_data)
        if res.id:
            res = True
        logging.info(res)
    except Exception as e:
        logging.error(e)
        error = 'Ошибка в добавлениеи'
        return web.json_response({'error': error, 'res': res})
    data = {'error': error, 'res': res}
    return web.json_response(data)


async def del_sw(request):
    error, res = '', ''
    if request.method == 'POST':
        data = await request.post()
        sw_id = data['id']
        if sw_id and await utils.is_int(sw_id):
            try:
                res = await app_db.delete(Sweets, int(sw_id))
                if res:
                    logging.info(f'Удалили запись с id{res}')
                else:
                    error = 'Ошибка удаления'
            except Exception as e:
                logging.error(
                    f'Не смогли удалить запись с id{sw_id} ошибка удаления: {e}')
        else:
            error = 'Неверное id'
    else:
        error = 'Неверный метод'
    return web.json_response({'res': res, 'error': error})


async def update_sw(request):
    error, res = '', ''
    if request.method == 'POST':
        data = dict(await request.post())
    if not data['cost'].isdigit() or not data['weight'].isdigit():
        error = 'Некоректный вес или цена'
        return web.json_response({'error': error, 'res': res})
    new_data = await utils.utils_sweets(data)
    if isinstance(new_data, dict):
        if await utils.check_man_day(new_data['production_date']):
            return web.json_response({'error': 'Некорктная дата', 'res':res})
        if not await utils.check_expir_date(new_data['production_date'], new_data['expiration_date']):
            return web.json_response({'error': 'Некоректный срок годности', 'res':res})
        try:
            res = await app_db.update(model=Sweets, id=int(new_data['id']), name=new_data['name'], cost = new_data['cost'], weight = new_data['weight'], production_date = new_data['production_date'], expiration_date= new_data['expiration_date'], with_sugar = new_data['with_sugar'], requires_freezing= new_data['requires_freezing'], sweets_types_id = new_data['sweets_types_id'], manufacturer_id = new_data['manufacturer_id'])
            logging.info(res)
        except Exception as e:
            logging.error(e)
            error = 'Ошибка в добавлениеи'
            return web.json_response({'error': error, 'res': res})
    else:
        logging.error(new_data)
        error = 'Обновление не прошло'
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
    return {'title': title, 'errors': errors, 'res': res}


async def del_man(request):
    if request.method == 'POST':
        data = await request.post()
        mn_id = data['man_id']
        if mn_id:
            res = await app_db.delete(Manufacturers, int(mn_id))
            if res:
                return web.json_response({'succes': 'Запись удалена', 'error': ''})
            else:
                return web.json_response({'succes': '', 'error': 'Ошибка удаления'})
        return web.json_response({'succes': '', 'error': 'Некоректное id'})
    return web.json_response({'succes': '', 'error': 'Method not error'})


async def update_mn(request):
    error, res = '', ''
    if request.method == 'POST':
        data = dict(await request.post())
        if await utils.valid_dict(data):
            try:
                res = await app_db.update(model=Manufacturers, id=int(data['id']), name=data['name'], phone=data['phone'], adress=data['adress'], city=data['city'], country=data['country'])
            except Exception as e:
                error = e
        else:
            error = 'Неверные входные данные'
        return web.json_response({'res': res, 'error': error})
    
@aiohttp_jinja2.template("storehouses.html")
async def storehouses(request):
    title = "Склады"
    errors = []
    res = []
    try:
        res = await app_db.select(Storehouses)
    except Exception as e:
        errors.append(e)
    return {'title': title, 'errors': errors, 'res': res}

async def add_store(request):
    error, res = '', ''
    if request.method == 'POST':
        data = await request.post()
        print(data)
    try:
        res = await app_db.add(model=Storehouses, name = data['name'], adress = data['adress'], city = data['city'], country = data['country'])
        if res.id and res.id >0:
            res = res.id
            logging.info(f'Успешное добавление id {res}')
    except Exception as e:
        logging.error(e)
        error = 'Ошибка добавления'
    return web.json_response({'res': res, 'error': error})
    



async def del_st(request):
    if request.method == 'POST':
        data = await request.post()
        st_id = data['st_id']
        if st_id:
            res = await app_db.delete(Storehouses, int(st_id))
            if res:
                return web.json_response({'succes': 'Запись удалена', 'error': ''})
            else:
                return web.json_response({'succes': '', 'error': 'Ошибка удаления'})
        return web.json_response({'succes': '', 'error': 'Некоректное id'})
    return web.json_response({'succes': '', 'error': 'Method not error'})

async def update_st(request):
    error, res = '', ''
    if request.method == 'POST':
        data = dict(await request.post())
        if await utils.valid_dict(data):
            try:
                res = await app_db.update(model=Storehouses, id=int(data['id']), name=data['name'], adress=data['adress'], city=data['city'], country=data['country'])
            except Exception as e:
                error = e
        else:
            error = 'Неверные входные данные'
        return web.json_response({'res': res, 'error': error})


@aiohttp_jinja2.template("sweets_types.html")
async def sweets_types(request):
    title = 'Виды Сладости'
    error, res = [], []
    if request.method =='POST':
        data = await request.post()
        res = await app_db.add(SweetsTypes, **data)
    try:
        res = await app_db.select(SweetsTypes)
    except Exception as e:
        error.append(e)
    return {'title': title, 'errors': error, 'res': res}

async def del_swtype(request):
    if request.method == 'POST':
        data = await request.post()
        swtype_id = data['swtype_id']
        if swtype_id:
            res = await app_db.delete(SweetsTypes, int(swtype_id))
            if res:
                return web.json_response({'succes': 'Запись удалена', 'error': ''})
            else:
                return web.json_response({'succes': '', 'error': 'Ошибка удаления'})
        return web.json_response({'succes': '', 'error': 'Некоректное id'})
    return web.json_response({'succes': '', 'error': 'Method not error'})

async def update_swtype(request):
    error, res = '', ''
    if request.method == 'POST':
        data = dict(await request.post())
        if await utils.valid_dict(data):
            try:
                res = await app_db.update(model=SweetsTypes, id=int(data['id']), name=data['name'])
            except Exception as e:
                error = e
        else:
            error = 'Неверные входные данные'
        return web.json_response({'res': res, 'error': error})





app.add_routes([web.get('/', home, name='home')])
app.add_routes([web.get('/sweets', sweets, name='sweets')])
app.add_routes([web.get('/sweetsInfo', sweetsInfo, name='sweetsInfo')])
app.add_routes([web.post('/add_sweets', add_sweets, name='add_sweets')])
app.add_routes([web.post('/del_sw', del_sw, name='del_sw')])
app.add_routes([web.post('/update_sw', update_sw, name='update_sw')])
app.add_routes([web.get('/manufacturers', manufacturers, name='manufacturers')])
app.add_routes([web.post('/manufacturers', manufacturers, name='manufacturers')])
app.add_routes([web.post('/del_man', del_man, name='del_man')])
app.add_routes([web.post('/update_mn', update_mn, name='update_mn')])
app.add_routes([web.get('/storehouses', storehouses, name='storehouses')])
app.add_routes([web.post('/storehouses', storehouses, name='storehouses')])
app.add_routes([web.post('/add_store', add_store, name='add_store')])
app.add_routes([web.post('/del_st', del_st, name='del_st')])
app.add_routes([web.post('/update_st', update_st, name='update_st')])
app.add_routes([web.get('/sweets_types', sweets_types, name='sweets_types')])
app.add_routes([web.post('/sweets_types', sweets_types, name='sweets_types')])
app.add_routes([web.post('/del_swtype', del_swtype, name='del_swtype')])
app.add_routes([web.post('/update_swtype', update_swtype, name='update_swtype')])
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
