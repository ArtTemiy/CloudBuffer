from django.http.response import HttpResponseBadRequest


def assert_400(expr):
    if not expr:
        raise HttpResponseBadRequest()
