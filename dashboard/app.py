""" The main dashboard to view the sensor """

import logging
import os
from datetime import datetime
from dash import Dash, html, dcc
from azure.eventhub import EventHubConsumerClient, EventData
from dotenv import load_dotenv
import plotly.express as px
import pandas as pd

load_dotenv()

HUB_NAME="ecm3440-egp-hub"
CONSUMER_GROUP="$Default"
IOT_HUB_EVENT_ENDPOINT="sb://iothub-ns-ecm3440-eg-21754765-c77f1ada98.servicebus.windows.net/"
DEVICE_ID="soil-moisture-sensor"
SAS_KEY=os.getenv("SAS_KEY")

conn_str = f"Endpoint={IOT_HUB_EVENT_ENDPOINT}/;" + \
f"EntityPath={HUB_NAME};" + \
f"SharedAccessKeyName=service;SharedAccessKey={SAS_KEY}"

def prepare_app():
    """Start the app"""
    dashboard = Dash(__name__)

    data_frame = pd.DataFrame({'soil_moisture':[12.0, 14.6, 13.2, 14.4],'time':[0,1,2,3]})

    fig = px.bar(data_frame, x='time', y='soil_moisture')

    dashboard.layout = html.Div(children=[
        html.H1(children='A simple chart'),
        dcc.Graph(id='soil-moisture-graph',figure=fig)
    ])
    return dashboard

if __name__ == '__main__':
    app = prepare_app()

    #app.run_server(debug=False,host='0.0.0.0',port=5001)

    client = EventHubConsumerClient.from_connection_string(conn_str, consumer_group=CONSUMER_GROUP)

    logger = logging.getLogger("azure.eventhub")
    logging.basicConfig(level=logging.INFO)

    def on_event(partition_context, event: EventData):
        """Handle messages from the event client"""
        json_body = event.body_as_json()
        if 'soil_moisture' in json_body:
            print("-" * 20)
            now = datetime.now(event.enqueued_time.tzinfo)
            print(f"{event.enqueued_time} - in past? {event.enqueued_time < now}")
            print(f"SOIL MOISTURE: {json_body['soil_moisture']}")
            print("-" * 20)

        partition_context.update_checkpoint(event)

    with client:
        client.receive(
            on_event=on_event,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )

    print("Hello World")
