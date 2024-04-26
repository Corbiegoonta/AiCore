from data_extraction import DataExtractor
import pandas as pd
from dateutil.parser import parse
import numpy as np

class DataCleaning:

    def __init__(self):
        pass

    def clean_user_data(self, user_details = DataExtractor().read_rds_table()['user_details']):
        user_details.first_name = user_details.first_name.astype('string', errors='raise')
        user_details.last_name = user_details.last_name.astype('string', errors='raise')
        user_details.date_of_birth = pd.to_datetime(user_details.date_of_birth, infer_datetime_format=True, errors='coerce')
        user_details.company = user_details.company.astype('string', errors='raise')
        user_details.email_address = user_details.email_address.astype('string', errors='raise')
        user_details.address = user_details.address.astype('string', errors='raise')
        user_details.country = user_details.country.astype('string', errors='raise')
        user_details.country_code = user_details.country_code.astype('string', errors='raise')
        user_details.phone_number = user_details.phone_number.replace({r'\(': '',r'\)': '',r' ': '',r'-': '',r'\.': '',r'\+': '',r'[a-z]': ''}, regex=True)
        user_details.phone_number = pd.to_numeric(user_details.phone_number, errors='coerce', downcast="integer")
        print(len(user_details.index))
        print(user_details.isnull().sum())
        user_details.join_date = pd.to_datetime(user_details.join_date, infer_datetime_format=True, errors='coerce')
        user_details.replace('GGB', 'GB', inplace=True)
        user_details = user_details.dropna()
        print('The user data has been cleaned.')

        return user_details
    
    def clean_card_data(self, card_data = DataExtractor().retrieve_pdf_data()):
        pd.options.display.float_format = '{:.0f}'.format
        print(len(card_data.index))
        print(card_data[card_data['card_number'] == 4537509987455280000])
        print(card_data[card_data['card_number'] == 4537509987455280128])
        print('entire df')
        card_data.card_number = card_data.card_number.replace({r'\(': '',r'\)': '',r' ': '',r'-': '',r'\.': '',r'\+': '',r'[a-z]': '',r'\?': ''}, regex=True)
        print(card_data[card_data['card_number'] == 4537509987455280000])
        print('after regex')
        card_data.card_number = card_data.card_number.astype('int64', errors='ignore')
        print(card_data[card_data['card_number'] == 4537509987455280000])
        print('after numeric')
        card_data.expiry_date = pd.to_datetime(card_data.expiry_date, format='%m/%y', errors='coerce')
        print(card_data[card_data['card_number'] == 4537509987455280000])
        print('after expiry')
        card_data.card_provider = card_data.card_provider.astype('string', errors='raise')
        print(card_data[card_data['card_number'] == 4537509987455280000])
        print('after provider')
        card_data.date_payment_confirmed = pd.to_datetime(card_data.date_payment_confirmed, infer_datetime_format=True, errors='coerce')
        print(card_data[card_data['card_number'] == 4537509987455280000])
        print(card_data[card_data['card_number'] == 4537509987455280128])
        print('after datetime')
        card_data = card_data.dropna()
        print('The card details have been cleaned.')

        return card_data
    
    def called_clean_store_data(self, sdf = DataExtractor().retrieve_stores_data()):
        sdf = sdf.drop('lat', axis=1)
        sdf.longitude = pd.to_numeric(sdf.longitude, errors='coerce')
        sdf.address = sdf.address.astype('string', errors='raise')
        sdf.locality = sdf.locality.astype('string', errors='raise')
        sdf.store_code = sdf.store_code.astype('string', errors='raise')
        sdf.staff_numbers = sdf.staff_numbers.replace({r'[A-Z]': '',r'[a-z]': ''}, regex=True)
        sdf.staff_numbers = pd.to_numeric(sdf.staff_numbers, errors='raise')
        sdf.opening_date = pd.to_datetime(sdf.opening_date, infer_datetime_format=True, errors='coerce')
        sdf.store_type = sdf.store_type.astype('string', errors='raise')
        sdf.latitude = pd.to_numeric(sdf.latitude, errors='coerce')
        sdf.country_code = sdf.country_code.astype('string', errors='raise')
        sdf.continent = sdf.continent.astype('string', errors='raise')
        sdf['continent'] = sdf['continent'].str.replace('eeEurope', 'Europe', regex=True)
        sdf['continent'] = sdf['continent'].str.replace('eeAmerica', 'America', regex=True)
        if ((sdf[sdf['store_type'] == 'Web Portal'].to_dict()['store_type'])[0]) == 'Web Portal':
            ind = sdf[sdf['store_type'] == 'Web Portal'].any(axis=1).index
        il = []
        for i in (sdf[sdf['longitude'].isnull()].index):
            il.append(i)
        for i in il:
            if ind in il:
                il.remove(ind)
        for i in il:
            sdf = sdf.drop(index=i)

        return sdf

    def convert_product_weights(self, pdf=DataExtractor().extract_from_s3()):
        pdf = pdf.dropna()
        for weight in pdf.weight:
            if weight[-1:] == '.':
                pdf['weight'].replace('77g .','77g', inplace=True)
            if weight[-1:] != 'g' and weight[-1:] != 'l' and weight[-1:] != 'z':
                pdf = pdf[pdf.weight != weight]
            if 'x' in weight:
                index = weight.index('x')
                num1 = int(weight[:(index - 1)])
                num2 = int(weight[(index + 1):-1])
                total = num1 * num2
                stotal = str(total) + 'g'
                pdf['weight'].replace(weight, stotal, inplace=True)
        for weights in pdf.weight:
            if weights[-2:] != 'kg':
                if weights[-2:] == 'ml':
                    number = float(weights[:-2])
                    fnum = round((number/1000), 3)
                    fsnum = str(fnum) + 'kg'
                    pdf['weight'].replace(weights, fsnum, inplace=True)
                elif weights[-1:] == 'g':
                    number = float(weights[:-1])
                    fnum = round((number/1000), 3)
                    fsnum = str(fnum) + 'kg'
                    pdf['weight'].replace(weights, fsnum, inplace=True)
                elif weights[-2:] == 'oz':
                    number = float(weights[:-2])
                    fnumber = round(((number * 28.4131)/1000), 3)
                    snum = str(fnumber) + 'kg'
                    pdf['weight'].replace(weights, snum, inplace=True)
            else:
                number = float(weights[:-2])
                fnum = round(number, 3)
                fsnum = str(fnum) + 'kg'
                pdf['weight'].replace(weights, fsnum, inplace=True)

        return pdf

    def clean_products_data(self):
        pdf = self.convert_product_weights()
        pdf.product_name = pdf.product_name.astype('string', errors='raise')
        pdf.product_price = pdf.product_price.astype('string', errors='raise')
        pdf.weight = pdf.weight.astype('string', errors='raise')
        pdf.product_name = pdf.product_name.astype('string', errors='raise')
        pdf.category = pdf.category.astype('string', errors='raise')
        pdf.EAN = pd.to_numeric(pdf.EAN, errors='coerce')
        pdf.date_added = pd.to_datetime(pdf.date_added, errors='raise', infer_datetime_format=True)
        pdf.uuid = pdf.uuid.astype('object', errors='raise')
        pdf.removed = pdf.removed.astype('string', errors='raise')
        pdf.product_code = pdf.product_code.astype('object', errors='raise')
        pdf.rename(columns={'Unnamed: 0' : 'number'}, inplace=True)
        pdf = pdf.dropna()

        return pdf
    
    def clean_orders_data(self, orders_table=DataExtractor().read_rds_table()['orders']):
        orders_table = orders_table.drop(columns=['1','first_name','last_name'])

        return orders_table
    
    def clean_sales_data(self, sdf=DataExtractor().retrieve_sales_data()):
        sdf.timestamp = pd.to_datetime(sdf.timestamp, format='%H:%M:%S', errors='coerce').dt.time
        sdf.dropna(inplace=True)
        sdf.month = sdf.month.astype('int64', errors='raise')
        sdf.year = sdf.year.astype('int64', errors='raise')
        sdf.day = sdf.day.astype('int64', errors='raise')
        sdf.time_period = sdf.time_period.astype('string', errors='raise')

        return sdf

DataCleaning().clean_card_data()