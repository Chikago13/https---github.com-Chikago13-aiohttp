import datetime, json



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




