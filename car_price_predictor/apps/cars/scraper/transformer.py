import pandas as pd


class CarTransformer:
    """Transforma y limpia datos (adaptado de transform.py)"""

    BASE_URL = "https://neoauto.com"

    def transform(self, data):
        """
        Limpia y transforma datos

        Args:
            data (list): Lista de diccionarios con datos crudos

        Returns:
            pd.DataFrame: DataFrame transformado
        """
        df = pd.DataFrame(data)

        # Completar URLs
        df['link'] = self.BASE_URL + df['link']

        # Transformar precios
        df['price'] = df['price'].apply(self._clean_price)

        return df

    def _clean_price(self, price_str):
        """Limpia string de precio a float"""
        if price_str == 'Consultar' or not price_str:
            return None

        try:
            cleaned = price_str.replace(' ', '').replace('US$', '').replace(',', '').strip()
            return float(cleaned)
        except:
            return None
