import errno
from typing import ChainMap
import requests
from selenium.webdriver import Chrome
from webdrivermanager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re
import uuid
import pandas as pd
import certifi
import ssl
import json
import urllib.request
from urllib.request import urlopen, Request
import boto3
from botocore.exceptions import ClientError
import os
import pymysql
from sqlalchemy import create_engine


url = 'https://www.op.gg/'

class Scraper():

    def __init__(self): 
        options = Options()
        #options.add_argument('--headless')
        self.driver = Chrome(r"C:\Users\nickc\OneDrive\Desktop\Code\AiCore\Data Pipeline Project\chromedriver")
        self.driver.maximize_window()
        self.display_dict = {
                        'Champion_Name' : [],
                        'Champion_Tier' : [],
                        'Win_Rate %' : [],
                        'Pick_Rate %' : [],
                        'Ban_Rate %' : [],
                        'Champion_Counters' : [],
                        'Lane' : [], 
                        'Champion_Rank' : [],
                        'Champion_Rank_Movement' : [],
                        'Champion_Page_Link' : [],
                        'Patch' : [],
                        'UUID' : []
        }
        pass

    def navigate_to_website(self):
        self.driver.get(url)
        time.sleep(1)
        pass

    def bypass_cookies(self):
        try:
            button_continer = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="qc-cmp2-summary-buttons"]')))
            buttons = button_continer.find_elements(By.XPATH, './button')
            accept_cookies_button = buttons[1]
            accept_cookies_button.click()
        except Exception:
            print("No cookies found.")
        pass
    
    def get_latest_page(self):
        time.sleep(2)
        champions_link = self.driver.find_element(By.XPATH, '//a[@href="/champions"]')
        champions_link.click()
        time.sleep(2)
        pass

    def get_lane(self):
        lanes_container = self.driver.find_element(By.XPATH, '//nav[@class="css-1wrsp9i e14ouzjd5"]')
        lanes = lanes_container.find_elements(By.XPATH, './button')
        for i in range(1, 5):
            time.sleep(2)
            lanes[i].click()
            time.sleep(2)
        pass
    
    def switch_region_to_global(self):
        try:
            region_button_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-1dgy7lj e5qh6tw1"]')))
            region_buttton_whole = region_button_container.find_element(By.XPATH, './div')
            region_buttton_whole1 = region_buttton_whole.find_element(By.XPATH, './button')
            region_buttton_whole1.click()
            time.sleep(2)
            global_button = self.driver.find_element(By.XPATH, '//button[@class="region_filter css-1mye3k2 e5qh6tw0"]')
            global_button.click()
            print("region switched!")
        except Exception:
            self.driver.refresh()
            self.get_latest_page()
            self.bypass_cookies()
        pass

    def switch_rank_to_all(self):
        rank_button_container = self.driver.find_element(By.XPATH, '//div[@class="css-1b4j62k e5qh6tw1"]')
        rank_button_container.click()
        time.sleep(2)
        global_button = self.driver.find_element(By.XPATH, '//button[@class="css-16v6t24 e5qh6tw0"]')
        global_button.click()
        print("rank switched!")
        pass
    
    def click_win_rate(self):
        main_container = self.driver.find_element(By.XPATH, '//div[@class="css-1fcwcq0 e2v0byd0"]')
        main1_container = main_container.find_element(By.XPATH, './main')
        stats_container = main1_container.find_element(By.XPATH, './div')
        stats_table = stats_container.find_element(By.XPATH, './table')
        column_header_contianer = stats_table.find_element(By.XPATH, './thead')
        column_headers = column_header_contianer.find_element(By.XPATH, './tr')
        individual_headers = column_headers.find_elements(By.XPATH, './th')
        win_rate = individual_headers[3]
        win_rate.click()
        pass

    def get_champion_rows(self):
        main_container = self.driver.find_element(By.XPATH, '//div[@class="css-1fcwcq0 e2v0byd0"]')
        main1_container = main_container.find_element(By.XPATH, './main')
        stats_container = main1_container.find_element(By.XPATH, './div')
        stats_table = stats_container.find_element(By.XPATH, './table')
        body_contianer = stats_table.find_element(By.XPATH, './tbody')
        champion_rows = body_contianer.find_elements(By.XPATH, './tr')
        return champion_rows

    def get_patch(self):
        row_container = self.driver.find_elements(By.XPATH, '//div[@class="css-bnue16 e14ouzjd3"]')
        info_container = row_container[0]
        patch_number_container = info_container.find_elements(By.XPATH, '//div[@class="css-gfgr92 e5qh6tw3"]')
        patch_button_container = patch_number_container[1].find_element(By.XPATH, './label')
        patch_button_container1 = patch_button_container.get_attribute("for")
        patch = patch_button_container1
        return patch

    def get_champion_info(self):
        lanes_container = self.driver.find_element(By.XPATH, '//nav[@class="css-1wrsp9i e14ouzjd5"]')
        lanes = lanes_container.find_elements(By.XPATH, './button')
        time.sleep(2)
        lanes[1].click()
        time.sleep(2)
        for i in range(0, 5):
            time.sleep(2)
            lanes[i].click()
            time.sleep(2)
            all_champion_rows = self.get_champion_rows()
            number = 0
            for j in all_champion_rows:
                patch = self.get_patch()
                self.display_dict['Patch'].append(patch)
                self.display_dict['Lane'].append(lanes[i].text)
                champion_info_columns = j.find_elements(By.XPATH, './td')
                rank_and_movement = champion_info_columns[0].find_elements(By.XPATH, './span')
                if rank_and_movement != [] and rank_and_movement[0].text != '':
                    self.display_dict['Champion_Rank'].append(int(rank_and_movement[0].text))
                    self.display_dict['Champion_Rank_Movement'].append(int(rank_and_movement[1].text))
                    number += 1
                champion_name_contianer = champion_info_columns[1].find_element(By.XPATH,'./a')
                champion_name = champion_name_contianer.find_element(By.XPATH, './strong')
                self.display_dict['Champion_Name'].append(champion_name.text)
                champion_tier = champion_info_columns[2]
                self.display_dict['Champion_Tier'].append(int(champion_tier.text))
                champion_win_rate = champion_info_columns[3]
                self.display_dict['Win_Rate %'].append(float((champion_win_rate.text)[:-1]))
                champion_pick_rate = champion_info_columns[4]
                self.display_dict['Pick_Rate %'].append(float((champion_pick_rate.text)[:-1]))
                champion_ban_rate = champion_info_columns[5]
                self.display_dict['Ban_Rate %'].append(float((champion_ban_rate.text)[:-1]))
                champion_counters_container = champion_info_columns[6]
                champion_counters_containers = champion_counters_container.find_elements(By.XPATH, './a')
                champion_counter_list = []
                for k in champion_counters_containers:
                    champion_counters_container1 = k.find_element(By.XPATH, './div')
                    champion_counters = champion_counters_container1.find_element(By.TAG_NAME, 'img')
                    champion_counter1 = champion_counters.get_attribute("alt")
                    champion_counter_list.append(champion_counter1)
                self.display_dict['Champion_Counters'].append(champion_counter_list) 
        try:
            names_links = self.get_unique_champion_name_and_link()      
            self.put_champion_links_in_dictionary(names_links)
        except Exception as e:
                print(e)
        print(self.display_dict['Lane'])
        print(len((self.display_dict['Lane'])))
        print(self.display_dict['Champion_Rank'])
        print(len(self.display_dict['Champion_Rank']))
        print(self.display_dict['Champion_Rank_Movement'])
        print(len(self.display_dict['Champion_Rank_Movement']))
        print(self.display_dict['Champion_Name'])
        print(len(self.display_dict['Champion_Name']))
        print(self.display_dict['Champion_Tier'])
        print(len(self.display_dict['Champion_Tier']))
        print(self.display_dict['Win_Rate %'])
        print(len(self.display_dict['Win_Rate %']))
        print(self.display_dict['Pick_Rate %'])
        print(len(self.display_dict['Pick_Rate %']))
        print(self.display_dict['Ban_Rate %'])
        print(len(self.display_dict['Ban_Rate %']))
        print(self.display_dict['Champion_Counters'])
        print(len(self.display_dict['Champion_Counters']))
        print(self.display_dict['Champion_Page_Link'])
        print(len(self.display_dict['Champion_Page_Link']))
        print(self.display_dict['Patch'])
        print(len((self.display_dict['Patch'])))
        print(number)
        pass
    
    def get_unique_champion_name_and_link(self):
        champion_info = {}
        counter = 1
        for champion in self.display_dict['Champion_Name']:
            champ_data = []
            if champion not in champion_info:
                champion_name = champion.lower()
                if champion_name == 'nunu & willump':
                    champion_name = 'nunu'
                    champ_data.append(champion_name)
                    print(champion_name)
                elif champion_name == 'renata glasc':
                    champion_name = 'renata'
                    champ_data.append(champion_name)
                    print(champion_name) 
                else:
                    champion_name = list(champion_name)
                    print(champion_name)
                    champion_name_list_counter = 0
                    switch_check = True 
                    for i in champion_name:
                        if i.isalpha() is False and switch_check is True:
                            champion_name[champion_name_list_counter] = '-'
                            switch_check = False
                        elif i.isalpha() is False and switch_check is False:
                            champion_name.pop(champion_name_list_counter)
                        champion_name_list_counter += 1
                    champion_name = ''.join(champion_name)
                    champ_data.append(champion_name)
                    print(champion_name)
                self.driver.get(f'https://www.leagueoflegends.com/en-gb/champions/{champion_name}/')
                time.sleep(1)
                self.accept_lol_page_cookies()
                time.sleep(1)
                image_contianer = self.driver.find_element(By.XPATH, '//div[@class="style__BackgroundImage-sc-8gkpub-2 WSJaH"]')
                image_tag = image_contianer.find_element(By.XPATH, './img')
                image_link = image_tag.get_attribute('src')
                champ_data.append(image_link)
                champion_info[champion] = champ_data
                counter += 1
            print(counter)
        print(champion_info)
        return champion_info


    def put_champion_links_in_dictionary(self, info_dict):
        for i in self.display_dict['Champion_Name']:
            self.display_dict['Champion_Page_Link'].append(info_dict[i][1])
        print(self.display_dict['Champion_Page_Link'])
        pass


    def create_uuid(self):
        for i in self.display_dict['Champion_Name']:
            indentifier = uuid.uuid4()
            self.display_dict['UUID'].append(str(indentifier))
        print(self.display_dict['UUID'])
        print(len(self.display_dict['UUID']))
        print(len(self.display_dict['Champion_Name']))
        pass

    def create_dataframe(self):
        table = pd.DataFrame(self.display_dict)
        print(table)
        return table
    
    
    def create_folder(self, folder_name=r"\Champion Info", parent_directory=r"C:\Users\nickc\OneDrive\Desktop\Code\AiCore\Data Pipeline Project"):
        try:
            path = parent_directory + folder_name 
            if not os.path.isdir(path):
                os.mkdir(path)
                print("Directory created.")
                print(path)
        except errno as e:
            print(e)
        pass

    def get_images(self, url, champion_name):
        urllib.request.urlretrieve(url, rf"C:\Users\nickc\OneDrive\Desktop\Code\AiCore\Data Pipeline Project\Champion Info\{champion_name}.jpg")
        pass

    def accept_lol_page_cookies(self):
        try:
            time.sleep(2)
            accept_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="osano-cm-accept-all osano-cm-buttons__button osano-cm-button osano-cm-button--type_accept"]')))
            accept_button.click()
        except Exception as e:
            print(e)
        pass

    def accept_lol_pic_page_cookies(self):
        try:
            accept_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="osano-cm-accept-all osano-cm-buttons__button osano-cm-button osano-cm-button--type_accept"]')))
            accept_button.click()
        except Exception:
            print("No cookies found.")
        pass

    def create_json_file(self):
        with open(r'C:\Users\nickc\OneDrive\Desktop\Code\AiCore\Data Pipeline Project\Champion Info\champion_info.json', 'w') as raw_data_file:
            json.dump(json.dumps(self.display_dict, indent = 4), raw_data_file)

    def create_s3_bucket(self, bucket_name='lolchampiondata', Location='eu-west-2', 
        access_key_id='AKIA4BMRGIVBJ5AVGRII', secret_access_key='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'):
        session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        s3 = session.resource('s3')
        try:
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': Location})
            print(f'The s3_bucket {bucket_name} was successfully created')
        except Exception as e:
            print(e)
        pass

    def upload_data_to_s3_bucket(self, file_name='Champion Info/', bucket_name='lolchampiondata', 
        access_key_id='AKIA4BMRGIVBJ5AVGRII', secret_access_key='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'):
        session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        s3 = session.resource('s3')
        bucket = s3.Bucket(bucket_name)
    
        list_of_files = os.listdir(file_name)
        for file in list_of_files:
            file_path = rf'C:\Users\nickc\OneDrive\Desktop\Code\AiCore\Data Pipeline Project\Champion Info\{file}'
            file_name = os.path.basename(file_path)
            try:
                bucket.upload_file(file_path, file_name)
                print('File was uploaded to s3 bucket successfully.')
            except Exception as e:
                print(e)
        pass
    
    def upload_dataframe_to_rds1(self, host = 'lolchampiondatabase.cudnxxlhkqef.eu-west-2.rds.amazonaws.com',
        port = int(3306),
        user = 'corbie',
        password = 'leagueoflegends',
        database = 'lolchampiondatabase'):
        
        try:
            champion_dataframe = self.create_dataframe()
            print(f'Dataframe {champion_dataframe} was created succefully.')
        except Exception as e:
            print('Creation of dataframe was unsuccessful.')
            print(e)
        
        conn = pymysql.connect(host=host, user=user, passwd=password, connect_timeout=10)
        with conn.cursor() as cur:
            cur.execute('create database bsb-round;')
            
        try:
            championdatadb = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + ':' + str(port) + '/' + database , echo=False)
            print('Create_engine successful.')
            champion_dataframe.to_sql(name='finalchampdb', con=championdatadb, if_exists='replace', index=False)
            print('To_sql successful.')
        except Exception as e:
            print(e)
        pass


    def upload_dataframe_to_rds2(host = 'lolchampiondatabase.cudnxxlhkqef.eu-west-2.rds.amazonaws.com',
        port = str(3306),
        user = 'corbie',
        password = 'leagueoflegends',
        rds_database = 'lolchampiondatabase',
        sql_database = 'tabl'):
        
        alcheng = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + ':' + port + '/' + sql_database , echo=False)
        
        connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=sql_database)

        cursor = connection.cursor()
        
        try:
            dblist = cursor.execute('SHOW DATABASES')
            print('Sql shown successfully.1')
        except Exception as e:
            print('Sql database was not shown.1')

        try:
            cursor.execute(f'CREATE DATABASE {sql_database}')
            print('Sql database created successfully.')
        except Exception as e:
            print(e)
            print('Sql database was not created.')

        try:
            cursor.execute('SHOW TABLES')
            print('Sql shown tables successfully.2')
        except Exception as e:
            print(e)
            print('Sql tables were not shown.2')

        for i in cursor:
            print(i)

        try:
            test_dict = {'apple' : [1]}
            test_df = pd.DataFrame(test_dict)
            print('Dataframe was created succefully.')
        except Exception as e:
            print('Creation of dataframe was unsuccessful.')
            print(e)
        
        try:
            test_df.to_sql(name='Champion_Data_Table', con=alcheng, if_exists='replace', index=False)
            print('To_sql successful.')
        except Exception as e:
            print(e)
        pass

        cursor.execute('SELECT * FROM Champion_Data_Table')

        cursor.fetchall()

        for i in cursor:
            print(i)
        
        connection.close()

        

       
if __name__ == '__main__':   
    start = Scraper()

