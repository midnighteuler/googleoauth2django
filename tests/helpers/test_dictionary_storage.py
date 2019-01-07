# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for oauth2client.contrib.dictionary_storage"""

import unittest

from google.oauth2.credentials import Credentials
import jsonpickle

from googleoauth2django import GOOGLE_TOKEN_URI
from googleoauth2django.helpers import dictionary_storage


def _generate_credentials(scopes=None):
    return Credentials(
        token='access_tokenz',
        id_token='base64encodedjwtidtoken',
        refresh_token='refresh_tokenz',
        token_uri=GOOGLE_TOKEN_URI,
        client_id='client_idz',
        client_secret='client_secretz',
        scopes=scopes)


class TestStorage(unittest.TestCase):

    def test_locked_get_abstract(self):
        storage = dictionary_storage.Storage()
        with self.assertRaises(NotImplementedError):
            storage.locked_get()

    def test_locked_put_abstract(self):
        storage = dictionary_storage.Storage()
        credentials = object()
        with self.assertRaises(NotImplementedError):
            storage.locked_put(credentials)

    def test_locked_delete_abstract(self):
        storage = dictionary_storage.Storage()
        with self.assertRaises(NotImplementedError):
            storage.locked_delete()


class _FakeLock(object):

    _acquire_count = 0
    _release_count = 0

    def acquire(self):
        self._acquire_count += 1

    def release(self):
        self._release_count += 1


class DictionaryStorageTests(unittest.TestCase):

    def test_constructor_defaults(self):
        dictionary = {}
        key = 'test-key'
        storage = dictionary_storage.DictionaryStorage(dictionary, key)

        self.assertEqual(dictionary, storage._dictionary)
        self.assertEqual(key, storage._key)
        self.assertIsNone(storage._lock)

    def test_constructor_explicit(self):
        dictionary = {}
        key = 'test-key'
        storage = dictionary_storage.DictionaryStorage(dictionary, key)

        lock = object()
        storage = dictionary_storage.DictionaryStorage(
            dictionary, key, lock=lock)
        self.assertEqual(storage._lock, lock)

    def test_get(self):
        credentials = _generate_credentials()
        dictionary = {}
        key = 'credentials'
        storage = dictionary_storage.DictionaryStorage(dictionary, key)

        self.assertIsNone(storage.get())

        dictionary[key] = jsonpickle.encode(credentials)
        returned = storage.get()

        self.assertIsNotNone(returned)
        self.assertEqual(returned.token, credentials.token)
        self.assertEqual(returned.id_token, credentials.id_token)
        self.assertEqual(returned.refresh_token, credentials.refresh_token)
        self.assertEqual(returned.client_id, credentials.client_id)

    def test_put(self):
        credentials = _generate_credentials()
        dictionary = {}
        key = 'credentials'
        storage = dictionary_storage.DictionaryStorage(dictionary, key)

        storage.put(credentials)
        returned = storage.get()

        self.assertIn(key, dictionary)
        self.assertIsNotNone(returned)
        self.assertEqual(returned.token, credentials.token)
        self.assertEqual(returned.id_token, credentials.id_token)
        self.assertEqual(returned.refresh_token, credentials.refresh_token)
        self.assertEqual(returned.client_id, credentials.client_id)

    def test_delete(self):
        credentials = _generate_credentials()
        dictionary = {}
        key = 'credentials'
        storage = dictionary_storage.DictionaryStorage(dictionary, key)

        storage.put(credentials)

        self.assertIn(key, dictionary)

        storage.delete()

        self.assertNotIn(key, dictionary)
        self.assertIsNone(storage.get())

    def test_acquire_lock(self):
        dictionary = {}
        key = 'credentials'
        storage = dictionary_storage.DictionaryStorage(dictionary, key)
        storage._lock = lock = _FakeLock()
        self.assertEqual(lock._acquire_count, 0)
        storage.acquire_lock()
        self.assertEqual(lock._acquire_count, 1)

    def test_release_lock(self):
        dictionary = {}
        key = 'credentials'
        storage = dictionary_storage.DictionaryStorage(dictionary, key)
        storage._lock = lock = _FakeLock()
        self.assertEqual(lock._release_count, 0)
        storage.release_lock()
        self.assertEqual(lock._release_count, 1)
