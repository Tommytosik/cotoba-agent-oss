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
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

from programy.mappings.base import PersonalPronounCollection
from programy.storage.factory import StorageFactory


class BasePersonCollection(PersonalPronounCollection):

    def __init__(self, errors_dict=None):
        PersonalPronounCollection.__init__(self, errors_dict)

    def person(self, person):
        if self.has_keyVal(person):
            return self.value(person)
        return None

    def personalise_string(self, tokenizer, string):
        return self.replace_by_words(tokenizer, string)

    def get_storage_name(self):
        raise NotImplementedError()

    def get_lookups_store(self, lookups_engine):
        raise NotImplementedError()

    def load(self, storage_factory):
        if storage_factory.entity_storage_engine_available(self.get_storage_name()) is True:
            lookups_engine = storage_factory.entity_storage_engine(self.get_storage_name())
            if lookups_engine:
                try:
                    lookups_store = self.get_lookups_store(lookups_engine)
                    lookups_store.load_all(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load lookups from storage", e)

    def reload(self, storage_factory):
        self.load(storage_factory)


class PersonCollection(BasePersonCollection):

    def __init__(self, errors_dict=None):
        if errors_dict is None:
            self._errors = None
        else:
            errors_dict['persons'] = []
            self._errors = errors_dict['persons']
        BasePersonCollection.__init__(self, self._errors)

    def get_storage_name(self):
        return StorageFactory.PERSON

    def get_lookups_store(self, lookups_engine):
        return lookups_engine.person_store()


class Person2Collection(BasePersonCollection):

    def __init__(self, errors_dict=None):
        if errors_dict is None:
            self._errors = None
        else:
            errors_dict['person2s'] = []
            self._errors = errors_dict['person2s']
        BasePersonCollection.__init__(self, self._errors)

    def get_storage_name(self):
        return StorageFactory.PERSON2

    def get_lookups_store(self, lookups_engine):
        return lookups_engine.person2_store()
