from django.urls import path

from .views import FileView, FileGet, FileLoadView

urlpatterns = [
    path('register/', FileView.as_view(), name='file'),
    path('load/', FileLoadView.as_view(), name='file-load'),
    path('get/', FileGet.as_view(), name='file-get'),
]
