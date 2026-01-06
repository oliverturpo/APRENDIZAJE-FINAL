from prefect import flow
from tasks.extract import extract
from tasks.transform import transform
from tasks.load import load


@flow
def main():
    data = extract()
    print(f'extraidos {len(data)} registros')
    #print(data[0])
    data_transform = transform(data)
    #print(data_transform.columns)
    print(f'transformados {data_transform.shape[0]} registros')
    resultado = load(data_transform)
    print(f'se insertaron {resultado} registros en la bd')
    
if __name__ == "__main__":
    main()
