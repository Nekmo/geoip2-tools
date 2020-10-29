import datetime
import os
from typing import Union

from geoip2_tools.database import DATABASE_ALIASES, Geoip2DataBase, GEOIP2_MAXMIND_LICENSE_KEY_ENVNAME


DEFAULT_EXPIRATION = datetime.timedelta(days=7)


class Geoip2DataBaseManager:
    def __init__(self, license_key: Union[str, None] = None,
                 directory: Union[str, None] = None,
                 expiration: Union[datetime.timedelta] = None):
        self.directory = directory
        self.license_key = license_key
        self.opened_databases = {}
        self.expiration = expiration or DEFAULT_EXPIRATION

    def is_license_key_available(self):
        return self.license_key or os.environ.get(GEOIP2_MAXMIND_LICENSE_KEY_ENVNAME)

    def open_database(self, edition_id: str):
        database = Geoip2DataBase(edition_id, self.directory, self.license_key)
        now = datetime.datetime.now()
        if not database.exists() or database.updated_at() + self.expiration < now:
            database.download()
        return database

    def __getitem__(self, edition_id):
        edition_id = DATABASE_ALIASES.get(edition_id, edition_id)
        if edition_id not in self.opened_databases:
            self.opened_databases[edition_id] = self.open_database(edition_id)
        return self.opened_databases[edition_id]
