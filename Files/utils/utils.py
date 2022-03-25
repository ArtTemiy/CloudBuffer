from CloudBuffer.settings import MEDIA_ROOT


def get_file_path(account, token):
    file_name = f'{account.user.username}__{token}'
    return f'{MEDIA_ROOT}/{file_name}'
