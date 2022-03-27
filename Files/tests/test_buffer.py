from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from CloudBuffer.tests_settings_override import overrides
from Files.models.models import File
from Tests.assertion import *
from Tests.create_testing_enviroment import create_testing_environment
from Tests.utils import create_account


@create_testing_environment
@override_settings(**overrides)
class BufferViewTest(TestCase):
    USERNAME = 'user'
    PASSWORD = 'password'

    @classmethod
    def setUpTestData(cls):
        cls.user = create_account(cls.USERNAME, cls.PASSWORD)

    def setUp(self):
        login_result = self.client.login(
            username=self.USERNAME,
            password=self.PASSWORD,
        )
        assert_t(login_result)

    def test_post_file(self):
        response = self._create_file_request()

        assert_eq(response.status_code, 200, response.json())
        assert_eq(response.json(), {
            'code': 0,
            'message': 'ok'
        })

        assert_eq(len(File.objects.filter(account=self.user, token='@')), 1)

    def test_post_text(self):
        response = self._create_text_request()

        assert_eq(response.status_code, 200)
        assert_eq(response.json(), {
            'code': 0,
            'message': 'ok'
        })

        assert_eq(len(File.objects.filter(account=self.user, token='@')), 1)

    def test_overrides(self):
        requests = [
            self._create_file_request,
            self._create_file_request,
            self._create_text_request,
            self._create_text_request,
            self._create_file_request,
        ]
        for request in requests:
            request()
            assert_eq(len(File.objects.filter(account=self.user, token='@')), 1)

    def _create_file_request(self):
        test_string = b'Hello, world!'
        file_name = 'file-name.ext'
        file = SimpleUploadedFile(file_name, test_string)

        return self.client.post(
            reverse('buffer'),
            {'file': file},
            HTTP_X_DATA_TYPE='file',
        )

    def _create_text_request(self):
        test_string = b'Hello, world!'
        file = BytesIO(test_string)

        return self.client.post(
            reverse('buffer'),
            {'file': file},
            HTTP_X_DATA_TYPE='file',
        )
