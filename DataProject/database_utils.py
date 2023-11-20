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
        return table_names

    def upload_to_db(self, database_name='sales_data', user_table_name='dim_users', card_table_name='dim_card_details', password=password):

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

        pass
    
    pass

# print(DatabaseConnector().read_db_creds())
# print(DatabaseConnector().list_db_tables())
DatabaseConnector().upload_to_db()
