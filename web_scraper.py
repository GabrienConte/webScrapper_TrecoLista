import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from Sites import Sites
import asyncio
import aiohttp
import validators

def get_produto_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if Sites.BooksToScrape.value in url:
        title = soup.find('div', {'class': 'produto_main'}).find('h1').text.strip()
        price = soup.find('p', {'class': 'price_color'}).text.strip()
        image_relative_url = soup.find('div', {'class': 'item active'}).find('img')['src']
        image_url = urljoin(url, image_relative_url)
        plataforma = Sites.BooksToScrape.value
    elif Sites.LojaVirtual.value in url:
        title = soup.find('h1', {'class': 'ui-pdp-title'}).text.strip()
        interiro = soup.find('span', {'class':'andes-money-amount__fraction'}).text.strip()
        fracao = soup.find('span', {'class':'andes-money-amount__cents andes-money-amount__cents--superscript-36'}).text.strip()
        price = f"{interiro}.{fracao}"
        image_url = soup.find('figure', {'class': 'ui-pdp-gallery__figure'}).find('img')['src']
        plataforma = Sites.LojaVirtual.value
    else:
        title = ""
        price = "0"
        image_url = ""
        plataforma = "Outra"

    return {
        'descricao': title,
        'valor': price,
        'imagemPath': image_url,
        'plataforma': plataforma
    }

async def fetch_produto_info(session, produto, semaphore):
    if not validators.url(produto['ProdutoLink']):
        return {'id': produto['ProdutoId'], 'valor': '0'}
    
    async with semaphore:
        async with session.get(produto['ProdutoLink']) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            if Sites.BooksToScrape.value in produto['ProdutoLink']:
                price = soup.find('p', {'class': 'price_color'}).text.strip()
            elif Sites.LojaVirtual.value in produto['ProdutoLink']:
                interiro = soup.find('span', {'class':'andes-money-amount__fraction'}).text.strip()
                fracao = soup.find('span', {'class':'andes-money-amount__cents andes-money-amount__cents--superscript-36'}).text.strip()
                price = f"{interiro}.{fracao}"
            else:
                price = "0"

            return {
                'id': produto['ProdutoId'],
                'valor': price
            }

async def get_produtos_info(produtos, max_concurrent_requests=5, pause_interval=5, pause_duration=1):
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, produto in enumerate(produtos):
            tasks.append(fetch_produto_info(session, produto, semaphore))
            if (i + 1) % pause_interval == 0:
                await asyncio.sleep(pause_duration)  # Pausa após cada `pause_interval` requisições

        return await asyncio.gather(*tasks)