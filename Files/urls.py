from django.urls import path

import Files.views.buffer_views as buffer_views
import Files.views.files_views as file_views

urlpatterns = [
    path('register/', file_views.FileView.as_view(), name='file'),
    path('load/', file_views.FileLoadView.as_view(), name='file-load'),
    path('get/', file_views.FileGet.as_view(), name='file-get'),
    path('buffer/', buffer_views.BufferView.as_view(), name='buffer'),
]
