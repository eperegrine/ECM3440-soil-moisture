import os
from counterfit_connection import CounterFitConnection
import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

CounterFitConnection.init('127.0.0.1', 8080)

adc = ADC()
relay = GroveRelay(5)

conn_str = os.getenv('SENSOR_CONN_STR')

if conn_str is None:
    print("Connection string could not be found")
    exit(-1)

device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

print('Connecting')
device_client.connect()
print('Connected')


def handle_method_request(request):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)


device_client.on_method_request_received = handle_method_request

while True:
    soil_moisture = adc.read(0)
    print("Soil moisture:", soil_moisture)

    message = Message(json.dumps({
        'soil_moisture': soil_moisture
    }))
    device_client.send_message(message)

    time.sleep(10)
