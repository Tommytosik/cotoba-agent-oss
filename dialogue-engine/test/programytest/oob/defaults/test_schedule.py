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
import unittest.mock

from programy.oob.defaults.schedule import ScheduleOutOfBandProcessor
import xml.etree.ElementTree as ET

from programytest.client import TestClient


class ScheduleOutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def test_processor_xml_parsing(self):
        oob_processor = ScheduleOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = []
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = []
        oob.append(unittest.mock.Mock())
        oob[0].tag = "title"
        oob[0].text = "Lets meet!"
        oob.append(unittest.mock.Mock())
        oob[1].tag = "description"
        oob[1].text = "Are you free, my patio needs work"

        self.assertTrue(oob_processor.parse_oob_xml(oob))

    def test_processor(self):
        oob_processor = ScheduleOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<schedule><title>Lets meet!</title><description>How about a meeting</description></schedule>")
        self.assertEqual("SCHEDULE", oob_processor.process_out_of_bounds(self._client_context, oob_content))
