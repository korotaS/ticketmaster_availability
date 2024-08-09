import io
from time import sleep

import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import chrome_options, tg_bot, sleep_times, my_id, reader

url = 'https://shop.ticketmaster.it/tickets/buy-tickets-twenty-one-pilots-the-clancy-world-tour-28-april-2025-forum-assago-8877.html'

captcha_tracker = []

statuses = {}
good_status = 'available'
bad_status = 'not available'

for i in range(10_000):
    driver = webdriver.Chrome(options=chrome_options)
    print('driver init')

    try:
        driver.get(url)

        sleep(sleep_times['init'])

        try:
            elem = driver.find_element(By.CLASS_NAME, 'captcha-code')
        except Exception as e:
            print(i, 'couldnt find captcha element')
            print()
            driver.quit()
            sleep(sleep_times['between_calls'])
            continue
        image = Image.open(io.BytesIO(elem.screenshot_as_png))
        result = reader.readtext(np.array(image))
        if not result or not result[0]:
            print(i, f'Empty captcha')
            print()
            driver.quit()
            sleep(sleep_times['between_calls'])
            continue
        captcha_text = result[0][1].upper()
        print(i, f'Captcha: {captcha_text}')

        elem_input = driver.find_element(By.CLASS_NAME, 'botdetect-input')
        elem_input.send_keys(captcha_text)
        elem_input.send_keys(Keys.ENTER)

        sleep(sleep_times['after_enter'])

        try:
            driver.find_element(By.CLASS_NAME, 'text_h3')
        except Exception as e:
            captcha_tracker.append(0)
            captcha_percent = sum(captcha_tracker) * 100 / len(captcha_tracker)
            print(i, f'Wrong captcha, correct percent: {captcha_percent:.2f}%')
            print()
            driver.quit()
            sleep(sleep_times['between_calls'])
            continue

        captcha_tracker.append(1)
        captcha_percent = sum(captcha_tracker) * 100 / len(captcha_tracker)
        print(i, f'Correct captcha, correct percent: {captcha_percent:.2f}%')

        elems = driver.find_elements(By.CLASS_NAME, 'tr-1-2')
        for elem in elems:
            cat = elem.text.split('\n')[0]
            available = good_status if 'CURRENTLY NOT AVAILABLE' not in elem.text else bad_status

            if available == good_status and statuses.get(cat, bad_status) == bad_status:
                print(cat, available.upper())
                tg_bot.send_message(my_id, f'TICKETS AVAILABLE FOR CATEGORY {cat}')
            elif available == bad_status and statuses.get(cat, bad_status) == good_status:
                print(cat, available.upper())
                tg_bot.send_message(my_id, f'TICKETS ARE ALREADY NOT AVAILABLE FOR CATEGORY {cat}')
            statuses[cat] = available

        print()
        driver.quit()
        sleep(sleep_times['between_calls'])
    except KeyboardInterrupt:
        driver.quit()
        print(f'Graceful shutdown, driver closed')
        break
    except Exception as e:
        driver.quit()
        print(e)
        sleep(sleep_times['between_calls'])
        continue
