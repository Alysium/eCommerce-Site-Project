from django.db import models
from django.utils.text import slugify
from store.models import StoreLocation

from django.db.models import Avg

class Brand(models.Model):
    brandName = models.CharField(max_length=100)

    def __str__(self):
        return str(self.brandName)

class Gender(models.Model):
    gender = models.CharField(max_length=100)

    def __str__(self):
        return str(self.gender)

class ShoeStyle(models.Model):
    style = models.CharField(max_length=100)

    def __str__(self):
        return str(self.style)


class Color(models.Model):
    color = models.CharField(max_length=100)
    def __str__(self):
        return str(self.id) + ": " + str(self.color)    

class GeneralItemDictionary(models.Model):
    brand =  models.ForeignKey(Brand, on_delete=models.CASCADE)
    gender =  models.ForeignKey(Gender, on_delete=models.CASCADE)
    style = models.ForeignKey(ShoeStyle, on_delete=models.CASCADE)
    shoeName = models.CharField(max_length=200)
    shoeDescription = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.id) + ": " + " " + str(self.gender) + " " + str(self.brand) + " " + str(self.shoeName)

class Product(models.Model):
    generalItem = models.ForeignKey(GeneralItemDictionary, on_delete=models.CASCADE)
    color = models.ManyToManyField(Color)
    additionalName = models.CharField(max_length=100, blank=True, null=True)
    colorway = models.CharField(max_length=1000, blank=True, null=True)
    displayPic = models.ImageField(upload_to='displayPictures', blank=True)
    #Eg of colorway entry: White/Fire Red/Cement Grey/Black
    #While ManyToManyField color entry is: white, red, grey, black
    productDescription = models.CharField(max_length=1000, blank=True, null=True)
    slug = models.SlugField(blank=True, max_length=1000)

    def __str__(self):
        return str(self.id) + " | " + str(self.generalItem)+ " " + str(self.additionalName) + "| Colorway: " + str(self.colorway)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.generalItem.shoeName + "-" + self.generalItem.gender.gender)
        super(Product, self).save(*args, **kwargs)


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='generalPictures', blank=True)
    #maybe store links in db instead of straightup pictures?
    #imageName = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.id) + ": " + str(self.image) + "| " + str(self.product)

class Size(models.Model):
    size = models.FloatField()
    def __str__(self):
        return str(self.size)

class StoreInventory(models.Model):
    storeLocation = models.ForeignKey(StoreLocation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    regularPrice = models.DecimalField(decimal_places=2, max_digits=10)
    sale = models.BooleanField(default=False)
    salePrice = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)

    def __str__(self):
        return "size: " + str(self.size) + " | productId: " + str(self.product) + "|" + str(self.storeLocation)


#Alternative database option:
#class StoreInventory2 (models.Model):
#    storeLocation = models.ForeignKey(StoreLocation, on_delete=models.CASCADE)
#    product = models.ForeignKey(Product, on_delete=models.CASCADE)
#    size4 = models.IntegerField(default=0)
#    size4_5 = models.IntegerField(default=0)
#    size5 = models.IntegerField(default=0)
#    size5_5 = models.IntegerField(default=0)
#    size6 = models.IntegerField(default=0)
#    size6_5 = models.IntegerField(default=0)
#    size7 = models.IntegerField(default=0)
#    size7_5 = models.IntegerField(default=0)
#    size8 = models.IntegerField(default=0)
#   size8_5 = models.IntegerField(default=0)
#    size9 = models.IntegerField(default=0)
#    size9_5 = models.IntegerField(default=0)
#    size10 = models.IntegerField(default=0)
#    size10_5 = models.IntegerField(default=0)
#    size11 = models.IntegerField(default=0)
#    size11_5 = models.IntegerField(default=0)
#    size12 = models.IntegerField(default=0)
#    size12_5 = models.IntegerField(default=0)
#    size13 = models.IntegerField(default=0)
#    size13_5 = models.IntegerField(default=0)
#    size14 = models.IntegerField(default=0)
#    regularPrice = models.FloatField()
#    sale = models.BooleanField(default=False)
#    salesPrice = models.FloatField(blank=True)

#    def __str__(self):
#        return str(self.product) + " | " + str(self.storeLocation)

#class PriceSizeChange:
#    storeInventory = models.ForeignKey(StoreInventory2, on_delete=models.CASCADE)
#    size = models.FloatField()
#    newPrice = models.FloatField()


    
