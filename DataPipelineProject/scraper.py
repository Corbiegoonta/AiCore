import errno
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import uuid
import pandas as pd
import json
import urllib.request
import boto3
import os
from credentials import access_key_id, secret_access_key


url = 'https://www.op.gg/'

class Scraper():

    def __init__(self): 
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--enable-automation")
        options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
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
        rank_button_container = self.driver.find_element(By.XPATH, '//div[@class="css-g46fbk ez6zw1e2"]')
        rank_button_container.click()
        time.sleep(2)
        all_rank_button = self.driver.find_element(By.XPATH, '//button[@class="css-w2p1w6 ez6zw1e3"]')
        all_rank_button.click()
        print("rank switched!")
        pass
    
    def click_win_rate(self):
        main_container = self.driver.find_element(By.XPATH, '//div[@class="css-g5c2cp e1fe8s350"]')
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
        main_container = self.driver.find_element(By.XPATH, '//div[@class="css-g5c2cp e1fe8s350"]')
        main1_container = main_container.find_element(By.XPATH, './main')
        stats_container = main1_container.find_element(By.XPATH, './div')
        stats_table = stats_container.find_element(By.XPATH, './table')
        body_contianer = stats_table.find_element(By.XPATH, './tbody')
        champion_rows = body_contianer.find_elements(By.XPATH, './tr')
        return champion_rows

    def get_patch(self):
        row_container = self.driver.find_element(By.XPATH, '//div[@class="css-gtm9xc e4k9iir3"]')
        indv_container = row_container.find_elements(By.XPATH, './nav')
        patch_button_container = indv_container[0].find_elements(By.XPATH, './div')
        patch_button_container1 = patch_button_container[5].find_element(By.XPATH, './div')
        patch_button_container2 = patch_button_container1.find_element(By.XPATH, './button')
        patch_button_container3 = patch_button_container2.find_element(By.XPATH, './span')
        patch = patch_button_container3
        return patch

    def get_champion_info(self):
        lanes_container = self.driver.find_element(By.XPATH, '//nav[@class="css-lk6zc e4k9iir1"]')
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
                patch_num = patch.text[-5:]
                self.display_dict['Patch'].append(patch_num)
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
                elif champion_name == 'renata glasc':
                    champion_name = 'renata'
                    champ_data.append(champion_name)
                else:
                    champion_name = list(champion_name)
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
                champion_page_link = f'https://www.leagueoflegends.com/en-gb/champions/{champion_name}/'
                self.driver.get(champion_page_link)
                time.sleep(1)
                self.accept_lol_page_cookies()
                time.sleep(1)
                image_contianer = self.driver.find_element(By.XPATH, '//div[@class="style__ForegroundAsset-sc-8gkpub-4 iwXvjZ"]')
                image_tag = image_contianer.find_element(By.XPATH, './img')
                image_link = image_tag.get_attribute('src')
                champ_data.append(image_link)
                champ_data.append(champion_page_link)
                champion_info[champion] = champ_data
                self.get_images(image_link, champion)
                counter += 1
        return champion_info


    def put_champion_links_in_dictionary(self, info_dict):
        for i in self.display_dict['Champion_Name']:
            self.display_dict['Champion_Page_Link'].append(info_dict[i][2])
        pass


    def create_uuid(self):
        for i in self.display_dict['Champion_Name']:
            indentifier = uuid.uuid4()
            self.display_dict['UUID'].append(str(indentifier))
        pass

    def create_dataframe(self):
        table = pd.DataFrame(self.display_dict)
        return table
    
    
    def create_folder(self, folder_name=r"\Champion Info", parent_directory=r"C:\Users\nickc\OneDrive\Desktop\Code\AiCore\DataPipelineProject"):
        try:
            path = parent_directory + folder_name 
            if not os.path.isdir(path):
                os.mkdir(path)
                print("Directory created.")
        except errno as e:
            print(e)
        pass

    def get_images(self, url, champion_name):
        urllib.request.urlretrieve(url, rf"C:\Users\nickc\OneDrive\Desktop\Code\AiCore\DataPipelineProject\Champion Info\{champion_name}.jpg")
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
        with open(r'C:\Users\nickc\OneDrive\Desktop\Code\AiCore\DataPipelineProject\Champion Info\champion_info.json', 'w') as raw_data_file:
            json.dump(json.dumps(self.display_dict, indent = 4), raw_data_file)

    def create_s3_bucket(self, bucket_name='lolchampiondata', Location='eu-west-2', 
        access_key_id=access_key_id, secret_access_key=secret_access_key):
        session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        s3 = session.resource('s3')
        try:
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': Location})
            print(f'The s3_bucket {bucket_name} was successfully created')
        except Exception as e:
            print(e)
        pass

    def upload_data_to_s3_bucket(self, file_name=r'C:\Users\nickc\OneDrive\Desktop\Code\AiCore\DataPipelineProject\Champion Info', bucket_name='lolchampiondata', 
        access_key_id=access_key_id, secret_access_key=secret_access_key):
        session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        s3 = session.resource('s3')
        bucket = s3.Bucket(bucket_name)
    
        list_of_files = os.listdir(file_name)
        for file in list_of_files:
            file_path = rf'C:\Users\nickc\OneDrive\Desktop\Code\AiCore\DataPipelineProject\Champion Info\{file}'
            file_name = os.path.basename(file_path)
            try:
                bucket.upload_file(file_path, file_name)
                print(f'{file} was uploaded to s3 bucket successfully.')
            except Exception as e:
                print(e)
        pass     


if __name__ == '__main__':   
    start = Scraper()


