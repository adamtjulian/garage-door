from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time
import json
import os.path

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=20, rows=4, dotsize=8,
              charmap='A00',
              auto_linebreaks=True,
              backlight_enabled=True)
lcd.clear()
lcd.write_string("********************")
lcd.cursor_pos = (1, 0)
lcd.cursor_pos = (3, 0)
lcd.write_string("********************")



#currently this file will create a status file in the apache root which can then be consumed by the lcd util server and docker apache to display the status

last_status = "none"
g_data = dict()
try:
    with open("/var/www/html/status.json") as g_status:
        g_data = json.load(g_status)
        last_status = g_data["open-close"]
        print("Status file found")
except Exception as e:
    print(g_data)
    print("Status file missing, starting new file")
status = dict()
while True:
    try:
        input_22 = GPIO.input(22)
        if(input_22 == 0):
            print("closed")
            if last_status != "closed":
                lcd.cursor_pos = (1, 0)
                lcd.write_string("Garage Closed")
                status["open-close"] = "closed"
                status["timestamp"] = int(time.time())
                with open("/var/www/html/status.json", "w") as out:
                    json.dump(status, out)
                last_status = "closed"
        else:
            print("open")
            if last_status == "closed":
                lcd.cursor_pos = (1, 0)
                lcd.write_string("Garage Open")
                #write to file that will be served up as JSON to be consumed by LCD and Docker webserver
                if last_status != "open":
                    status["open-close"] = "open"
                    status["timestamp"] = int(time.time())
                    with open("/var/www/html/status.json", "w") as out:
                        json.dump(status, out)
                    last_status = "open"
    except Exception as e:
        print("Exception reading garage status: " + str(e))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Exception")
    time.sleep(2)

