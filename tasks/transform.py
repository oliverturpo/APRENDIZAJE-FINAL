import pandas as pd
from prefect import task

URL = "https://neoauto.com/venta-de-autos-nuevos"

@task
def transform(data):

    transform_data = pd.DataFrame(data)

    transform_data['link'] = URL + transform_data['link']

    transform_data['price'] = transform_data['price'].apply(
        lambda x: float(x.replace(' ', '').replace('US$', '').replace(',', '').strip()) 
        if x != 'Consultar' else None
    )

    return transform_data
