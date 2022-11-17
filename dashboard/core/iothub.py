"""The module to retrieve data from the iothub"""

import logging
from datetime import datetime
from typing import Callable, Any
from azure.eventhub import EventHubConsumerClient, EventData

SaveMethod = Callable[[int], Any]

def generate_on_event(save_moisture: SaveMethod) -> Callable[[Any, EventData], Any]:
    """Generate a method to handle event calls"""
    def on_event(partition_context, event: EventData):
        """Handle messages from the event client"""
        json_body = event.body_as_json()
        if 'soil_moisture' in json_body:
            moisture = json_body['soil_moisture']
            enqueued_at = event.enqueued_time
            save_moisture(moisture)
            print("-" * 20)
            now = datetime.now(enqueued_at.tzinfo)
            print(f"{enqueued_at} - in past? {enqueued_at < now}")
            print(f"SOIL MOISTURE: {moisture}")
            print("-" * 20)

        partition_context.update_checkpoint(event)

    return on_event

def receive_events_from_iothub(conn_str: str, consumer_group: str, save_moisture: SaveMethod):
    """
    connect to and receive events from the eventhub
    """
    client = EventHubConsumerClient.from_connection_string(conn_str, consumer_group=consumer_group)

    logging.getLogger("azure.eventhub")
    logging.basicConfig(level=logging.INFO)

    on_event = generate_on_event(save_moisture)

    with client:
        client.receive(
            on_event=on_event,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )
