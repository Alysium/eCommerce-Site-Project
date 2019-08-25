from . import views
from django.urls import path
from django.conf.urls import url

app_name = 'categories'

urlpatterns = [

	path('', views.indexCategories, name='cIndex'),




]