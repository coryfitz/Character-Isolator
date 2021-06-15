from django.urls import path
from . import views

app_name = 'converter'
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('filter', views.filter, name='filter'),
    path('file_upload', views.file_upload, name='file_upload'),
]
