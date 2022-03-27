import os

from CloudBuffer.settings import MEDIA_ROOT, BUFFER_DIR
from CloudBuffer.tests_settings_override import overrides


def create_testing_environment(obj):
    _create_testing_environment()
    return obj


def _create_testing_environment():
    os.makedirs(overrides.get('MEDIA_ROOT', MEDIA_ROOT), exist_ok=True)
    os.makedirs(
        f"{overrides.get('MEDIA_ROOT', MEDIA_ROOT)}/{overrides.get('BUFFER_DIR', BUFFER_DIR)}",
        exist_ok=True
    )
