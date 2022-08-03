import unittest
from scraper import Scraper, url
import requests

bot = Scraper()

class TestScraper(unittest.TestCase):

    bot = Scraper()
        
    def test_navigate_to_website(self):
        self.bot.navigate_to_website()
        actual_url = self.bot.driver.current_url
        expected_url = url
        self.assertEqual(actual_url, expected_url)
        pass

    def test_bypass_cookies(self):
        pass

    def test_get_latest_page(self):
        pass

    def test_get_lane(self):
        pass
    
    def test_switch_region_to_global(self):
        self.bot.driver.get('https://euw.op.gg/champions')
        self.bot.bypass_cookies()
        actual = self.bot.switch_region_to_global()
        expected = print("region switched!")
        self.assertEqual(actual, expected)
        pass
    
    def test_switch_rank_to_all(self):
        pass

    def test_click_win_rate(self):
        pass

    def test_get_champion_rows(self):
        pass

    def test_get_champion_info(self):
        pass

    def test_create_uuid(self):
        pass

    def test_create_dataframe(self):
        pass

    def test_accept_google_cookies(self):
        pass

    def test_get_images(self):
        pass

    def test_accept_lol_page_cookies(self):
        pass

    def test_create_json_file(self):
        pass