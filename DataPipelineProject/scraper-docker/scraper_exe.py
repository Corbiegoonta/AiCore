from scraper_docker import Scraper

bot = Scraper()
bot.navigate_to_website()
bot.bypass_cookies()
bot.get_latest_page()
bot.bypass_cookies()
bot.switch_region_to_global()
bot.switch_rank_to_all()
bot.click_win_rate()
bot.create_folder()
bot.get_champion_info()
bot.create_uuid()
bot.create_dataframe()
bot.create_json_file()
bot.create_s3_bucket()
bot.upload_data_to_s3_bucket()