from django.urls import path
from .views import FileView, FileQRCode, FileLoadView

urlpatterns = [
    path('register/', FileView.as_view(), name='file'),
    path('load/', FileLoadView.as_view(), name='file-load'),
    path('qr/', FileQRCode.as_view(), name='file-qr'),
]
