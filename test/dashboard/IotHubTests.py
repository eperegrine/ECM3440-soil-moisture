"""Unit Tests"""

import datetime
from unittest import mock, TestCase
import unittest
from dashboard.core.iothub import generate_on_event

class IotHubTests(TestCase):
    """Test the dashboard"""

    def test_dashboard_sample(self):
        """A sample test"""
        assert 1+1 == 2

    def test_on_event_save_moisture(self):
        """Check the iottub saves the moisture when events are received"""
        #Arrange
        moisture_data = { "soil_moisture": 6789 }
        data = mock.Mock()
        data.body_as_json = mock.Mock(return_value=moisture_data)
        data.enqueued_time = datetime.datetime.now()

        save_moisture = mock.Mock()
        on_event = generate_on_event(save_moisture)
        #Act
        on_event(mock.Mock(), data)
        #Assert
        save_moisture.assert_called()

if __name__ == "main":
    unittest.main()
