from django.apps import AppConfig


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Files'
    label = 'Files'

    # TODO create and fill redis on start
