from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin


app_name = 'converter'
urlpatterns = [
    path('', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    path('file_upload', views.file_upload, name='file_upload'),
    path('download', views.download, name='download'),
]
