from . import views
from django.urls import path

app_name = 'products'

urlpatterns = [

    path('<slug:generalItem_slug>/product-id=<int:Product_id>/', views.productPage, name='productPage'),    

    path('productFilter/', views.ajaxProductFilter, name='productFilter'),

    path('table/filterTableAjax/', views.ajaxTable, name='tableDisplay'),
    path('table/UPDATEfilterTableAjax/', views.ajaxTableUpdate, name='tableDisplayUpdate'),
    path('selection/filterSizeAjax/', views.ajaxSizeSelection, name='sizeDisplay'),
    path('map/markersMapAjax/', views.ajaxMarkersMap, name='mapMarker'),


    path('<str:Category_cName>/', views.indexItems, name='productListing'),


    #for trying to update URL wihout refreshing experiments
    path('<str:Category_cName>/<str:serializedForm>', views.indexItems, name='productListingSerialize'),


    
    
    


    
    #removed URL below, saved it for future reference
    #path('<slug:generalItem_slug>/product-id=<int:Product_id>/<slug:selectedStore_slug>/store-id=<int:selectedStoreId>/', views.productPage, name='productPageStoreSelected'),
    #path('sizeSubmit/', views.sizeSubmit, name="sizeSubmit"), (this url was used for ajax form submission)
]
















