import io
from collections import defaultdict
from time import sleep

import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import chrome_options, tg_bot, sleep_times, my_id, reader, Status, n_iterations, logger, EVENTS

captcha_tracker = []
statuses = defaultdict(dict)

tg_bot.send_message(my_id, f'Starting search!')

for i in range(n_iterations):
    for event_name, url in EVENTS:
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get(url)

            sleep(sleep_times['init'])

            try:
                elem = driver.find_element(By.CLASS_NAME, 'captcha-code')
            except Exception as e:
                logger.info(f'Event: {event_name}, iteration: {i}, couldnt find captcha element')
                driver.quit()
                logger.info(f'Sleeping for {sleep_times["between_calls"]}s before next call')
                sleep(sleep_times['between_calls'])
                continue
            image = Image.open(io.BytesIO(elem.screenshot_as_png))
            result = reader.readtext(np.array(image))
            if not result or not result[0]:
                logger.info(f'Event: {event_name}, iteration: {i}, empty captcha')
                driver.quit()
                logger.info(f'Sleeping for {sleep_times["between_calls"]}s before next cal')
                sleep(sleep_times['between_calls'])
                continue
            captcha_text = result[0][1].upper()
            logger.info(f'Event: {event_name}, iteration: {i}, captcha: {captcha_text}')

            elem_input = driver.find_element(By.CLASS_NAME, 'botdetect-input')
            elem_input.send_keys(captcha_text)
            elem_input.send_keys(Keys.ENTER)

            sleep(sleep_times['after_enter'])

            try:
                driver.find_element(By.CLASS_NAME, 'text_h3')
            except Exception as e:
                captcha_tracker.append(0)
                captcha_percent = sum(captcha_tracker) * 100 / len(captcha_tracker)
                logger.info(f'Event: {event_name}, iteration: {i}, wrong captcha, correct percent: {captcha_percent:.2f}%')
                driver.quit()
                logger.info(f'Sleeping for {sleep_times["between_calls"]}s before next call')
                sleep(sleep_times['between_calls'])
                continue

            captcha_tracker.append(1)
            captcha_percent = sum(captcha_tracker) * 100 / len(captcha_tracker)
            logger.info(f'Event: {event_name}, iteration: {i}, correct captcha, correct percent: {captcha_percent:.2f}%')

            elems = driver.find_elements(By.CLASS_NAME, 'tr-1-2')
            for elem in elems:
                cat = elem.text.split('\n')[0]
                status = Status.AVAILABLE if 'CURRENTLY NOT AVAILABLE' not in elem.text else Status.NOT_AVAILABLE

                if status == Status.AVAILABLE and statuses[url].get(cat, Status.NOT_AVAILABLE) == Status.NOT_AVAILABLE:
                    _, *num_tickets, price, _ = elem.text.split('\n')
                    num = num_tickets[-1]
                    msg = f'TICKETS AVAILABLE\nEVENT: {event_name}\nCATEGORY: {cat}\nNUM: {num}\nPRICE: {price}'
                    logger.info(f'Event: {event_name}, iteration: {i}, cat: {cat}, became available')
                    tg_bot.send_message(my_id, msg)
                elif status == Status.NOT_AVAILABLE and statuses[url].get(cat,
                                                                          Status.NOT_AVAILABLE) == Status.AVAILABLE:
                    logger.info(f'Event: {event_name}, iteration: {i}, cat: {cat}, no longer available')
                    tg_bot.send_message(my_id, f'TICKETS ARE NO LONGER AVAILABLE\nEVENT {event_name}\nCATEGORY {cat}')
                statuses[url][cat] = status

            driver.quit()
        except KeyboardInterrupt:
            driver.quit()
            logger.info(f'Graceful shutdown, driver closed')
            exit(0)
        except Exception as e:
            driver.quit()
            logger.exception(e)
            sleep(sleep_times['between_calls'])
            continue
        logger.info(f'Sleeping for {sleep_times["between_calls"]}s before next call')
        sleep(sleep_times['between_calls'])
