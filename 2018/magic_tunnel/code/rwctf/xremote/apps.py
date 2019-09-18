from django.apps import AppConfig
from django.db import connection


class XRemoteConfig(AppConfig):
    name = 'xremote'

    # def ready(self):
    #     connection.creation.create_test_db(keepdb=True)
