from django.contrib import admin
from .models import Store, City, StoreLocation

# Register your models here.
admin.site.register(Store)
admin.site.register(City)
admin.site.register(StoreLocation)


prepopulated_fields = {'slug': ('sName',), }

