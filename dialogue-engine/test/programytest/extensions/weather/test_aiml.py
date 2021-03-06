"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import unittest
import os
import json

from programy.extensions.weather.weather import WeatherExtension
from programy.utils.weather.metoffice import MetOffice
from programy.utils.geo.google import GoogleMaps

from programytest.client import TestClient


class MockGoogleMaps(GoogleMaps):

    def __init__(self, response_file):
        self._response_file = response_file

    def _get_response_as_json(self, url):
        with open(self._response_file, "r", encoding="utf-8") as response_data:
            return json.load(response_data)


class MockMetOffice(MetOffice):

    def __init__(self, response_file):
        self._response_file = response_file

    def _get_response_as_json(self):
        with open(self._response_file, "r", encoding="utf-8") as response_data:
            return json.load(response_data)

    def get_forecast_data(self, lat, lon, forecast_type):
        return self._get_response_as_json()

    def get_observation_data(self, lat, lon):
        return self._get_response_as_json()


class MockWeatherExtension(WeatherExtension):

    def get_geo_locator(self, bot):
        return MockGoogleMaps(WeathersAIMLTests.maps_file)

    def get_met_office(self, bot):
        return MockMetOffice(WeathersAIMLTests.weather_file)


class WeathersTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(WeathersTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_properties_store(os.path.dirname(__file__) + os.sep + "properties.txt")


class WeathersAIMLTests(unittest.TestCase):

    maps_file = None
    weather_file = None

    def setUp(self):
        client = WeathersTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_weather(self):
        WeathersAIMLTests.maps_file = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        WeathersAIMLTests.weather_file = os.path.dirname(__file__) + os.sep + "observation.json"
        # threehourly = os.path.dirname(__file__) + os.sep + "forecast_3hourly.json"
        # daily = os.path.dirname(__file__) + os.sep + "forecast_daily.json"

        response = self._client_context.bot.ask_question(self._client_context, "WEATHER LOCATION KY39UR WHEN TODAY")
        self.assertIsNotNone(response)
        texts = "According to the UK Met Office, this it is partly cloudy (day) , with a temperature of around 12dot3'C ," + \
            " humidty is 57.3% , with pressure at 1017mb and falling ."
        self.assertEqual(response, texts)


"""
WEATHER IN *
WEATHER LOCATION * WHEN *
FORECAST LOCATION * DAY *
FORECAST LOCATION * TIME *
WILL IT RAIN TODAY IN *
WILL IT RAIN TOMORROW IN *
"""
