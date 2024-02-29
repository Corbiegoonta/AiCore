from data_extraction import DataExtractor
import pandas as pd
from dateutil.parser import parse
import numpy as np

class DataCleaning:

    def __init__(self):
        pass

    def clean_user_data(self, user_details = DataExtractor().read_rds_table()['user_details']):
        # print(user_details.isnull().sum())
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
        # user_details.phone_number = user_details.phone_number.astype('int64', errors='raise')
        user_details.join_date = pd.to_datetime(user_details.join_date, infer_datetime_format=True, errors='coerce')
        user_details.replace('GGB', 'GB', inplace=True)
        # print(user_details.dtypes)
        # pn_regex = '^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$'
        # user_details.loc[~user_details['phone_number'].str.match(pn_regex), 'phone_number'] = np.nan
        # user_details['phone_number'] = user_details.loc[~user_details['phone_number'].str.match(pn_regex), 'phone_number'] 
        user_details = user_details.dropna()
        # print(len(user_details.index))
        # print(user_details.phone_number)
        print('The user data has been cleaned.')

        return user_details
    
    def clean_card_data(self, card_data = DataExtractor().retrieve_pdf_data()):
        print(card_data.isnull().sum())
        card_data.card_number = card_data.card_number.replace({r'\(': '',r'\)': '',r' ': '',r'-': '',r'\.': '',r'\+': '',r'[a-z]': '',r'\?': ''}, regex=True)
        card_data.card_number = pd.to_numeric(card_data.card_number, errors='coerce', downcast='integer')
        card_data.expiry_date = pd.to_datetime(card_data.expiry_date, format='%m/%y', errors='coerce')
        card_data.card_provider = card_data.card_provider.astype('string', errors='raise')
        card_data.date_payment_confirmed = pd.to_datetime(card_data.date_payment_confirmed, infer_datetime_format=True, errors='coerce')
        print(len(card_data.index))
        print(card_data.isnull().all())
        card_data = card_data.dropna()
        print(card_data[card_data['card_number'] == 4537509987455280000])
        pd.options.display.float_format = '{:.0f}'.format
        print(card_data[card_data['card_number'] == 4537509987455280000])
        print('The card details have been cleaned.')

        return card_data
    
    def called_clean_store_data(self, sdf = DataExtractor().retrieve_stores_data()):
        sdf = sdf.drop('lat', axis=1)
        # print(len(sdf.index))
        # print(sdf.loc[(sdf.index[0])])
        # sdf.loc[1:] = sdf.loc[1:].dropna(inplace=True)
        # print(sdf.loc[(sdf.index[0])])
        # print(len(sdf.index))
        # print(fr)
        # print(type(sdf.loc[1:]))
        # sdf = sdf.dropna()
        # fr = sdf.loc[(sdf.index[0])]
        # print(fr)
        # print(type(fr))
        # print(sdf.to_string())
        # sdf = sdf.drop((sdf.loc[(sdf == 'WEB-1388012W').any(axis=1)].index[0]), axis=0)
        # print(sdf.to_string())
        # print(sdf.loc[(sdf == 'HI-9B97EE4E').any(axis=1)].index[0])
        # for i in range(1, len(sdf.index)):
        #     # for j in range(1, (len(sdf.index) + 1)):
        #     sdf = sdf.loc[(sdf.index[i])]
        #         print(type(sdf))
        #         sdf = sdf.loc[(sdf.index[i])]
        # #     print(type(i))
            # if i != 'WEB-1388012W':
            #     sdf.longitude = pd.to_numeric(sdf.longitude, errors='coerce')
            # else:
            #     a = 1
        # print(sdf.loc[(sdf.index[0])])
        # print(sdf.loc[(sdf.index[1])])
        # print(len(sdf.index))
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
        # print(sdf.loc[(sdf.index[0])])
        # print(sdf.loc[(sdf.index[1])])
        # print(len(sdf.index))
        # il = []
        # for i in (sdf[sdf['longitude'].isnull()].index):
        #     il.append(i)
        # print(il)
        # print(type(sdf[sdf['longitude'].isnull()]).index)
        # print(len(sdf[sdf['longitude'].isnull()]))
        # print(sdf.isnull().)
        # print(sdf.iloc[0])
        # print(sdf.to_string())
        # sdf = sdf.dropna()
        # print(sdf.loc[-1])
        # sdf = sdf.sort_index().reset_index(drop=True)
        # sdf.index = sdf.index + 1  
        # sdf = sdf.sort_index()  
        # print(sdf.to_string())
        # print(sdf)
        # print(len(sdf.index))
        # print(sdf.to_string())
        # if sdf[sdf['store_type'] == 'Web Portal'].any(axis=1) is True:
        #     ind = sdf[sdf['store_type'] == 'Web Portal'].any(axis=1).index
        # if ((sdf[sdf['store_type'] == 'Web Portal'].to_dict()['store_type'])[0]) == 'Web Portal':
            # print('yes')
        # print(((sdf[sdf['store_type'] == 'Web Portal'].to_dict()['store_type'])[0]))
        # for i in sdf['store_code']:
        #     if i == 'n/a' or i == 'N/A' or i == 'null':
        #         print(sdf[sdf['store_code'] == i].any(axis=1))
        # print(sdf[sdf['store_code'] == 'WEB-1388012W'].any(axis=1).index)
        # print(sdf[sdf['longitude'].isnull()])
        # print(type(sdf[sdf['longitude'].isnull()]))
        # # print(sdf['longitude'])
        # if 'Web Portal' in sdf['store_type']:
        #     print('yes')
        # print(len(sdf.index))
        # print(sdf.loc[(sdf.index[0])])
        # sdf = sdf.dropna(subset='staff_numbers')
        # sdf = sdf.loc[1:].dropna()
        # print(sdf.loc[(sdf.index[0])])
        # print(len(sdf.index))

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