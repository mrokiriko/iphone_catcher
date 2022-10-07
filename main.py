import urllib.request
import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

# url = "https://reserve-prime.apple.com/AE/en_AE/reserve/A/availability?iUP=N"
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


def foo():
    contents = urllib.request.urlopen(availability_url).read()
    content = contents.decode("utf8")
    save_to_file(content)
    # if "We’re not taking reservations to buy iPhone in the store right now." in content:
    # if "true" in content:
    if content.count("true") > 1:
        printer('GOT IT')
        r = requests.post(ifttt_url, json={
            "this": 1
        })
    else:
        printer('not got it')


while True:
    try:
        foo()
    except Exception as exception:
        printer("error occurred")
        traceback.print_exc()
    time.sleep(10)
