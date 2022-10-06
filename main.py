import urllib.request
import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


url = "https://reserve-prime.apple.com/AE/en_AE/reserve/A/availability?iUP=N"


def printer(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time, msg)


def foo():
    contents = urllib.request.urlopen(url).read()
    ifttt_url = "https://maker.ifttt.com/trigger/iphone_appeared/json/with/key/" + os.getenv('IFTTT_TOKEN')
    if "We’re not taking reservations to buy iPhone in the store right now." in contents.decode("utf8"):
        printer('not got it')
    else:
        printer('GOT IT')
        r = requests.post(ifttt_url, json={
            "this": 1
        })


while True:
    foo()
    time.sleep(10)

