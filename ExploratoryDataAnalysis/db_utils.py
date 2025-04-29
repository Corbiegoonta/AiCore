import yaml
from sqlalchemy import create_engine, inspect, text
import pandas as pd


yaml_file_path = r"C:\Users\nickc\Desktop\Code\AiCore\ML_Project\credentials.yaml"

def load_rds_credentials(file_path):
    
    with open(file_path, "r") as file:
        rds_credentials = yaml.safe_load(file)

    return rds_credentials

class RDSDatabaseConnector:
    
    def __init__(self):
        try:
            self.credentials = load_rds_credentials(yaml_file_path)

            creds = self.credentials

            DATABASE_TYPE = 'postgresql'
            DBAPI = 'psycopg2'
            HOST = creds["RDS_HOST"]
            USER = creds["RDS_USER"]
            PASSWORD = creds["RDS_PASSWORD"]
            DATABASE = creds["RDS_DATABASE"]
            PORT = 5432

            self.engine_connection = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}").execution_options(isolation_level='AUTOCOMMIT').connect()

            print("Database connection has connected!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
    
    def get_table_name(self):
        table_names = inspect(self.engine_connection).get_table_names()
        print(f"The table names in this database are {table_names}")
        return table_names

    def extract_loans_table(self, table_name):
        with self.engine_connection as connection:
            contents_of_table = connection.execute(text(f"SELECT * FROM {table_name}"))
        
        loans_table = pd.DataFrame(contents_of_table)

        return loans_table
    
    def save_data_to_csv(self, path_to_save_directory, file_name, table_name):
        loan_payments_df = self.extract_loans_table(f"{table_name}")
        loan_payments_df.to_csv(f"{path_to_save_directory}\{file_name}")
        print(f"File {file_name} has been created at {path_to_save_directory}.")
        pass

    def load_data_from_csv(self, file_path):
        loan_payments_data = pd.read_csv(file_path)
        return loan_payments_data
        
    pass

if __name__ == "__main__":
    RDSDatabaseConnector().load_data_from_csv(r"C:\Users\nickc\OneDrive\Desktop\Code\AiCore\ML_Project\loan_payments.csv")
