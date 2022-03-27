from django.contrib.auth.models import User

from Accounts.models import Account


def create_account(username, password):
    user = User(username=username, password=password)
    user.set_password(password)
    user.save()
    account = Account(user=user)
    account.save()
    assert User.objects.get(username=username).check_password(password)
    return account
