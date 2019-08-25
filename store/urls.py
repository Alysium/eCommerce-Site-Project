from django.urls import path
from . import views


app_name = 'store'


urlpatterns = [

	path('map/filterMapAjax/', views.filterMapAjax, name='ajaxMapFilter'),
	path('map/ajaxStoreCheckboxFilter/', views.filterStoreCheckboxAjax, name='ajaxStoreCheckboxFilter'),
	path('map/ajaxMarkerIconGenerate/', views.MarkerIconGenerateAjax, name='ajaxMarkerIconGenerate'),
	path('map/ajaxStoreSearch/', views.StoreSearchAjax, name='StoreSearchAjax'),

	path('list/', views.indexStore, name='sIndex'),
	path('map/', views.indexStoreMap, name='map'),
	path('<slug:store_Slug>/store-id=<int:store_Id>/', views.storePage , name='storePage'),

]