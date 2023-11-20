from data_extraction import DataExtractor
import pandas as pd
from dateutil.parser import parse
import numpy as np

class DataCleaning:

    def __init__(self):
        pass

    def clean_user_data(self):

        user_details = DataExtractor().read_rds_table()

        # user_details.info()
        try:
            user_details.first_name = user_details.first_name.astype('string', errors='raise')
            user_details.last_name = user_details.last_name.astype('string', errors='raise')
            # user_details.date_of_birth = user_details.date_of_birth.apply(parse)
            user_details.date_of_birth = pd.to_datetime(user_details.date_of_birth, infer_datetime_format=True, errors='coerce')
            # test = user_details
            # test = user_details.loc[user_details['date_of_birth'].isnull()]
            # test['True/False'] = test.replace({test['date_of_birth']:True}, inplace=True)
            # test.info()
            user_details.company = user_details.company.astype('string', errors='raise')
            user_details.email_address = user_details.email_address.astype('string', errors='raise')
            user_details.address = user_details.address.astype('string', errors='raise')
            user_details.country = user_details.country.astype('string', errors='raise')
            user_details.country_code = user_details.country_code.astype('string', errors='raise')
            user_details.phone_number = user_details.phone_number.replace({r'\(': '',r'\)': '',r' ': '',r'-': '',r'\.': '',r'\+': ''}, regex=True)
            user_details.phone_number = pd.to_numeric(user_details.phone_number, errors='coerce')
            user_details = user_details.dropna()
            user_details.phone_number = user_details.phone_number.astype('int64', errors='raise')
            user_details.join_date = pd.to_datetime(user_details.join_date, infer_datetime_format=True, errors='coerce')
            # pn_regex = '^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$'
            # user_details.loc[~user_details['phone_number'].str.match(pn_regex), 'phone_number'] = np.nan
            # user_details['phone_number'] = user_details.loc[~user_details['phone_number'].str.match(pn_regex), 'phone_number'] 
            user_details = user_details.dropna()
            print('The user data has been cleaned.')
        except Exception as e:
            print(e)

        return user_details
    
    def clean_card_data(self):
        card_data = DataExtractor().retrieve_pdf_data()
        card_data.card_number = card_data.card_number.astype('int64', errors='coerce')
        card_data.expiry_date = pd.to_datetime(card_data.expiry_date, format='%m/%y', errors='coerce')
        card_data.card_provider = card_data.card_provider.astype('string', errors='raise')
        card_data.date_payment_confirmed = pd.to_datetime(card_data.date_payment_confirmed, infer_datetime_format=True, errors='coerce')
        card_data = card_data.dropna()
        print('The card details have been cleaned.')
        return card_data
    
    def called_clean_store_data(self):
        sdf = DataExtractor().retrieve_stores_data()
        sdf.address = sdf.address.astype('string', errors='coerce')
        sdf.longtitude = sdf.longtitude.astype('float64', errors='coerce')
        sdf.lat = sdf.lat.astype('float64', errors='coerce')
        sdf.locality = sdf.locality.astype('string', errors='coerce')
        sdf.store_code = sdf.store_code.astype('int64', errors='coerce')
        sdf.staff_numbers = sdf.staff_numbers.astype('int64', errors='coerce')

        pass
    pass



# DataCleaning().clean_user_data()
DataCleaning().clean_card_data()