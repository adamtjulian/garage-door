from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time as timer
import json
import os.path
import requests
from datetime import datetime, time

def get_lcd(backlight_on, clear_screen=True):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=20, rows=4, dotsize=8,
              charmap='A00',
              auto_linebreaks=True,
              #backlight_enabled=backlight_on)
              backlight_enabled=True)
    if clear_screen:
        lcd.clear()
    lcd.write_string("********************")
    lcd.cursor_pos = (1, 0)
    lcd.cursor_pos = (3, 0)
    lcd.write_string("********************")
    return lcd

def check_if_dim(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.utcnow().time()
    print(begin_time)
    print(end_time)
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time

lcd = get_lcd(True)


while True:
    resp = None
    is_exception = False
    try:
        print("Getting status")
        resp = requests.get("http://garage.home/status.json", timeout=5)
        print("Status success")
    except Exception as e:
        print("Exception: " + str(e))
        is_exception = True
    #  if the garage is closed and it is past 10PM but before 6AM, turn of lcd
    # if the garage is open, turn on lcd
    #if the garage is
    print("Status: " + str(resp))
    print("Is Exception: " + str(is_exception))
    if is_exception is False and resp.status_code == 200:
        resp = json.loads(resp.text)
        print("Current Garage Status: " + resp["open-close"])
        if resp["open-close"] == "closed" and check_if_dim(time(22, 00), time(6, 00)):
            lcd = get_lcd(False, False)
        elif resp["open-close"] == "open" and check_if_dim(time(22, 00), time(6, 00)):
            lcd = get_lcd(True, False)

        if resp["open-close"] == "closed":
            lcd.cursor_pos = (1, 0)
            lcd.write_string("Garage Closed")
        elif resp["open-close"] == "open":
            lcd.cursor_pos = (1, 0)
            lcd.write_string("Garage Open")
        else:
            print(resp["open-close"])
            lcd.cursor_pos = (1, 0)
            lcd.write_string("Garage Error")
    else:
        lcd = get_lcd(True, False)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("HTTP Error")
    timer.sleep(5)
exit(0)

