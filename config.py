import logging
import os
import ssl
import sys
from enum import Enum

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

n_iterations = 10_000

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger('ticketmaster_availability')


EVENTS = [
    (
        'TOP Milan 28.05.2025',
        'https://shop.ticketmaster.it/tickets/buy-tickets-twenty-one-pilots-the-clancy-world-tour-28-april-2025-forum-assago-8877.html'
    ),
]


class Status(Enum):
    NOT_AVAILABLE = 0
    AVAILABLE = 1
