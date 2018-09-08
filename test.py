import asyncio
import aiohttp
from bs4 import BeautifulSoup
async def get_title(i):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(i*25)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status)
            text = await resp.text()
            print('start', i)
            soup = BeautifulSoup(text, 'html.parser')
            lis = soup.find('ol', class_='grid_view').find_all('li')
            for li in lis:
                title = li.find('span', class_="title").text
                print(title)
loop = asyncio.get_event_loop()
fun_list = (get_title(i) for i in range(10))
print(type(fun_list))
loop.run_until_complete(asyncio.gather(*fun_list))
