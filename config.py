import os
import ssl

import easyocr
import telebot
from selenium.webdriver.chrome.options import Options

ssl._create_default_https_context = ssl._create_unverified_context

chrome_options = Options()
chrome_options.add_argument("--headless")

my_id = os.environ['TG_MY_ID']
api_token = os.environ['TG_BOT_API_TOKEN']
tg_bot = telebot.TeleBot(api_token)

sleep_times = {
    'init': os.environ.get('SLEEP_INIT', 3),
    'after_enter': os.environ.get('SLEEP_AFTER_ENTER', 5),
    'between_calls': os.environ.get('SLEEP_BETWEEN_CALLS', 60),
}

reader = easyocr.Reader(['en'], gpu=False, recog_network='english_g2')
