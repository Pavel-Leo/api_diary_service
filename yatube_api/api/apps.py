from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'


class V1Config(AppConfig):
    name = 'api.v1'


class V2Config(AppConfig):
    name = 'api.v2'
