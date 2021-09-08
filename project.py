import conf
from boltiot import Sms, Bolt
import json, time

mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SSID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)

def get_sensor_value_from_pin(pin):
    try:
        response = mybolt.digitalRead(pin)
        data = json.loads(response)
        sensor_value = int(data["value"])
        if sensor_value == 1:
            return sensor_value
        return 0
    except Exception as e:
        print("Something went wrong while returning the sensor value ")
        print(e)
        return -999

while True:

    sensor_value = get_sensor_value_from_pin("0")
    print("The current sensor value is:", sensor_value)

    if sensor_value == -999:
        print("Something went wrong.....")
        time.sleep(5)
        continue

    if sensor_value == 0:
        mybolt.digitalWrite("1", "HIGH")
        mybolt.digitalWrite("2", "HIGH")
        print("Someone is at door. Please Open.")
        response = sms.send_sms("Someone is at door. Please Open:)")
        print("Status of SMS at Twilio is: " +str(response.status))
        time.sleep(5)
        mybolt.digitalWrite("1", "LOW")
        mybolt.digitalWrite("2", "LOW")
        time.sleep(5)
    elif sensor_value == 1:
        print("No motion detected")
    time.sleep(5)
