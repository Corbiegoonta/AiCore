from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# driver = Chrome(ChromeDriverManager().install())
# driver.get('https://www.displayspecifications.com/en')
# time.sleep(2)
# accept_cookies = driver.find_element_by_xpath('//a[@id="cookie_consent_accept"]')
# accept_cookies.click()
# search_bar = driver.find_element_by_xpath('//input[@id="search"]')
# search_bar.click
# search_bar.send_keys('Samsung')



class Scraper():

    def __init__(self, url:str = None): 
        """add maximise window"""
        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.display_dict = {
                        'Brand' : [],
                        'Year' : [],
                        'Model' : [],
                        'Link' : [],
                        'Screen_Size' : [],
                        'Resolution' : [],
                        'Refresh_Rate' : [],
                        'Brightness' : [],
                        'Asepect_Ratio' : [],
                        'Pixel_Density' : [],
                        'Connectivity' : [],
                        'Audio' : []
        }
        pass

    def navigate_to_website(self, url='https://www.displayspecifications.com/en'):
        self.driver.get(url)
        time.sleep(2)
        pass

    def bypass_cookies(self, cookie_xpath='//a[@id="cookie_consent_accept"]'):
        try:
            accept_cookies = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, cookie_xpath)))
            accept_cookies.click()
        except TimeoutException:
            print("No cookies found.")
        pass

    def search(self, search_xpath=None, search_item=None, search_buttons=None):
        search_bar = self.driver.find_element_by_xpath(search_xpath)
        search_bar.click
        search_bar.send_keys(search_item)
        search_bar.send_keys(Keys.ENTER)
        # search_bar = self.driver.find_element_by_xpath(search_xpath)
        # search_bar.click
        # search_bar.send_keys(search_item)
        # search_button = self.driver.find_element_by_xpath(search_buttons)
        # search_button.click()
        pass

    def get_brand_container(self):
        self.container = self.driver.find_element(By.XPATH, '//div[@class="brand-listing-container-frontpage"]')
        return self.container

    def get_main_container(self):
        self.main_container = self.driver.find_element(By.XPATH, '//div[@id="main"]')
        return self.main_container

    def get_model_year(self):
        self.tables_container = self.driver.find_element(By.XPATH, '//div[@style="width: 100%; margin-top: 20px;"]')
        all_tables = self.tables_container.find_elements(By.XPATH, './table')
        model_year_table = all_tables[0].find_element(By.XPATH, './tbody')
        rows_in_table = model_year_table.find_elements(By.XPATH, './tr')
        model_year_row = rows_in_table[4]
        model_year_cells = model_year_row.find_elements(By.XPATH, './td')
        model_year = model_year_cells[1].text
        return model_year

    def get_model(self):
        self.tables_container = self.driver.find_element(By.XPATH, '//div[@style="width: 100%; margin-top: 20px;"]')
        all_tables = self.tables_container.find_elements(By.XPATH, './table')
        model_year_table = all_tables[0].find_element(By.XPATH, './tbody')
        rows_in_table = model_year_table.find_elements(By.XPATH, './tr')
        model_year_row = rows_in_table[2]
        model_cells = model_year_row.find_elements(By.XPATH, './td')
        model = model_cells[1].text
        return model

    def get_screen_size(self):
        self.tables_container = self.driver.find_element(By.XPATH, '//div[@style="width: 100%; margin-top: 20px;"]')
        all_tables = self.tables_container.find_elements(By.XPATH, './table')
        display_table = all_tables[1].find_element(By.XPATH, './tbody')
        rows_in_table = display_table.find_elements(By.XPATH, './tr')
        size_row = rows_in_table[0]
        size_cell = size_row.find_elements(By.XPATH, './td')
        size = size_cell[1].text
        size = ''.join(size)
        size = float(size[:-12])
        return size

    def create_uuid(self):
        pass

    def close_ads(self):
        time.sleep(5)
        self.driver.refresh()
        pass


    def get_hyperlinks(self):
        brand_container = self.get_brand_container()
        raw_brand_list = brand_container.find_elements(By.XPATH, './a')
        for i in raw_brand_list:
            brand_store = i.text
            i.click()
            main_container = self.get_main_container()
            raw_product_container_list = main_container.find_elements(By.XPATH, './div')
            for j in raw_product_container_list:
                raw_product_list = j.find_elements(By.XPATH, './div')
                for k in raw_product_list:
                    try:
                        #time.sleep(5)
                        final_product_link = k.find_element(By.XPATH, './a')
                        link = final_product_link.get_attribute('href')
                        self.display_dict['Link'].append(link)
                        # self.driver.get(link)
                        # time.sleep(5)
                        # self.display_dict['Brand'].append(brand_store)
                        # self.display_dict['Year'].append(int(self.get_model_year()))
                        # self.display_dict['Model'].append(self.get_model())
                        # self.display_dict['Screen_Size'].append(self.get_screen_size())
                        # print(self.display_dict)
                        self.driver.back()
                        # time.sleep(5)
                    except Exception:
                        print("Ad Detected!")
                        #self.close_ads()
            self.driver.get('https://www.displayspecifications.com/en')

            #self.driver.back()
            
            
        
       

    # def test(self):
    #     # self.driver.get('https://www.displayspecifications.com/en')
    #     # #try:
    #     # #     WebDriverWait(self.driver, 5)until.
    #     # time.sleep(2)
    #     # accept_cookies = self.driver.find_element_by_xpath('//a[@id="cookie_consent_accept"]')
    #     # accept_cookies.click()
    #     search_bar = self.driver.find_element_by_xpath('//input[@id="search"]')
    #     search_bar.click
    #     search_bar.send_keys('Samsung')
    #     search_bar.send_keys(Keys.ENTER)

       
if __name__ == '__main__':   
    start = Scraper()

