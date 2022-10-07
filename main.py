import urllib.request
import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv
import traceback
import json

load_dotenv()

url = "https://reserve-prime.apple.com/AE/en_AE/reserve/A/availability?iUP=N"
availability_url = "https://reserve-prime.apple.com/AE/en_AE/reserve/A/availability.json"
ifttt_url = "https://maker.ifttt.com/trigger/iphone_appeared/json/with/key/" + os.getenv('IFTTT_TOKEN')


def get_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def printer(msg):
    print(get_time(), msg)


def save_to_file(text):
    time_id = get_time()
    file_path = 'logs/' + time_id + '.txt'
    with open(file_path, 'w') as f:
        f.write(text)


iphones = {
    "MQ1W3AA/A": "iPhone 14 Pro 512GB Silver",
    "MQ2G3AA/A": "iPhone 14 Pro 1TB Space Black",
    "MQAJ3AA/A": "iPhone 14 Pro Max 512GB Gold",
    "MQ0T3AA/A": "iPhone 14 Pro 256GB Space Black",
    "MQ9V3AA/A": "iPhone 14 Pro Max 256GB Silver",
    "MPXV3AA/A": "iPhone 14 Pro 128GB Space Black",
    "MQ2V3AA/A": "iPhone 14 Pro 1TB Gold",
    "MQ9W3AA/A": "iPhone 14 Pro Max 256GB Gold",
    "MQ323AA/A": "iPhone 14 Pro 1TB Deep Purple",
    "MQ2N3AA/A": "iPhone 14 Pro 1TB Silver",
    "MQ023AA/A": "iPhone 14 Pro 128GB Silver",
    "MQ9P3AA/A": "iPhone 14 Pro Max 128GB Space Black",
    "MQ293AA/A": "iPhone 14 Pro 512GB Deep Purple",
    "MQAM3AA/A": "iPhone 14 Pro Max 512GB Deep Purple",
    "MQ9U3AA/A": "iPhone 14 Pro Max 256GB Space Black",
    "MQ1F3AA/A": "iPhone 14 Pro 256GB Deep Purple",
    "MQC33AA/A": "iPhone 14 Pro Max 1TB Silver",
    "MQC53AA/A": "iPhone 14 Pro Max 1TB Deep Purple",
    "MQ9R3AA/A": "iPhone 14 Pro Max 128GB Gold",
    "MQAH3AA/A": "iPhone 14 Pro Max 512GB Silver",
    "MQC23AA/A": "iPhone 14 Pro Max 1TB Space Black",
    "MQ9X3AA/A": "iPhone 14 Pro Max 256GB Deep Purple",
    "MQ233AA/A": "iPhone 14 Pro 512GB Gold",
    "MQ0G3AA/A": "iPhone 14 Pro 128GB Deep Purple",
    "MQ083AA/A": "iPhone 14 Pro 128GB Gold",
    "MQ9Q3AA/A": "iPhone 14 Pro Max 128GB Silver",
    "MQ9T3AA/A": "iPhone 14 Pro Max 128GB Deep Purple",
    "MQAF3AA/A": "iPhone 14 Pro Max 512GB Space Black",
    "MQ103AA/A": "iPhone 14 Pro 256GB Silver",
    "MQ1M3AA/A": "iPhone 14 Pro 512GB Space Black",
    "MQC43AA/A": "iPhone 14 Pro Max 1TB Gold",
    "MQ183AA/A": "iPhone 14 Pro 256GB Gold",
}


store_names = {
    "R597": "Dubai / Dubai Mall",
    "R596": "Dubai / Mall of the Emirates",
    "R595": "Abu Dhabi / Yas Mall",
    "R706": "Abu Dhabi / Al Maryah Island",
}


def send_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())  # this sends the message


def availability_message(stores, store_code):
    message = ""
    store = stores[store_code]
    for iphone in store:
        if store[iphone]["availability"]["unlocked"]:
            message += iphones[iphone] + " in " + store_names[store_code] + "\n"
    return message


def foo():
    contents = urllib.request.urlopen(availability_url).read()
    content = contents.decode("utf8")
    save_to_file(content)

    json_obj = json.loads(content)

    store1 = availability_message(json_obj["stores"], "R597")
    store2 = availability_message(json_obj["stores"], "R596")

    store_msg = store1 + store2

    # if content.count("true") > 1:
    if len(store_msg) > 0:
        printer(store_msg)
        send_telegram(store_msg + url)
        # r = requests.post(ifttt_url, json={"msg": store_msg})
    else:
        printer('not got it')


while True:
    try:
        foo()
    except Exception as exception:
        printer("error occurred")
        traceback.print_exc()
    time.sleep(10)
