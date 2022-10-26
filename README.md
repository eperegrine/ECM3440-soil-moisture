Sensor
======

This repo is a sensor that can send data to the IOT Hub - It connect to CounterFit and pushes that data to the specified IOT Hub

## Setup

It is worth creating a virtualenv

### Virtualenv

https://docs.python.org/3/library/venv.html

To create a venv run:
```bash
python -m venv venv
```

For windows (powershell)
```powershell
venv\Scripts\Activate.ps1
```
For Mac/Linux
```bash
source venv/bin/activate
```

### Requirements

Install dependencies by running 

```
pip install -r requirements.txt
```

### Linting

The app is linted automatically by GH actions. The linting is done by pylint and can be run with: `pylint $(git ls-files '*.py')`

### Counter Fit

The sensor extracts data from counter fit, you can start this using

```bash
counterfit --port 3000
```

Make sure you are in the virtual env and have run the pip install

Then in counter fit you can setup the sensor

### Iot Hub

To create the device in the hub run:

```
az iot hub device-identity create --device-id soil-moisture-sensor --hub-name <hub_name>
```

Or to add a new device replace `soil-moisture-sensor` with the device name

## Startup

The following will help you setup the sensor to send data to the IoT Hub and have the dashboard receive it locally

First start counterfit `counterfit --port 3000`

For the sensor to start it needs a device connection string, if you have followed the previous instructions you should have a device in the IoT hub 
called `soil-moisture-sensor`. You can get the connection string by running:

```
az iot hub device-identity connection-string show --device-id soil-moisture-sensor --output table --hub-name <hub_name>
```

You will then need to put the connection string into the environemnt variables so the sensor can use it.

For Mac:

```
export SENSOR_CONN_STR='HostName=ecm3440-egp-hub.azure-devices.net;DeviceId=soil-moisture-sensor;SharedAccessKey=bOXsIlSVcMcfmK1wLwSnV1PHdV1mcg8sA+b8iRqOdk0='
```

For Windows

> TODO

Then you can run the sensor

```
python app.py
```