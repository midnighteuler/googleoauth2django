# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the DjangoORM storage class."""

# Mock a Django environment
import unittest

from django.db import models
from google.oauth2.credentials import Credentials
import mock

from googleoauth2django import GOOGLE_TOKEN_URI
from googleoauth2django.models import CredentialsField
from googleoauth2django.storage import DjangoORMStorage


class CredentialWithSetStore(CredentialsField):
    def __init__(self):
        self.model = CredentialWithSetStore

    def set_store(self, storage):
        pass


class FakeCredentialsModel(models.Model):
    credentials = CredentialsField()


class FakeCredentialsModelMock(object):
    def __init__(self, *args, **kwargs):
        self.model = FakeCredentialsModelMock
        self.saved = False
        self.deleted = False

    credentials = CredentialWithSetStore()


class FakeCredentialsModelMockNoSet(object):
    def __init__(self, set_store=False, *args, **kwargs):
        self.model = FakeCredentialsModelMock
        self.saved = False
        self.deleted = False

    credentials = CredentialsField()


class TestDjangoStorage(unittest.TestCase):
    def setUp(self):
        access_token = 'foo'
        refresh_token = '1/0/a.df219fjls0'
        client_id = 'some_client_id'
        client_secret = 'cOuDdkfjxxnv+'

        # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.credentials.html
        self.credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=GOOGLE_TOKEN_URI,
            client_id=client_id,
            client_secret=client_secret)

        self.key_name = 'id'
        self.key_value = '1'
        self.property_name = 'credentials'

    def test_constructor(self):
        storage = DjangoORMStorage(FakeCredentialsModel, self.key_name,
                                   self.key_value, self.property_name)

        self.assertEqual(storage.model_class, FakeCredentialsModel)
        self.assertEqual(storage.key_name, self.key_name)
        self.assertEqual(storage.key_value, self.key_value)
        self.assertEqual(storage.property_name, self.property_name)

    @mock.patch('django.db.models')
    def test_locked_get(self, djangoModel):
        fake_model_with_credentials = FakeCredentialsModelMock()
        entities = [
            fake_model_with_credentials
        ]
        filter_mock = mock.Mock(return_value=entities)
        object_mock = mock.Mock()
        object_mock.filter = filter_mock
        FakeCredentialsModelMock.objects = object_mock

        storage = DjangoORMStorage(FakeCredentialsModelMock, self.key_name,
                                   self.key_value, self.property_name)
        credential = storage.locked_get()
        self.assertEqual(
            credential, fake_model_with_credentials.credentials)
        credential = storage.get()
        self.assertEqual(
            credential, fake_model_with_credentials.credentials)

    @mock.patch('django.db.models')
    def test_locked_get_no_entities(self, djangoModel):
        entities = []
        filter_mock = mock.Mock(return_value=entities)
        object_mock = mock.Mock()
        object_mock.filter = filter_mock
        FakeCredentialsModelMock.objects = object_mock

        storage = DjangoORMStorage(FakeCredentialsModelMock, self.key_name,
                                   self.key_value, self.property_name)
        credential = storage.locked_get()
        self.assertIsNone(credential)

    @mock.patch('django.db.models')
    def test_locked_get_no_set_store(self, djangoModel):
        fake_model_with_credentials = FakeCredentialsModelMockNoSet()
        entities = [
            fake_model_with_credentials
        ]
        filter_mock = mock.Mock(return_value=entities)
        object_mock = mock.Mock()
        object_mock.filter = filter_mock
        FakeCredentialsModelMockNoSet.objects = object_mock

        storage = DjangoORMStorage(FakeCredentialsModelMockNoSet,
                                   self.key_name, self.key_value,
                                   self.property_name)
        credential = storage.locked_get()
        self.assertEqual(
            credential, fake_model_with_credentials.credentials)

    @mock.patch('django.db.models')
    def test_locked_put(self, djangoModel):
        entity_mock = mock.Mock(credentials=None)
        objects = mock.Mock(
            get_or_create=mock.Mock(return_value=(entity_mock, None)))
        FakeCredentialsModelMock.objects = objects
        storage = DjangoORMStorage(FakeCredentialsModelMock, self.key_name,
                                   self.key_value, self.property_name)
        storage.locked_put(self.credentials)

    @mock.patch('django.db.models')
    def test_put(self, djangoModel):
        entity_mock = mock.Mock(credentials=None)
        objects = mock.Mock(
            get_or_create=mock.Mock(return_value=(entity_mock, None)))
        FakeCredentialsModelMock.objects = objects
        storage = DjangoORMStorage(FakeCredentialsModelMock, self.key_name,
                                   self.key_value, self.property_name)
        storage.put(self.credentials)

    @mock.patch('django.db.models')
    def test_locked_delete(self, djangoModel):
        class FakeEntities(object):
            def __init__(self):
                self.deleted = False

            def delete(self):
                self.deleted = True

        fake_entities = FakeEntities()
        entities = fake_entities

        filter_mock = mock.Mock(return_value=entities)
        object_mock = mock.Mock()
        object_mock.filter = filter_mock
        FakeCredentialsModelMock.objects = object_mock
        storage = DjangoORMStorage(FakeCredentialsModelMock, self.key_name,
                                   self.key_value, self.property_name)
        storage.locked_delete()
        self.assertTrue(fake_entities.deleted)

    @mock.patch('django.db.models')
    def test_delete(self, djangoModel):
        class FakeEntities(object):
            def __init__(self):
                self.deleted = False

            def delete(self):
                self.deleted = True

        fake_entities = FakeEntities()
        entities = fake_entities

        filter_mock = mock.Mock(return_value=entities)
        object_mock = mock.Mock()
        object_mock.filter = filter_mock
        FakeCredentialsModelMock.objects = object_mock
        storage = DjangoORMStorage(FakeCredentialsModelMock, self.key_name,
                                   self.key_value, self.property_name)
        storage.delete()
        self.assertTrue(fake_entities.deleted)
