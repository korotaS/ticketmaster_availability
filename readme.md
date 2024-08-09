# Check availability of certain tickets on Ticketmaster

## Disclaimer

This project is not for abusing, DDoSing, resaling and other bad words concerning 
Tickermaster. It was made for me to save some time while I try to find tickets for 
upcoming Twenty One Pilots tour. 

The code only searches whether some category has tickets and **does not buy** those 
tickets automatically, you need to buy them manually afterwards. 

## How does it work? 
This project uses [Selenium](https://www.selenium.dev/) to enter the event webpage, 
[EasyOCR](https://github.com/JaidedAI/EasyOCR) to bypass captcha and then, only if 
some tickets are available, sends message from Telegram bot to you via 
[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). 

## Usage
In [config.py](config.py) find the `EVENTS` variable and enter events as tuples
of form (`event_name`, `event_url`); optionally change `sleep_times` and `n_iterations`.

Then you need to create a simple Telegram bot using [BotFather](https://telegram.me/BotFather), 
start the bot, paste the API token into `TG_BOT_API_TOKEN` env var and also paste your 
telegram ID into `TG_MY_ID` env var (you can find your id via [this bot](https://t.me/getmyid_bot)). 

After that you are free to start the search:
```shell
python find_available_tickets.py
```

## Prerequisites
The code can run on Linux and MacOS. 

Selenium uses Chrome to enter the webpages, so make sure that it is installed 
on your machine. 

## TODOs
- [ ] Docker version?
- [ ] Better OCR? Currently the OCR captcha accuracy is about 30%, which is OK 
by me but definitely could be better
- [x] Add prices into the notifications
