from django.contrib import admin
from .models import Brand, Gender, ShoeStyle, GeneralItemDictionary, Product, Color,  ProductPhoto, StoreInventory, Size

admin.site.register(Brand)
admin.site.register(Gender)
admin.site.register(ShoeStyle)
admin.site.register(GeneralItemDictionary)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductPhoto)
admin.site.register(StoreInventory)
admin.site.register(Size)

prepopulated_fields = {'slug': ('generalItem.shoeName',), }


