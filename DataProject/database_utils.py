import yaml
import psycopg2
from sqlalchemy import create_engine, inspect, text
from data_cleaning import DataCleaning
from pg_password import password

class DatabaseConnector():
    
    def __init__(self):
        pass

    def read_db_creds(self):
        with open("db_creds.yaml", "r") as file:
            db_creds = yaml.safe_load(file)
        return db_creds

    def init_db_engine(self):

        creds=self.read_db_creds()

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = creds['RDS_HOST']
        USER = creds['RDS_USER']
        PASSWORD = creds['RDS_PASSWORD']
        DATABASE = creds['RDS_DATABASE']
        PORT = creds['RDS_PORT']

        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

        engine.execution_options(isolation_level='AUTOCOMMIT').connect()

        # result = engine.execution_options(isolation_level='AUTOCOMMIT').connect().execute((text("SELECT * FROM actor")))

        return engine

    def list_db_tables(self):
        inspector = inspect(self.init_db_engine())
        table_names = inspector.get_table_names()
        print(table_names)
        return table_names

    def upload_to_db(self, database_name='sales_data', user_table_name='dim_users', card_table_name='dim_card_details', called_clean_store_table_name='dim_store_details', clean_products_data_table_name='dim_products', clean_orders_data_table_name='orders_table', clean_sales_data_table_name='dim_date_times', password=password):

        database_type = 'postgresql'
        database_api = 'psycopg2'
        database = database_name
        user = 'postgres'
        password = password
        host = 'localhost'
        port = '5432'

        engine = create_engine(f"{database_type}+{database_api}://{user}:{password}@{host}:{port}/{database}")

        uddf = DataCleaning().clean_user_data()
        uddf.to_sql(name=user_table_name, con=engine, if_exists='replace', index=False)
        print(f'Your data has been uploaded to the {database_name} successfully under the {user_table_name} table.')

        cddf = DataCleaning().clean_card_data()
        cddf.to_sql(name=card_table_name, con=engine, if_exists='replace', index=False)
        print(f'Your data has been uploaded to the {database_name} successfully under the {card_table_name} table.')

        ccsddf = DataCleaning().called_clean_store_data()
        ccsddf.to_sql(name=called_clean_store_table_name, con=engine, if_exists='replace', index=False)
        print(f'Your data has been uploaded to the {database_name} successfully under the {called_clean_store_table_name} table.')

        cpddf = DataCleaning().clean_products_data()
        cpddf.to_sql(name=clean_products_data_table_name, con=engine, if_exists='replace', index=False)
        print(f'Your data has been uploaded to the {database_name} successfully under the {clean_products_data_table_name} table.')

        coddf = DataCleaning().clean_orders_data()
        coddf.to_sql(name=clean_orders_data_table_name, con=engine, if_exists='replace', index=False)
        print(f'Your data has been uploaded to the {database_name} successfully under the {clean_orders_data_table_name} table.')

        csddf = DataCleaning().clean_sales_data()
        csddf.to_sql(name=clean_sales_data_table_name, con=engine, if_exists='replace', index=False)
        print(f'Your data has been uploaded to the {database_name} successfully under the {clean_sales_data_table_name} table.')

        pass
    
    pass

# print(DatabaseConnector().read_db_creds())
# print(DatabaseConnector().list_db_tables())
DatabaseConnector().upload_to_db()
