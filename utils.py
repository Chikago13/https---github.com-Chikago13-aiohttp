import datetime, json
import re



class Utils:
    def __init__(self, *args):
        self.args = args

    async def convert_json(self, data):
        async def encode_detatime(obj):
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            else:
                return None
        return await json.dumps(data, default=encode_detatime, ensure_ascii=False)    
    


    async def tuple_to_list(self, typ):
        lists = []
        for i in typ:
            lists.append(list(i))
        return lists

    async def convert_string(self, typ):
        for index, val in enumerate(typ):
            for i, v in enumerate(val):
                if v == True:
                    typ[index][i] = 'Да'
                if v == False:
                    typ[index][i]= 'Нет'
                if isinstance(v, datetime.date):
                    typ[index][i]= v.strftime("%Y-%m-%d")
        return typ
    
    async def convert_today(self, data):
        dt = data.split('-')
        res = datetime.date(year=int(dt[0]), month=int(dt[1]), day= int(dt[2]))
        return res
    
    
    async def convert_bool(self, res):
        if res == '1':
            return True
        elif res =='0':
            return False
        else:
            return None
        
    async def valid_dict(self, res):
        for key, val in res.items():
            if len(str(val)) == 0:
                return False
        return True
    
    async def is_int(self, res):
        try:
            res = int(res)
            return True
        except:
            return False
        
    async def utils_sweets(self, data):
        error, res = '', ''
        try:
            new_data = data.copy()
            new_data['production_date'] = await self.convert_today(data['production_date'])
            new_data['expiration_date'] = await self.convert_today(data['expiration_date'])
            new_data['with_sugar'] = await self.convert_bool(data['with_sugar'])
            new_data['requires_freezing'] = await self.convert_bool(data['requires_freezing'])
            new_data['sweets_types_id'] = int(data['sweets_types_id'])
            new_data['manufacturer_id'] = int(data['manufacturer_id'])
        except Exception as e:
            e = 'Ошибка в добавлениеи'
            return e
        return new_data

    async def phone(self, phone):
        p = r"^(\\7|8)(\d{3})(\d{7})"
        res = re.search(p, phone)
        return res