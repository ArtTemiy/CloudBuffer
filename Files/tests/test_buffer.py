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
    test_string = b'Hello, world!'

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

        response = self.client.get(reverse('buffer'))
        assert_eq(response.status_code, 200)
        assert_eq(response.headers['X-Data-Type'], 'file')
        assert_eq(response.headers['Content-Disposition'], 'attachment; filename="file-name.ext"')
        assert_eq(b''.join(response.streaming_content), self.test_string)

    def test_post_text(self):
        response = self._create_text_request()

        assert_eq(response.status_code, 200)
        assert_eq(response.json(), {
            'code': 0,
            'message': 'ok'
        })

        assert_eq(len(File.objects.filter(account=self.user, token='@')), 1)

        response = self.client.get(reverse('buffer'))
        assert_eq(response.status_code, 200)
        assert_eq(response.headers['X-Data-Type'], 'text')
        assert_eq(b''.join(response.streaming_content), self.test_string)

    def test_overrides(self):
        requests = [
            (self._create_file_request, b'asd',),
            (self._create_file_request, b'123'),
            (self._create_text_request, b'qwe'),
            (self._create_text_request, b'zxc'),
            (self._create_file_request, b'mnb'),
        ]
        for request, message in requests:
            request(message)
            assert_eq(len(File.objects.filter(account=self.user, token='@')), 1)
            response = self.client.get(reverse('buffer'))
            assert_eq(response.status_code, 200)
            assert_eq(b''.join(response.streaming_content), message)

    # def test_wrong_file_format(self):
    #     file_name = ''
    #     file = SimpleUploadedFile(file_name, self._get_valid_message())
    #
    #     response = self.client.post(
    #         reverse('buffer'),
    #         {'file': file},
    #         HTTP_X_DATA_TYPE='file',
    #     )

    def test_no_file__file(self):
        response = self.client.post(
            reverse('buffer'),
            {},
            HTTP_X_DATA_TYPE='file',
        )
        assert_eq(response.status_code, 400)

    def test_no_file__text(self):
        response = self.client.post(
            reverse('buffer'),
            {},
            HTTP_X_DATA_TYPE='text',
        )
        assert_eq(response.status_code, 400)

    def _create_file_request(self, message=None):
        file_name = 'file-name.ext'
        file = SimpleUploadedFile(file_name, self._get_valid_message(message))

        return self.client.post(
            reverse('buffer'),
            {'file': file},
            HTTP_X_DATA_TYPE='file',
        )

    def _create_text_request(self, message=None):
        file = BytesIO(self._get_valid_message(message))

        return self.client.post(
            reverse('buffer'),
            {'file': file},
            HTTP_X_DATA_TYPE='text',
        )

    def _get_valid_message(self, message=None):
        if message:
            return message
        return self.test_string
