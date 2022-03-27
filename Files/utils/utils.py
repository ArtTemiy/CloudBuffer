from django.conf import settings


def get_file_path(account, token):
    if token == '@':
        return get_buffer_file_path(account)
    else:
        return get_user_file_path(account, token)


def get_user_file_path(account, token):
    file_name = f'{account.user.username}__{token}'
    return f'{settings.MEDIA_ROOT}/{file_name}'


def get_buffer_file_path(account):
    file_name = f'{account.user.username}'
    return f'{settings.MEDIA_ROOT}/{settings.BUFFER_DIR}/{file_name}'
