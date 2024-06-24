import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from Sites import Sites

def get_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if Sites.BooksToScrape.value in url:
        title = soup.find('div', {'class': 'product_main'}).find('h1').text.strip()
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
        plataforma = "Outra"

    return {
        'descricao': title,
        'valor': price,
        'imagemPath': image_url,
        'plataforma': plataforma
    }