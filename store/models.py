from django.db import models
from django.utils.text import slugify
from categories.models import Category

import json
import urllib.parse
from decimal import Decimal

class City (models.Model):
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	def __str__(self):
		return str(self.city)

class Store (models.Model):
	sName = models.CharField(max_length=200)
	sCategory = models.ManyToManyField(Category)
	sLogo = models.ImageField(upload_to='storeLogos',blank=True) #need to change, set up photo directory
	slug = models.SlugField(blank=True, max_length=300)

	sLogoURL = models.CharField(max_length=1000, blank=True)

	def __str__(self):
		return str(self.id)+":"+str(self.sName)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.sName)
		super(Store,self).save(*args, **kwargs)
	

class StoreLocation (models.Model):
	parentStore =  models.ForeignKey(Store, on_delete=models.CASCADE)
	locationCity =  models.ForeignKey(City, on_delete=models.CASCADE, null=True)
	address = models.CharField (max_length = 300, blank = True)
	postalCode = models.CharField(max_length= 100)
	phoneNum = models.CharField (max_length=20, blank=True, null=True)
	email = models.EmailField(max_length=100, blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True )
	longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True,  null=True)
	
	def __str__(self):
		return "Self: " + str(self.id) + " Parent: " +str(self.parentStore) + " " + str(self.locationCity) + " " + str(self.address) 


	def save(self, *args, **kwargs):
		if not self.latitude or not self.longitude:
			self.latitude, self.longitude = self.geocode(self.address + " " + self.postalCode)
		
		super(StoreLocation, self).save()

	def geocode(self, address):
		address = urllib.parse.quote_plus(address)
		maps_api_url = "?".join([
			"http://maps.googleapis.com/maps/api/geocode/json",
			urllib.parse.urlencode({"address":address, "sensor":False})
		])
		response = urllib.request.urlopen(maps_api_url)
		data = json.loads(response.read().decode('utf8'))

		if data['status'] == 'OK':
			lat = data['results'][0]['geometry']['location']['lat']
			lng = data['results'][0]['geometry']['location']['lng']
			return Decimal(lat), Decimal(lng)