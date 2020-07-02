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

from programytest.client import TestClient


class SraiTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(SraiTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])

    def load_configuration(self, arguments, subs=None):
        super(SraiTestClient, self).load_configuration(arguments, subs)
        bot_config = self._configuration.client_configuration.configurations[0]
        brain_config = bot_config.configurations[0]
        brain_config.dynamics.dynamic_sets["number"] = "programy.dynamic.sets.numeric.IsNumeric"


class SraiAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SraiTestClient()
        self._client_context = client.create_client_context("testid")

    def test_srai_response(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE.')

    def test_single_srai(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HI")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE.')

    def test_multiple_srai(self):
        response = self._client_context.bot.ask_question(self._client_context, "MORNING")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'WELL HI THERE AND HI THERE AGAIN.')

    def test_nested_srai(self):
        response = self._client_context.bot.ask_question(self._client_context, "FAREWELL")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SEEYA MATE.')

    def test_predicate_set_srai(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST PREDICATE SET")
        self.assertIsNotNone(response)
        self.assertEqual('Global1 set to Value1 and Local1 set to unknown and Local2 set to Value3.', response)

    def test_srai_with_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST MULTI SRAI KEITH STERLING")
        self.assertIsNotNone(response)
        self.assertEqual('TEST1 KEITH TEST1 TEST2 STERLING TEST2.', response)

    def test_srai_with_included_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST INCLUDED SRAI KEITH STERLING")
        self.assertIsNotNone(response)
        self.assertEqual('TEST1 KEITH TEST2 STERLING TEST2 TEST1.', response)

    def test_xlength_xadd_0_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "XADD 0 XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('1.', response)

    def test_xlength_xadd_1_1(self):
        response = self._client_context.bot.ask_question(self._client_context, "XADD 1 XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('2.', response)

    def test_length_no_string(self):
        response = self._client_context.bot.ask_question(self._client_context, "XLENGTH")
        self.assertIsNotNone(response)
        self.assertEqual('0.', response)

    def test_xxlength_1char_string(self):
        response = self._client_context.bot.ask_question(self._client_context, "XXLENGTH X XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('1.', response)

    def test_xxlength_3char_string(self):
        response = self._client_context.bot.ask_question(self._client_context, "XXLENGTH X Y Z XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('3.', response)
