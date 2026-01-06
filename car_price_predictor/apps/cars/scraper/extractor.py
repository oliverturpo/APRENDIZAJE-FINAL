import requests
from bs4 import BeautifulSoup
import re
import json


class CarExtractor:
    """Extrae datos de neoauto.com (adaptado de extract.py)"""

    def __init__(self, base_url="https://neoauto.com/venta-de-autos"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def extract(self, max_pages=None):
        """
        Extrae datos de todas las páginas

        Args:
            max_pages (int): Límite de páginas a scrapear (None = todas)

        Returns:
            list: Lista de diccionarios con datos de autos
        """
        extract_data = []

        # Obtener total de páginas
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error al conectar: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')
        last_page_link = soup.find('a', class_='c-pagination-content__last-page')
        match = re.search(r'page=(\d+)', last_page_link['href']) if last_page_link else None
        total_pages = int(match.group(1)) if match else 1

        # Limitar páginas si se especifica
        if max_pages:
            total_pages = min(total_pages, max_pages)

        print(f'Número total de páginas a scrapear: {total_pages}')

        # Scrapear cada página
        for page in range(1, total_pages + 1):
            url_page = f'{self.base_url}?page={page}'
            print(f'Scrapeando página {page}/{total_pages}: {url_page}')
            page_data = self._scrape_page(url_page)
            extract_data.extend(page_data)

        return extract_data

    def _scrape_page(self, url):
        """Scrapea una página individual"""
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print(f'Error al scrapear {url}: {response.status_code}')
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        autos = soup.find_all("article", class_="c-results")

        page_data = []
        for art in autos:
            try:
                data_gtm = json.loads(art["data-gtm"])
                title = art.find("h2", class_="c-results__header-title").text.strip()
                link = art.find("a", class_="c-results__link")["href"]
                tag = art.find("div", class_="c-results-tag__stick")
                tag = tag.get_text() if tag else None
                image = art.find("img", class_="c-results-slider__img-inside")["data-src"]
                fuel = art.find("span", class_="c-results-used__detail-fuel").text.strip()
                location = art.find("span", class_="c-results-details__description-text--highlighted").text.strip()
                price = art.find("div", class_="c-results-mount__price").text.strip()

                car_data = {
                    "id": data_gtm.get("item_id"),
                    "title": title,
                    "link": link,
                    "tag": tag,
                    "image": image,
                    "fuel": data_gtm.get("item_fuel"),
                    "location": location,
                    "price": price,
                    "brand": data_gtm.get("item_brand"),
                    "year": data_gtm.get("item_year"),
                    "advertiser": data_gtm.get("item_advertiser"),
                    "category": data_gtm.get("item_category"),
                    "subcategory": data_gtm.get("item_category_2"),
                    "transmission": data_gtm.get("item_transmission"),
                    "slug": data_gtm.get("item_publication_slug"),
                }
                page_data.append(car_data)
            except Exception as e:
                print(f"Error procesando auto: {e}")
                continue

        return page_data
