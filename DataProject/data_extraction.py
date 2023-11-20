from sqlalchemy import text, create_engine, inspect
import pandas as pd
import yaml
import tabula
from api_key import api_key
import requests


class DataExtractor:

    def __init__(self):
        pass

    def read_data(self):
        pass

    def read_rds_table(self):
        
        with open("db_creds.yaml", "r") as file:
            creds = yaml.safe_load(file)

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = creds['RDS_HOST']
        USER = creds['RDS_USER']
        PASSWORD = creds['RDS_PASSWORD']
        DATABASE = creds['RDS_DATABASE']
        PORT = creds['RDS_PORT']

        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

        engine.execution_options(isolation_level='AUTOCOMMIT').connect()

        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        user_details = table_names[1]

        # with engine.connect() as connection:
        #     result = connection.execute(text(f"SELECT * FROM {store_details}"))
        #     # for row in result:
        #     #     print(row)
        #     sdpdf = pd.DataFrame(result)

        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {user_details}"))
            # for row in result:
            #     print(row)
            udpdf = pd.DataFrame(result)

        # with engine.connect() as connection:
        #     result = connection.execute(text(f"SELECT * FROM {orders}"))
        #     # for row in result:
        #     #     print(row)
        #     opdf = pd.DataFrame(result)
        
        # ucdata = [sdpdf, udpdf, opdf]
        
        return udpdf
    
    def retrieve_pdf_data(self, pdf_link='https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'):
        pdf_df = tabula.read_pdf(pdf_link, stream=True)
        pdf_df = pdf_df[0]
        print('Pdf file has be extracted sucessfully.')
        return pdf_df

    def list_number_of_stores(self, headers=api_key, num_of_stores_endpoint='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'):
        response = requests.get(url=num_of_stores_endpoint, headers=headers)
        result = response.json()
        nos = result['number_stores']
        return nos
    
    def retrieve_stores_data(self, headers=api_key):
        response = requests.get(url=f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/0', headers=headers)
        stores = response.json()
        store_dict = {}
        for field in stores:
            store_dict[field] = []
        for store_num in range(self.list_number_of_stores()):
            store_number = store_num
            response = requests.get(url=f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}', headers=headers)
            stores = response.json()
            for field in stores:
                store_dict[field].append(stores[field])
        # print(store_dict)
        storedf = pd.DataFrame(store_dict)
        return storedf
    pass

# print(DataExtractor().read_rds_table())
DataExtractor().retrieve_stores_data()