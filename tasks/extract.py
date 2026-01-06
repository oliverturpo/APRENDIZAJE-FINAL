from prefect import task
import requests
from bs4 import BeautifulSoup
import re
import json

@task
def extract():
    extract_data = []
    
    #URL = "https://neoauto.com/venta-de-autos-nuevos"
    #URL = "https://neoauto.com/venta-de-autos-seminuevos"
    URL = "https://neoauto.com/venta-de-autos"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response_pages = requests.get(URL, headers=headers)
    if response_pages.status_code == 200:
        pages_soup = BeautifulSoup(response_pages.content, 'html.parser')
        # Encuentra el número total de páginas
        last_page_link = pages_soup.find('a', class_='c-pagination-content__last-page')
        match = re.search(r'page=(\d+)', last_page_link['href']) if last_page_link else None
        total_paginas = int(match.group(1)) if match else 1
        print(f'Número total de páginas: {total_paginas}')

    for pagina in range(1, total_paginas + 1):
        URL_PAGE = f'{URL}?page={pagina}'
        print(f'Conectando a la página {URL_PAGE}...')
        # Realiza la solicitud HTTP
        response = requests.get(URL_PAGE,headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content,'html.parser')
            autos = soup.find_all("article", class_="c-results")
            
            for art in autos:
                data_gtm = json.loads(art["data-gtm"])
                title = art.find("h2", class_="c-results__header-title").text.strip()
                link = art.find("a", class_="c-results__link")["href"]
                tag = art.find("div", class_="c-results-tag__stick")
                if tag:
                    tag = tag.get_text()
                image = art.find("img", class_="c-results-slider__img-inside")["data-src"]
                fuel = art.find("span", class_="c-results-used__detail-fuel").text.strip()
                location = art.find("span", class_="c-results-details__description-text--highlighted").text.strip()
                price = art.find("div", class_="c-results-mount__price").text.strip()
            
                dic_autos = {
                    "id" : data_gtm.get("item_id"),
                    "title": title,
                    "link": link,
                    "tag": tag,
                    "image": image,
                    "fuel": fuel,
                    "location": location,
                    "price": price,
                    "brand": data_gtm.get("item_brand"),
                    "year": data_gtm.get("item_year"),
                    "advertiser": data_gtm.get("item_advertiser"),
                    "category": data_gtm.get("item_category"),
                    "subcategory": data_gtm.get("item_category_2"),
                    "transmission": data_gtm.get("item_transmission"),
                    "fuel": data_gtm.get("item_fuel"),
                    "slug": data_gtm.get("item_publication_slug"),
                }
                
                extract_data.append(dic_autos)
    
    
    return extract_data