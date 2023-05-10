import asyncio
import aiofiles, aiohttp




# async def my_coroutine():
#     print('Запуск coroutine')
#     await asyncio.sleep(1)
#     print('завершение coroutine')

# async def main():
#     print('Запуск програмы')
#     await asyncio.gather(my_coroutine(), my_coroutine(), my_coroutine())
#     print('Завершение программы')

# asyncio.run(main()

# async def read_text(fiel):
#     print(f'read {fiel}')
#     async with aiofiles.open(fiel, 'r') as f:
#         context = await f.read()
#         print(f'Сщдержимое фаила {context}')


# async def main():
#     await asyncio.gather(read_text('fiel1.txt'), read_text('fiel2.txt'), read_text('fiel3.txt'))


# asyncio.run(main())

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as respons:
            return await respons.text()
        

async def main():
    context = 'https://docs.aiohttp.org/en/stable/index.html'
    response = await fetch_url(context)
    print(response)
    
asyncio.run(main())