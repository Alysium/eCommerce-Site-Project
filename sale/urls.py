from . import views
from django.urls import path

app_name = 'sale'


urlpatterns = [

    path('<str:SaleCategory_cName>/', views.saleItems, name='saleProductListing'),



    

]





















