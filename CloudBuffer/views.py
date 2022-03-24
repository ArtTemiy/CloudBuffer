from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET


@require_GET
def home_view(request):
    print(request.COOKIES)
    return render(request, 'site/home.html', {
        'title': 'Home',
        'username': request.user.username,
    })


@require_GET
def ping(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'message': 'Ok',
            'data': {
                'user': request.user.username,
            }
        }, status=200)
    else:
        return JsonResponse({
            'message': 'Not authorized',
            'data': {}
        }, status=403)
