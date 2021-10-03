from django.apps import AppConfig


class MyUsersConfig(AppConfig):
    name = 'my_users'

    def ready(self):
        from . import signals