from cgitb import text
from typing import ChainMap
import requests
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
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
import json
import urllib.request
from urllib.request import urlopen, Request

url = 'https://www.op.gg/'

class Scraper():

    def __init__(self): 
        options = Options()
        #options.add_argument('--headless')
        self.driver = Chrome(ChromeDriverManager().install(), options=options)
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
        time.sleep(2)
        pass

    def bypass_cookies(self):
        try:
            time.sleep(10)
            button_continer = WebDriverWait(self.driver, 240).until(EC.presence_of_element_located((By.XPATH, '//div[@class="qc-cmp2-summary-buttons"]')))
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
        rank_button_container = self.driver.find_element(By.XPATH, '//div[@class="css-1irfcct e5qh6tw1"]')
        rank_button_container.click()
        time.sleep(2)
        global_button = self.driver.find_element(By.XPATH, '//button[@class="css-16v6t24 e5qh6tw0"]')
        global_button.click()
        print("rank switched!")
        pass
    
    def click_win_rate(self):
        main_container = self.driver.find_element(By.XPATH, '//div[@class="css-1fcwcq0 e2v0byd0"]')
        print(main_container)
        main1_container = main_container.find_element(By.XPATH, './main')
        stats_container = main1_container.find_element(By.XPATH, './div')
        stats_table = stats_container.find_element(By.XPATH, './table')
        column_header_contianer = stats_table.find_element(By.XPATH, './thead')
        column_headers = column_header_contianer.find_element(By.XPATH, './tr')
        print(column_headers)
        individual_headers = column_headers.find_elements(By.XPATH, './th')
        win_rate = individual_headers[3]
        print(win_rate)
        win_rate.click()
        pass

    def get_champion_rows(self):
        main_container = self.driver.find_element(By.XPATH, '//div[@class="css-1fcwcq0 e2v0byd0"]')
        print(main_container)
        main1_container = main_container.find_element(By.XPATH, './main')
        stats_container = main1_container.find_element(By.XPATH, './div')
        stats_table = stats_container.find_element(By.XPATH, './table')
        body_contianer = stats_table.find_element(By.XPATH, './tbody')
        champion_rows = body_contianer.find_elements(By.XPATH, './tr')
        return champion_rows

    def get_patch(self):
        patch_button_container = self.driver.find_element(By.XPATH, '//button[@class="css-ee3hyw e5qh6tw2"]')
        patch = patch_button_container.text
        print(patch)
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
                champion_counters_container1 = champion_counters_container.find_elements(By.XPATH, './div')
                champion_counter_list = []
                for k in champion_counters_container1:
                    champion_counter = k.find_element(By.TAG_NAME, 'img')
                    champion_counter1 = champion_counter.get_attribute("alt")
                    champion_counter_list.append(champion_counter1)
                self.display_dict['Champion_Counters'].append(champion_counter_list)
        dict_counter = 0
        for l in self.display_dict['Champion_Name']:
            try:
                self.get_champion_page(l)
                self.get_images(self.display_dict['Champion_Page_Link'][dict_counter], l)
                dict_counter += 1
            except Exception:
                print("no pic")
                self.driver.refresh()
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
        pass

    def get_champion_page(self, champion):
        champion_name = champion.lower()
        if champion_name == 'nunu & willump':
            champion_name = 'nunu'
            print(champion_name)
        elif champion_name == 'renata glasc':
            champion_name = 'renata'
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
            print(champion_name)            
        self.driver.get(f'https://www.leagueoflegends.com/en-gb/champions/{champion_name}/')
        time.sleep(2)
        self.accept_lol_page_cookies()
        time.sleep(1)
        image_contianer = self.driver.find_element(By.XPATH, '//div[@class="style__ForegroundAsset-sc-8gkpub-4 fyyYJz"]')
        image_tag = image_contianer.find_element_by_tag_name('img')
        image_link = image_tag.get_attribute('src')
        self.display_dict['Champion_Page_Link'].append(image_link)
        # image = requests.get(image_link).content
        # with open(f'{champion}.jpg', 'wb') as champion_image:
        #     champion_image.write(image)
        pass

    def get_images(self, url, champion_name):
        urllib.request.urlretrieve(url, rf'C:\Users\nickc\Documents\scratch\AiCore\Data Pipeline Project\Champion Images\{champion_name}.jpg')
        pass

    def accept_lol_page_cookies(self):
        try:
            time.sleep(2)
            accept_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="osano-cm-accept-all osano-cm-buttons__button osano-cm-button osano-cm-button--type_accept"]')))
            accept_button.click()
        except Exception:
            print("No cookies found.")
        pass

    def accept_lol_pic_page_cookies(self):
        try:
            accept_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="osano-cm-accept-all osano-cm-buttons__button osano-cm-button osano-cm-button--type_accept"]')))
            accept_button.click()
        except Exception:
            print("No cookies found.")
        pass

    def create_json_file(self):
        with open('champion_info.json', 'w') as raw_data_file:
            json.dump(json.dumps(self.display_dict, indent = 4), raw_data_file)
       
if __name__ == '__main__':   
    start = Scraper()

