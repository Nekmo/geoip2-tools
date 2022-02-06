import datetime
import os
import tarfile
import tempfile
import portalocker
from typing import Union

import geoip2.database
import requests

from geoip2_tools.exceptions import DatabaseNotExists
from geoip2_tools.lock import lock_file
from geoip2_tools.utils import extract_file_to

DATABASE_ALIASES = {
    'asn': 'GeoLite2-ASN',
    'country': 'GeoLite2-Country',
    'city': 'GeoLite2-City',
}
DEFAULT_GEOIP2_TOOLS_DIRECTORY = os.path.expanduser('~/.config/geoip2-tools/')
GEOIP2_TOOLS_DIRECTORY = os.environ.get('GEOIP2_TOOLS_DIRECTORY', DEFAULT_GEOIP2_TOOLS_DIRECTORY)
GEOIP2_DOWNLOAD_URL = 'https://download.maxmind.com/app/geoip_download'
GEOIP2_MAXMIND_LICENSE_KEY_ENVNAME = 'GEOIP2_MAXMIND_LICENSE_KEY'
DOWNLOAD_CHUNK_SIZE = 1024 * 4


class Geoip2DataBase:
    def __init__(self, edition_id: str, directory: Union[str, None] = None,
                 license_key: Union[str, None] = None):
        self.edition_id = DATABASE_ALIASES.get(edition_id, edition_id)
        self.directory = directory or GEOIP2_TOOLS_DIRECTORY
        self.license_key = license_key or os.environ.get(GEOIP2_MAXMIND_LICENSE_KEY_ENVNAME)
        self._reader = None
        self._path = None
        assert self.license_key is not None, "A MaxMind license is required."

    def exists(self):
        return os.path.lexists(self.path)

    @property
    def path(self) -> str:
        return os.path.join(self.directory, f'{self.edition_id}.mmdb')

    def download_params(self) -> dict:
        return {
            'edition_id': self.edition_id,
            'license_key': self.license_key,
            'suffix': 'tar.gz',
        }

    def download(self) -> None:
        # Lock the database file during download in case another process lands
        # here.
        with lock_file(f'{self.path}.lock') as lock:

            # We have the lock on an empty file, so let's write some data to it.
            r = requests.get(GEOIP2_DOWNLOAD_URL, params=self.download_params(), stream=True)
            os.makedirs(self.directory, exist_ok=True)

            with tempfile.NamedTemporaryFile(suffix='.tar.gz') as temp_file:
                for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        temp_file.write(chunk)
                temp_file.seek(0)

                tar = tarfile.open(mode="r:gz", fileobj=temp_file)
                member_path = next(filter(lambda x: x.endswith('.mmdb'), tar.getnames()))
                extract_file_to(tar, member_path, lock)
                tar.close()

    def updated_at(self) -> Union[None, datetime.datetime]:
        if not self.exists():
            return None
        t = os.path.getmtime(self.path)
        return datetime.datetime.fromtimestamp(t)

    @property
    def reader(self) -> geoip2.database.Reader:
        if not self._reader and not self.exists():
            raise DatabaseNotExists(f'Database {self.edition_id} not exists in {self.path}.')
        if not self._reader:
            self._reader = geoip2.database.Reader(self.path)
        return self._reader
