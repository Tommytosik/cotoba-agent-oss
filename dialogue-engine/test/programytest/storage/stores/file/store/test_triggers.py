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
import os.path
import shutil

from programy.storage.stores.file.store.triggers import FileTriggersStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.triggers.manager import TriggerManager
from programy.triggers.config import TriggerConfiguration


class FileTriggersStoreTests(unittest.TestCase):

    def setUp(self):
        self._tmpdir = os.path.dirname(__file__) + os.sep + "triggers"
        self._tmpfile = self._tmpdir + os.sep + "triggers.txt"

    def tearDown(self):
        if os.path.exists(self._tmpdir):
            shutil.rmtree(self._tmpdir)
        self.assertFalse(os.path.exists(self._tmpdir))

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTriggersStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_triggers(self):
        config = FileStorageConfiguration()
        config._triggers_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "triggers" + os.sep + "triggers.txt",
                                                          format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTriggersStore(engine)

        trigger_config = TriggerConfiguration()
        trigger_config._manager = TriggerConfiguration.LOCAL_MANAGER

        mgr = TriggerManager.load_trigger_manager(trigger_config)
        store.load(mgr)

        self.assertTrue(mgr.has_trigger_event("TRIGGER1"))
        self.assertTrue(mgr.has_trigger_event("TRIGGER2"))
        self.assertTrue(mgr.has_trigger_event("TRIGGER3"))
        self.assertFalse(mgr.has_trigger_event("TRIGGER4"))
