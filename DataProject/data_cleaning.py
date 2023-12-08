from data_extraction import DataExtractor
import pandas as pd
from dateutil.parser import parse
import numpy as np

class DataCleaning:

    def __init__(self):
        pass

    def clean_user_data(self, user_details = DataExtractor().read_rds_table()):
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
    
    def clean_card_data(self, card_data = DataExtractor().retrieve_pdf_data()):
        card_data.card_number = pd.to_numeric(card_data.card_number, errors='coerce')
        card_data.expiry_date = pd.to_datetime(card_data.expiry_date, format='%m/%y', errors='coerce')
        card_data.card_provider = card_data.card_provider.astype('string', errors='raise')
        card_data.date_payment_confirmed = pd.to_datetime(card_data.date_payment_confirmed, infer_datetime_format=True, errors='coerce')
        card_data = card_data.dropna()
        print('The card details have been cleaned.')
        return card_data
    
    def called_clean_store_data(self, sdf = DataExtractor().retrieve_stores_data()):
        # try:  
            # sdf.info()
            # print(sdf)
            sdf = sdf.drop('lat', axis=1)
            sdf.longitude = pd.to_numeric(sdf.longitude, errors='coerce')
            sdf = sdf.dropna()
            sdf.address = sdf.address.astype('string', errors='raise')
            sdf.locality = sdf.locality.astype('string', errors='raise')
            sdf.store_code = sdf.store_code.astype('string', errors='raise')
            sdf.staff_numbers = pd.to_numeric(sdf.staff_numbers, errors='coerce')
            sdf.opening_date = pd.to_datetime(sdf.opening_date, infer_datetime_format=True, errors='coerce')
            sdf.store_type = sdf.store_type.astype('string', errors='raise')
            sdf.latitude = pd.to_numeric(sdf.latitude, errors='coerce')
            sdf.country_code = sdf.country_code.astype('string', errors='raise')
            sdf.continent = sdf.continent.astype('string', errors='raise')
            sdf['continent'] = sdf['continent'].str.replace('eeEurope', 'Europe', regex=True)
            sdf['continent'] = sdf['continent'].str.replace('eeAmerica', 'America', regex=True)
            # sdf.info()
            # sdfdict = sdf.to_dict()
            # print(sdfdict)
        # except Exception as e:
        #     print(e)
            return sdf
    pass

    def convert_product_weights(self, pdf=DataExtractor().extract_from_s3()):
        pdf = pdf.dropna()
        # pdf['weight'].replace('77g .','77g', inplace=True)
        for weight in pdf.weight:
            # if type(weight) is float:
            #     print(weight)
            #  print(type(weight))
            if weight[-1:] == '.':
                pdf['weight'].replace('77g .','77g', inplace=True)
                # print('a')
                # while weight[-1:] != 'g':
                #     pdf.weight = weight.replace(weight[-1:],'',inplace=True)
                #     print('b')
                #     print(len(weight))
                #     print(weight)
            if weight[-1:] != 'g' and weight[-1:] != 'l' and weight[-1:] != 'z':
                # print(weight)
                pdf = pdf[pdf.weight != weight]
            if 'x' in weight:
                index = weight.index('x')
                num1 = int(weight[:(index - 1)])
                num2 = int(weight[(index + 1):-1])
                total = num1 * num2
                stotal = str(total) + 'g'
                # print(stotal)
                pdf['weight'].replace(weight, stotal, inplace=True)
        # print(pdf)
        # for weights in pdf.weight:
        #     if weights[-1:] != 'g' and weights[-1:] != 'l' and weights[-1:] != 'z':
                    # print(weights)
        for weights in pdf.weight:
            if weights[-2:] != 'kg':
                if weights[-2:] == 'ml':
                    number = float(weights[:-2])
                    # print(number)
                    fnum = round((number/1000), 3)
                    # print(fnum)
                    fsnum = str(fnum) + 'kg'
                    # print(fsnum)
                    pdf['weight'].replace(weights, fsnum, inplace=True)
                elif weights[-1:] == 'g':
                    number = float(weights[:-1])
                    # print(number)
                    fnum = round((number/1000), 3)
                    # print(fnum)
                    fsnum = str(fnum) + 'kg'
                    # print(fsnum)
                    pdf['weight'].replace(weights, fsnum, inplace=True)
                elif weights[-2:] == 'oz':
                    number = float(weights[:-2])
                    # print(number)
                    fnumber = round(((number * 28.4131)/1000), 3)
                    # print(fnumber)
                    snum = str(fnumber) + 'kg'
                    # print(snum)
                    pdf['weight'].replace(weights, snum, inplace=True)
            else:
                number = float(weights[:-2])
                # print(number)
                fnum = round(number, 3)
                # print(fnum)
                fsnum = str(fnum) + 'kg'
                # print(fsnum)
                pdf['weight'].replace(weights, fsnum, inplace=True)
        # print(pdf.to_string())
        # pdf.value_counts()
        # for i in pdf.weight:
        # # # # #     if 'kg' not in i:
        # # # # #         print(i)
            # print(i)
            # print(type(i))
            #     index = weights.index('x')
            #     num1 = int(weights[:(index - 1)])
            #     num2 = int(weights[(index + 2):-1])
            #     total = num1 * num2
            #     stotal = str(total) + 'g'
            #     # print(stotal)
            #     pdf['weight'].replace(weights, stotal, inplace=True)
        # for weights in pdf.weight:
        #     if 'oz' in weights:
        #         print(weights)
            # if weights[-2:] == 'ml':
            #     a = None
            # elif weights[-2:] == 'oz':
            #     a = None
            # elif weights[-2:] == 'kg':
            #     a = None
            # else:
                # if 'x' in weights:
                #     print(weights)
                # print(weights)

        return pdf

    def clean_products_data(self):
        pdf = self.convert_product_weights()
        pdf.product_name = pdf.product_name.astype('string', errors='raise')
        pdf.product_price = pdf.product_price.astype('string', errors='raise')
        pdf.weight = pdf.weight.astype('string', errors='raise')
        pdf.product_name = pdf.product_name.astype('string', errors='raise')
        pdf.category = pdf.category.astype('string', errors='raise')
        pdf.EAN = pd.to_numeric(pdf.EAN, errors='coerce')
        pdf.date_added = pd.to_datetime(pdf.date_added, format='%Y-%m-%d', errors='coerce')
        pdf.uuid = pdf.uuid.astype('object', errors='raise')
        pdf.removed = pdf.removed.astype('string', errors='raise')
        pdf.product_code = pdf.product_code.astype('object', errors='raise')
        pdf.rename(columns={'Unnamed: 0' : 'number'}, inplace=True)
        pdf = pdf.dropna()
        pdf.info()
        # for i in pdf:
        #     print(i)
        return pdf

# DataCleaning().clean_user_data()
DataCleaning().clean_products_data()