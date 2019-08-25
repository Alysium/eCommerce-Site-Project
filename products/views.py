from django.shortcuts import render, get_object_or_404
from categories.models import Category, subCategory
from store.models import StoreLocation, City
from .models import GeneralItemDictionary, Product, Color, ShoeStyle, Gender, Brand, ProductPhoto, StoreInventory, Size
from django.template.loader import get_template
from django.http import HttpResponse
from functions.commonFunctions import loopCalculator
from django.db.models import Q

from django.db.models import Avg
from django.db.models import Func
from django.template.loader import render_to_string


import json
from django.core.serializers.json import DjangoJSONEncoder

from django.http import JsonResponse
from django.conf import settings





def ajaxSizeSelection(request):
	Product_id = request.GET.get('productID')
	tab = request.GET.get('tab')
	storeLocationID = request.GET.get('storeLocationID')

	if (tab=='size'):
		availableInventory = StoreInventory.objects.filter(product=Product_id)
		availableSizesID = availableInventory.values_list('size', flat=True).distinct()
		qSizes = Size.objects.filter(id__in=availableSizesID).order_by('size')

	elif (tab=='storeLoc'):
		qSizes = StoreInventory.objects.filter(storeLocation__id=storeLocationID).filter(product__id=Product_id).distinct()
	
	context = {
		'qSizes':qSizes,
		'tab':tab,
	}
	return render (request, 'items/ajaxTemplates/sizeSelection.html', context)

#Ajax call for generating table displaying all store location listings and store location map
def ajaxTable(request):
	Product_id = request.GET.get('productID')
	tab = request.GET.get('tab')

	filteredCity = request.GET.get('filteredCity')

	if (tab == 'storeLoc'):
		if (filteredCity == 'none'):
			storeLocationIDs = StoreInventory.objects.filter(product_id=Product_id).filter(quantity__gte=1).values('storeLocation').distinct()
			qStoreLocationListing = StoreLocation.objects.filter(id__in=storeLocationIDs).distinct()
			qStoreLocationIDs = qStoreLocationListing.values_list('id', flat=True)
			
			qCitiesIDs = qStoreLocationListing.values_list('locationCity_id', flat=True)
			qCities = City.objects.filter(id__in=qCitiesIDs).order_by().distinct()



			qStoreInventoryListing = 'None'

	elif (tab == 'size'):
		if (filteredCity == 'none'):
			selectedSize = request.GET.get('size')
			selectedSize = float(selectedSize)

			qStoreInventoryListing = StoreInventory.objects.filter(product_id=Product_id)
			qStoreInventoryListing = qStoreInventoryListing.filter(size=selectedSize)
			qStoreLocationListing = 'None'

			qStoreLocationIDs = qStoreInventoryListing.values_list('storeLocation_id', flat=True)

			qCitiesIDs = qStoreInventoryListing.values_list('storeLocation__locationCity_id', flat=True)
			qCities = City.objects.filter(id__in=qCitiesIDs).order_by().distinct()

	context={
		'Product_id':Product_id,
		'qStoreInventoryListing':qStoreInventoryListing,
		'tab':tab,
		'qStoreLocationListing':qStoreLocationListing,
		
		'qStoreLocationIDs': list(qStoreLocationIDs),
		'qCities': qCities,
	}
	return render(request, 'items/ajaxTemplates/table.html', context)


def ajaxTableUpdate (request):
	productID = request.GET.get('productID')
	selectedCityID = request.GET.get('selectedCityID')
	tab = request.GET.get('tab')

	if (tab=='size'):
		sizeSelectedID = request.GET.get('sizeSelectedID')
		qStoreLocationListing = StoreInventory.objects.filter(product__id=productID).order_by()
		qStoreLocationListing = qStoreLocationListing.filter(size__id=sizeSelectedID)

		if (selectedCityID != 'none'):
			qStoreLocationListing = qStoreLocationListing.filter(storeLocation__locationCity__id=selectedCityID)

	elif (tab=='storeLoc'):		
		storeLocationIDs = StoreInventory.objects.filter(product_id=productID).filter(quantity__gte=1).values('storeLocation').distinct()
		qStoreLocationListing = StoreLocation.objects.filter(id__in=storeLocationIDs).distinct()
	
		if (selectedCityID != 'none'):
			qStoreLocationListing = qStoreLocationListing.filter(locationCity__id=selectedCityID)

	context = {
		'tab': tab,
		'qStoreLocationListing': qStoreLocationListing,


	}
	return render(request,  'items/ajaxTemplates/tableUpdate.html', context)


#For plotting markers onto the map displayed on the product page
def ajaxMarkersMap (request):

	tab = request.GET.get('tab')

	if (tab=='size'):
		StoreLocationIDs = request.GET.getlist('StoreLocationIDs[]')
		qStoreLocation = StoreLocation.objects.filter(id__in=StoreLocationIDs)

	elif (tab=='storeLoc'):
		storeLocTabInventoryID = request.GET.getlist('storeLocTabInventoryID[]')
		qStoreLocation = StoreLocation.objects.filter(id__in=storeLocTabInventoryID).order_by()

	
	qStoreNames = qStoreLocation.values_list('parentStore__sName', flat=True)
	qStorePics = qStoreLocation.values_list('parentStore__sLogo', flat=True)

	qStorePicsToLoc = []
	for i in qStorePics:
		qStorePicsToLoc = qStorePicsToLoc + [settings.MEDIA_URL + i]
		
	data= {
		'qStoreLocation': list(qStoreLocation.values()), #actual object of store location
		'qStoreNames': list(qStoreNames),
		'qStorePics': list(qStorePics),
		'qStorePicsToLoc': qStorePicsToLoc,
		
	}
	return JsonResponse(data)




def productPage(request, generalItem_slug, Product_id, selectedSize=0):

	allCategory = Category.objects.all().order_by('cName')
	selectedProduct = Product.objects.get(pk=Product_id)
	relatedPics = ProductPhoto.objects.filter(product_id=Product_id)

	generalItemId = selectedProduct.generalItem.id

	allColors = Product.objects.filter(generalItem_id=generalItemId)
	numOfColors = allColors.count()
	numOfPics = relatedPics.count()

	numOfColPics = 4
	numOfRow = loopCalculator(len(allColors), numOfColPics)	


	availableInventory = StoreInventory.objects.filter(product=Product_id)
	availableSizesID = availableInventory.values_list('size', flat=True).distinct()
	availableSizes = Size.objects.filter(id__in=availableSizesID).order_by('size')

	availability= 'Available'
	if not availableSizes:
		availability= 'None'

	context = {
		'allCategory': allCategory,
		'selectedProduct': selectedProduct,
		'allColors': allColors,
		'numOfColors': numOfColors,
		'relatedPics': relatedPics,
		'numOfPicsRange': range(int(numOfPics)),
		'availableSizes': availableSizes,

		'generalItem_slug': generalItem_slug,
		'Product_id': Product_id,
		'selectedSize': selectedSize,
		'numOfRow': range(int(numOfRow)),
		#'numOfRow': range(int(numOfRow+1)),
		'numOfColPicRange': range(int(numOfColPics)),
		'numOfColPic': numOfColPics,

		'availability':availability,

	}

	return render(request, 'items/footwearProductPage.html', context)
	
class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

from django.db.models import Count #------------------------------------------------------------

def ajaxProductFilter(request):

	noResults = False

	status = request.GET.get('status')
	orderValue = request.GET.get('orderValue')

	if(status == 'all'):
		qFootwear = Product.objects.all()
	else:
		qFootwear = Product.objects.all()
		genderList = request.GET.getlist('genderFilter[]')
		styleList = request.GET.getlist('styleFilter[]')
		brandList = request.GET.getlist('brandFilter[]')
		colorList = request.GET.getlist('colorFilter[]')


		if (len(genderList)!=0):
			qFootwear = qFootwear.filter(generalItem__gender__in=genderList).distinct()


		if(len(styleList)!=0):
			qFootwear = qFootwear.filter(generalItem__style__in=styleList).distinct()

		if(len(brandList)!=0):
			qFootwear = qFootwear.filter(generalItem__brand__in=brandList).distinct()

		if(len(colorList)!=0):
			qFootwear = qFootwear.filter(color__in=colorList).distinct()

	#Filter out footwear that have no stock available
	qFootwear = qFootwear.annotate(numOfInv=Count('storeinventory'))
	qFootwear = qFootwear.filter(numOfInv__gte=1)

	#Add average cost as object onto each qs entry
	qFootwear = qFootwear.distinct()
	qFootwear = qFootwear.annotate(avgCost=Avg('storeinventory__regularPrice'))

	numOfCol = 4
	numOfRow = loopCalculator(len(qFootwear), numOfCol)

	if (orderValue == 'alphabetical'):
		qFootwear = qFootwear.order_by('generalItem__shoeName', 'additionalName')
	elif (orderValue == 'priceLowToHigh'):
		qFootwear = qFootwear.order_by('avgCost')
	elif (orderValue == 'priceHighToLow'):
		qFootwear = qFootwear.order_by('-avgCost')


	if (not qFootwear):
		noResults = True

	context = {
		'qFootwear': qFootwear,
		'noResults': noResults,
		'amountOfProducts': len(qFootwear),
		'numOfRow': range(int(numOfRow+1)),
		'numOfColRange' : range(int(numOfCol)),
		'numOfCol': numOfCol,
	}
	
	html = render_to_string('items/ajaxTemplates/productListingGrid.html', context)
	return HttpResponse(html)

def indexItems(request, Category_cName, serializedForm="all"):

	#note: search bar not implemented, probably will have to implement Solr or some sort 
	#      of searching software for efficienct and appropreitely search the models' columns of
	#      general name, additional name, and colorway
	noResults = False
	allCategory = Category.objects.all().order_by('cName')


	if (Category_cName == "footwear"):
		qFootwear = Product.objects.all()
		allColors = Color.objects.all()
		allGender = Gender.objects.all()
		allBrands = Brand.objects.all()
		allShoeStyle = ShoeStyle.objects.all()


		if (serializedForm == "all"):
			qFootwear= Product.objects.all()
			numOfCol = 4
			numOfRow = loopCalculator(len(qFootwear), numOfCol)
			
			#Filter out footwear that have no stock available
			qFootwear = qFootwear.annotate(numOfInv=Count('storeinventory'))
			qFootwear = qFootwear.filter(numOfInv__gte=1)
			
			qFootwear = qFootwear.distinct()
			
			#Add average cost as object onto each qs entry
			qFootwear = qFootwear.annotate(avgCost=Avg('storeinventory__regularPrice'))

			if (not qFootwear):
				noResults = True

			context = {
				'allCategory': allCategory,
				'allColors': allColors,
				'allGender': allGender,
				'allBrands': allBrands,
				'allShoeStyle': allShoeStyle,
				'selectedCategory': Category_cName,
				'qFootwear': qFootwear,
				'amountOfProducts': len(qFootwear),
				'numOfRow': range(int(numOfRow+1)),
				'numOfColRange' : range(int(numOfCol)),
				'numOfCol': numOfCol,
				'noResults': noResults,
			}
	
		else:
			qFootwear= Product.objects.all()
			genderIDList = []
			shoeStyleIDList= []
			brandsIDList = []
			colorsIDList = []

			serializeList = serializedForm.split("&")

			for selectedSerialize in serializeList:
				serializeElements = selectedSerialize.split("=")

				if (serializeElements[0]=='gender'):
					genderIDList = genderIDList + [int(serializeElements[1])]
				elif (serializeElements[0]=='shoeStyle'):
					shoeStyleIDList = shoeStyleIDList + [int(serializeElements[1])]
				elif (serializeElements[0]=='brands'):
					brandsIDList = brandsIDList + [int(serializeElements[1])]
				elif (serializeElements[0]=='colors'):
					colorsIDList = colorsIDList + [int(serializeElements[1])]

			gendersList_json = []
			shoeStyleList_json = []
			brandsList_json = []
			colorsList_json = []
			
			if (len(genderIDList) != 0):
				qFootwear = qFootwear.filter(generalItem__gender__in=genderIDList).distinct()
				gendersList = Gender.objects.filter(id__in=genderIDList)
				gendersList = gendersList.values_list('gender', flat=True).distinct()
				gendersList_json = json.dumps(list(gendersList), cls=DjangoJSONEncoder)


			if (len(shoeStyleIDList) != 0):
				qFootwear = qFootwear.filter(generalItem__style__in=shoeStyleIDList).distinct()
				shoeStyleList = ShoeStyle.objects.filter(id__in=shoeStyleIDList)
				shoeStyleList = shoeStyleList.values_list('style', flat=True).distinct()
				shoeStyleList_json = json.dumps(list(shoeStyleList), cls=DjangoJSONEncoder)

			if (len(brandsIDList) != 0):
				qFootwear = qFootwear.filter(generalItem__brand__in=brandsIDList).distinct()
				brandsList = Brand.objects.filter(id__in=brandsIDList)
				brandsList = brandsList.values_list('brandName', flat=True).distinct()
				brandsList_json = json.dumps(list(brandsList), cls=DjangoJSONEncoder)

			if (len(colorsIDList) != 0):
				qFootwear = qFootwear.filter(color__in=colorsIDList).distinct()
				colorsList = Color.objects.filter(id__in=colorsIDList)
				colorsList = colorsList.values_list('color', flat=True).distinct()
				colorsList_json = json.dumps(list(colorsList), cls=DjangoJSONEncoder)

			numOfCol = 4
			numOfRow = loopCalculator(len(qFootwear), numOfCol)
			
			#Filter out footwear that have no stock available
			qFootwear = qFootwear.annotate(numOfInv=Count('storeinventory'))
			qFootwear = qFootwear.filter(numOfInv__gte=1)

			qFootwear = qFootwear.distinct()

			#Add average cost as object onto each qs entry			
			qFootwear = qFootwear.annotate(avgCost=Avg('storeinventory__regularPrice'))

			context = {
				'allCategory': allCategory,
				'allColors': allColors,
				'allGender': allGender,
				'allBrands': allBrands,
				'allShoeStyle': allShoeStyle,
				'selectedCategory': Category_cName,
				'qFootwear': qFootwear,
				'amountOfProducts': len(qFootwear),
				'numOfRow': range(int(numOfRow+1)),
				'numOfColRange' : range(int(numOfCol)),
				'numOfCol': numOfCol,
				'noResults': noResults,

				'gendersList_json':gendersList_json,
				'shoeStyleList_json':shoeStyleList_json,
				'brandsList_json':brandsList_json,
				'colorsList_json':colorsList_json,			
			}
		return render(request, 'items/footwearProducts.html', context)
	else:
		#temperary
		context={}
		return render(request, 'items/footwearProducts.html', context)
