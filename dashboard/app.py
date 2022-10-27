""" The main dashboard to view the sensor """

import logging
import os
from datetime import datetime
import threading
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
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

moisture_data = []
DF = pd.DataFrame({'soil_moisture':[50],'time':[1]})

def prepare_app():
    """Start the app"""
    dashboard = Dash(__name__)

    fig = px.bar(DF, x='time', y='soil_moisture')

    dashboard.layout = html.Div(children=[
        html.H1(children='A simple chart'),
        dcc.Graph(id='soil-moisture-graph',figure=fig),
        dcc.Interval(
            id='interval-component',
            interval=2*1000, # in milliseconds
            n_intervals=0
        )
    ])
    return dashboard


def receive_events_from_iothub():
    """
    connect to and receive events from the eventhub
    """
    client = EventHubConsumerClient.from_connection_string(conn_str, consumer_group=CONSUMER_GROUP)

    logging.getLogger("azure.eventhub")
    logging.basicConfig(level=logging.INFO)

    def on_event(partition_context, event: EventData):
        """Handle messages from the event client"""
        json_body = event.body_as_json()
        if 'soil_moisture' in json_body:
            moisture = json_body['soil_moisture']
            enqueued_at = event.enqueued_time
            moisture_data.append(moisture)
            print("-" * 20)
            now = datetime.now(enqueued_at.tzinfo)
            print(f"{enqueued_at} - in past? {enqueued_at < now}")
            print(f"SOIL MOISTURE: {moisture}")
            print("-" * 20)

        partition_context.update_checkpoint(event)

    with client:
        client.receive(
            on_event=on_event,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )


def start_server():
    """Start the web app"""
    app = prepare_app()


    @app.callback(Output('soil-moisture-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
    def update_graph_live(_):
        time_values = [count for count, _ in enumerate(moisture_data)]
        data_frame = pd.DataFrame({ 'soil_moisture': moisture_data, 'time':time_values})
        fig = px.bar(data_frame,  y='soil_moisture',  x='time', barmode="group")
        return fig

    app.run_server(debug=False,host='0.0.0.0',port=5001)

if __name__ == '__main__':

    event_thread = threading.Thread(target=receive_events_from_iothub, daemon=True)
    server_thread = threading.Thread(target=start_server, daemon=True)
    event_thread.start()
    server_thread.start()

    print("Hello World")
    input()
