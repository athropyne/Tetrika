import asyncio
import csv
from time import time
from collections import defaultdict

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

letters_count = defaultdict(int)
base_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
lock = asyncio.Lock()


async def process_page(session: ClientSession, url: str):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        next_page = soup.find('a', string='Следующая страница')
        next_task = None
        if next_page:
            next_url = f"https://ru.wikipedia.org{next_page['href']}"
            next_task = asyncio.create_task(process_page(session, next_url))
        groups = soup.find_all('div', class_='mw-category-group')
        for group in groups:
            letter = group.find('h3').text
            items = group.find_all('li')
            async with lock:
                letters_count[letter] += len(items)
        if next_task:
            await next_task


async def main():
    async with aiohttp.ClientSession() as session:
        await process_page(session, base_url)

    with open('beasts.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for letter, count in sorted(letters_count.items()):
            writer.writerow([letter, count])


if __name__ == "__main__":
    start = time()
    asyncio.run(main())
    end = time() - start
    print(f"Время выполнения: {end} секунд")
