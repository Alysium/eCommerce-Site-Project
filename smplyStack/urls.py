from django.contrib import admin
from django.conf.urls import include, re_path
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from authentication import views as authentication_views
urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('home.urls')),
	path('categories/', include('categories.urls')),
	path('stores/', include('store.urls')),
	path('product/', include('products.urls')),
	path('sale/', include('sale.urls')),
	path('home/', authentication_views.home, name = 'home'),
    path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path('signup/', authentication_views.signup, name='signup'),
    path('account_activation_sent/',authentication_views.account_activation_sent, \
    	name='account_activation_sent'),
    path('activate/<uidb64>/<token>',\
    	authentication_views.activate, name='activate'),


	#testing for solr search:
	path('search/', include('haystack.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
