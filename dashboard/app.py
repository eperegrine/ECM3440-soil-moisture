""" The main dashboard to view the sensor """

import os
import threading
from dotenv import load_dotenv
from core.server import start_server
from core.iothub import receive_events_from_iothub

load_dotenv()

HUB_NAME="ecm3440-egp-hub"
CONSUMER_GROUP="$Default"
IOT_HUB_EVENT_ENDPOINT="sb://iothub-ns-ecm3440-eg-21754765-c77f1ada98.servicebus.windows.net/"
DEVICE_ID="soil-moisture-sensor"
SAS_KEY=os.getenv("SAS_KEY")

conn_str = f"Endpoint={IOT_HUB_EVENT_ENDPOINT}/;" + \
f"EntityPath={HUB_NAME};" + \
f"SharedAccessKeyName=service;SharedAccessKey={SAS_KEY}"

#This should be switched to a redis connection, but for simplicity a global
#variable works
moisture_data = []

if __name__ == '__main__':

    def save_moisture(moisture):
        """A method the thread can use to save a moisture update"""
        print("saving moisture")
        moisture_data.append(moisture)

    def get_moisture() -> list[int]:
        """A method the thread can use to get the moisture"""
        print("getting moisture")
        return moisture_data

    event_thread = threading.Thread(
        target=receive_events_from_iothub,
        args=[conn_str, CONSUMER_GROUP, save_moisture],
        daemon=True)
    server_thread = threading.Thread(target=start_server, args=[get_moisture], daemon=True)
    event_thread.start()
    server_thread.start()
    while True:
        pass
