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

"""Dictionary storage for OAuth2 Credentials."""

import jsonpickle


class Storage(object):
    """Base class for all Storage objects.

    Store and retrieve a single credential. This class supports locking
    such that multiple processes and threads can operate on a single
    store.
    """
    def __init__(self, lock=None):
        """Create a Storage instance.

        Args:
            lock: An optional threading.Lock-like object. Must implement at
                  least acquire() and release(). Does not need to be
                  re-entrant.
        """
        self._lock = lock

    def acquire_lock(self):
        """Acquires any lock necessary to access this Storage.

        This lock is not reentrant.
        """
        if self._lock is not None:
            self._lock.acquire()

    def release_lock(self):
        """Release the Storage lock.

        Trying to release a lock that isn't held will result in a
        RuntimeError in the case of a threading.Lock or multiprocessing.Lock.
        """
        if self._lock is not None:
            self._lock.release()

    def locked_get(self):
        """Retrieve credential.

        The Storage lock must be held when this is called.

        Returns:
            google.oauth2.credentials.Credentials
        """
        raise NotImplementedError

    def locked_put(self, credentials):
        """Write a credential.

        The Storage lock must be held when this is called.

        Args:
            credentials: Credentials, the credentials to store.
        """
        raise NotImplementedError

    def locked_delete(self):
        """Delete a credential.

        The Storage lock must be held when this is called.
        """
        raise NotImplementedError

    def get(self):
        """Retrieve credential.

        The Storage lock must *not* be held when this is called.

        Returns:
            google.oauth2.credentials.Credentials
        """
        self.acquire_lock()
        try:
            return self.locked_get()
        finally:
            self.release_lock()

    def put(self, credentials):
        """Write a credential.

        The Storage lock must be held when this is called.

        Args:
            credentials: Credentials, the credentials to store.
        """
        self.acquire_lock()
        try:
            self.locked_put(credentials)
        finally:
            self.release_lock()

    def delete(self):
        """Delete credential.

        Frees any resources associated with storing the credential.
        The Storage lock must *not* be held when this is called.

        Returns:
            None
        """
        self.acquire_lock()
        try:
            return self.locked_delete()
        finally:
            self.release_lock()


class DictionaryStorage(Storage):
    """Store and retrieve credentials to and from a dictionary-like object.

    Args:
        dictionary: A dictionary or dictionary-like object.
        key: A string or other hashable. The credentials will be stored in
             ``dictionary[key]``.
        lock: An optional threading.Lock-like object. The lock will be
              acquired before anything is written or read from the
              dictionary.
    """

    def __init__(self, dictionary, key, lock=None):
        """Construct a DictionaryStorage instance."""
        super(DictionaryStorage, self).__init__(lock=lock)
        self._dictionary = dictionary
        self._key = key

    def locked_get(self):
        """Retrieve the credentials from the dictionary, if they exist.

        Returns: A :class:`google.oauth2.credentials.Credentials` instance.
        """
        serialized = self._dictionary.get(self._key)

        if serialized is None:
            return None

        credentials = jsonpickle.decode(serialized)

        return credentials

    def locked_put(self, credentials):
        """Save the credentials to the dictionary.

        Args:
            credentials: A :class:`google.oauth2.credentials.Credentials`
                         instance.
        """
        serialized = jsonpickle.encode(credentials)
        self._dictionary[self._key] = serialized

    def locked_delete(self):
        """Remove the credentials from the dictionary, if they exist."""
        self._dictionary.pop(self._key, None)
