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
python3 -m CounterFit
```

Then in counter fit you can setup the sensor

### How to build and run the dashboard container

Pre-requisite:  You need to know the name of the docker hub repo where this image should be pushed to or ask a team member for this information.  Do a ``` docker login ``` to login to docker.

To build the dashboard container, run the command below:
`docker build . -t $(REPO_NAME)/python-dashboard:latest`

To run the dashboard container, run the command below:
`docker run -p 127.0.0.1:8080:8080 python-dashboard:latest`

To push to the hub, the command is:
`docker push $(REPO_NAME)/python-dashboard:latest`
