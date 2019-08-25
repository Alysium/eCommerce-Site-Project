from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from categories.models import Category, subCategory
from products.models import Product, StoreInventory
from .models import Store, StoreLocation, City
from functions.commonFunctions import loopCalculator

from django.db.models import Avg, Count




def storePage(request, store_Slug, store_Id):
	noResult = False
	saveFilter = False


	selectedStore = Store.objects.get(pk=store_Id)
	storeDepartments = selectedStore.sCategory.all()
	storeLocations = StoreLocation.objects.all().filter(parentStore_id = store_Id)

	qStoreInventory = StoreInventory.objects.filter(storeLocation__parentStore=store_Id)
	productIds = qStoreInventory.values_list('product', flat=True).distinct()
	
	qFootwear = Product.objects.filter(pk__in=set(productIds)).distinct().order_by('generalItem__shoeName', 'additionalName')

	numOfCol = 4
	numOfRow = loopCalculator(len(qFootwear), numOfCol)

	if(request.GET.get('filterBtn')):
		if (request.GET.getlist('storeLoc')!=[]):
			storeLocIDs = request.GET.getlist('storeLoc')
			availableInventory = StoreInventory.objects.filter(storeLocation__in=storeLocIDs)
			productIDs = availableInventory.values_list('product', flat=True).distinct()
			qFootwear = qFootwear.filter(id__in=productIDs)
			saveFilter= True

	if (not qFootwear):
		noResult = True

	qFootwear = qFootwear.distinct()
	


	#Filter out footwear that have no stock available
	qFootwear = qFootwear.annotate(numOfInv=Count('storeinventory'))
	qFootwear = qFootwear.filter(numOfInv__gte=1)

	#Add average cost as object onto each qs entry
	qFootwear = qFootwear.annotate(avgCost=Avg('storeinventory__regularPrice'))


	context = {
		'allCategory': Category.objects.all().order_by('cName'),
		'selectedStore': selectedStore,
		'storeDepartments': storeDepartments,
		'storeLocations': storeLocations,
		'qStoreInventory': qStoreInventory,
		'qFootwear': qFootwear, 

		'amountOfProducts': len(qFootwear),
		'numOfRow': range(int(numOfRow+1)),
		'numOfColRange': range(int(numOfCol)),
		'numOfCol': numOfCol,

		'saveFilter': saveFilter,
		'noResult': noResult,


	}
	return render(request, 'store/storePage.html', context) 

#For store listing page--------------------------------------------------------
def indexStore(request):
	saveFilter = False

	allCategory = Category.objects.all().order_by('cName')
	error = False
	noResults = False

	qStores = Store.objects.all()
	q = "Search Store..."	


	if(request.GET.get('searchBtn')):
		q = request.GET['q'] 
		if q:
			qStores = qStores.filter(sName__icontains=q).order_by("sName").distinct()
		else:
			q = "Search Store..."
			error = True
		saveFilter = False
			

	if(request.GET.get('filterBtn')):
		categoryInput = request.GET.getlist('categoryName')


		if(categoryInput):
			qStores = qStores.filter(sCategory__in=categoryInput).order_by("sName").distinct()
		saveFilter = True

	if (not qStores):
		noResults = True
		
	context = {
		'Categories': Category.objects.all(),
		'SearchTxt': q,
		'qStores': qStores,
		'error': error,
		'noResults': noResults,
		'allCategory': allCategory,
		'saveFilter': saveFilter,
	}
	return render(request, 'store/storeIndex.html', context)

# these imports are used exclusively for functions below
from django.http import JsonResponse
import json
import math

from django.conf import settings

def filterMapAjax (request):
	seeAll = request.GET.get('seeAll')
	qStoreLocation = StoreLocation.objects.all().order_by('id')
	allStore = Store.objects.all()
	qStoreListing = StoreLocation.objects.all().order_by('id')

	if (seeAll == 'false'):
		checkedRadioID = request.GET.getlist('checkedRadioID[]')
		checkedCategoryID = request.GET.getlist('checkedCategoryID[]')
		checkedStoreID = request.GET.getlist('checkedStoreID[]')

		if checkedRadioID != []:
			qStoreLocation = qStoreLocation.filter(locationCity__in=checkedRadioID)
			qStoreListing = qStoreListing.filter(locationCity__id__in=checkedRadioID) #for store filtering
		if checkedCategoryID != []:
			qStoreLocation = qStoreLocation.filter(parentStore__sCategory__in=checkedCategoryID)
			qStoreListing = qStoreListing.filter(parentStore__sCategory__in=checkedCategoryID) #for store filtering
		if checkedStoreID != []:
			qStoreLocation = qStoreLocation.filter(parentStore__id__in=checkedStoreID)

		#Calculate User Distance---------------
		distanceFilterVal = request.GET.get('distanceValue')
		if (distanceFilterVal != "all"):
			userLat = float(request.GET.get('userLat'))
			userLng = float(request.GET.get('userLng'))
			if (distanceFilterVal == "10"):
				distance = 10
			elif (distanceFilterVal == "25"):
				distance = 25
			elif(distanceFilterVal=="50"):
				distance = 50
			elif(distanceFilterVal=="100"):
				distance = 100

			latBounds = distance/110.574
			lngBounds = distance/(111.320*(math.cos(math.radians(userLat))))

			latUpperBounds = userLat + latBounds
			latLowerBounds = userLat - latBounds	
			lngUpperBounds = userLng + lngBounds
			lngLowerBounds = userLng - lngBounds

			qStoreLocation = qStoreLocation.filter(latitude__gte=latLowerBounds, latitude__lte=latUpperBounds)
			qStoreLocation = qStoreLocation.filter(longitude__gte=lngLowerBounds, longitude__lte= lngUpperBounds)
			
			qStoreListing = qStoreListing.filter(latitude__gte=latLowerBounds, latitude__lte=latUpperBounds)
			qStoreListing = qStoreListing.filter(longitude__gte=lngLowerBounds, longitude__lte= lngUpperBounds)
		#--------------------------------------

		#Used later for refreshing store filter section
		qStoreIDs = qStoreListing.values_list('parentStore_id', flat=True).order_by().distinct()

	else:	
		#Used later for refreshing store filter section
		qStoreIDs = qStoreLocation.values_list('parentStore_id', flat=True).order_by().distinct()

	qStoreNames = qStoreLocation.values_list('parentStore__sName', flat=True)
	qPhoneNum = qStoreLocation.values_list('phoneNum', flat=True)
	qStoreSlugs = qStoreLocation.values_list('parentStore__slug', flat=True)
	qStorePics = qStoreLocation.values_list('parentStore__sLogo', flat=True)
	qStoreIDsForInfoBox = qStoreLocation.values_list('parentStore__id', flat=True)


	qStorePicsToLoc = []
	for i in qStorePics:
		qStorePicsToLoc = qStorePicsToLoc + [settings.MEDIA_URL + i]
	
	qStoreNames = list(qStoreNames)
	qPhoneNum = list(qPhoneNum)
	qStoreSlugs = list(qStoreSlugs)
	qStoreIDs = list(qStoreIDs)
	qStoreIDsForInfoBox = list(qStoreIDsForInfoBox)

	data = {
		'qStoreLocation': list(qStoreLocation.values()),  
		'qStoreIDs': qStoreIDs, 
		'allStore': list(allStore.values()),  
		'qStorePicsToLoc':qStorePicsToLoc,
		'qStoreNames': qStoreNames,
		'qPhoneNum':qPhoneNum,
		'qStoreSlugs': qStoreSlugs,
		'qStoreIDsForInfoBox':qStoreIDsForInfoBox,
	}
	return JsonResponse(data)


def filterStoreCheckboxAjax (request): #update filter boxes in store checkbox filter section

	qStoreIDs = request.GET.getlist('qStoreIDs[]')
	qStoreIDsIntList = []
	
	for i in range(len(qStoreIDs)):
		qStoreIDsIntList = qStoreIDsIntList + [int(qStoreIDs[i])] 

	if len(qStoreIDsIntList) != 0:
		qStores = Store.objects.filter(id__in=qStoreIDsIntList).order_by('sName')
	else:
		qStores = "None"

	context = {
		'qStores': qStores,
		'qStoreIDsIntList':qStoreIDsIntList
	}
	return render(request, 'store/ajaxTemplates/storeCheckboxSelection.html', context)


def MarkerIconGenerateAjax(request): # generate marker icons
	qStoreLocID = request.GET.get('storeLocID')
	storeLoc = StoreLocation.objects.filter(id=qStoreLocID)
	parentStorePic = storeLoc.values_list('parentStore_sLogo', flat=True).distinct()
	context = {
		'parentStorePic': parentStorePic
	}
	return JsonResponse(context)


#------------Store Search in Map Page------------------------------------------
def StoreSearchAjax(request):

	qStoreLocation = StoreLocation.objects.all().order_by('id')

	#Get Filter Lists
	checkedRadioID = request.GET.getlist('checkedRadioID[]')
	checkedCategoryID = request.GET.getlist('checkedCategoryID[]')

	#Filter by filter city, category, store lists--------------------
	if checkedRadioID !=[]:
		qStoreLocation = qStoreLocation.filter(locationCity__id__in=checkedRadioID)
	if checkedCategoryID !=[]:
		qStoreLocation = qStoreLocation.filter(locationCity__id__in=checkedCategoryID)

	#Calculate User Distance---------------
	distanceFilterVal = request.GET.get('distanceValue')
	if (distanceFilterVal != "all"):
		userLat = float(request.GET.get('userLat'))
		userLng = float(request.GET.get('userLng'))
		if (distanceFilterVal == "10"):
			distance = 10
		elif (distanceFilterVal == "25"):
			distance = 25
		elif(distanceFilterVal=="50"):
			distance = 50
		elif(distanceFilterVal=="100"):
			distance = 100

		latBounds = distance/110.574
		lngBounds = distance/(111.320*(math.cos(math.radians(userLat))))

		latUpperBounds = userLat + latBounds
		latLowerBounds = userLat - latBounds	
		lngUpperBounds = userLng + lngBounds
		lngLowerBounds = userLng - lngBounds
		qStoreLocation = qStoreLocation.filter(latitude__gte=latLowerBounds, latitude__lte=latUpperBounds)
		qStoreLocation = qStoreLocation.filter(longitude__gte=lngLowerBounds, longitude__lte= lngUpperBounds)
	#--------------------------------------

	#Get search value
	searchValue = request.GET.get('searchValue')
	if (searchValue): #if search is not empty
		searchedStores = Store.objects.filter(sName__icontains=searchValue) #search for stores that contain search term
		searchedStoresIDs = searchedStores.values_list('id', flat=True) #generate list of Ids of stores containing search term
		storeSearch = qStoreLocation.filter(parentStore__id__in=searchedStoresIDs) #filter for the general stores that meet the search and filter criteria
		qStoreIDs = storeSearch.values_list('parentStore_id', flat=True).order_by().distinct() #generate store IDs for line above

	else: #if search is empty
		qStoreListing = StoreLocation.objects.all().order_by('id')

		#apply city and category filters for generating updating store filter section
		if checkedRadioID != []:
			qStoreListing = qStoreListing.filter(locationCity__id__in=checkedRadioID)
		if checkedCategoryID != []:
			qStoreListing = qStoreListing.filter(parentStore__sCategory__in=checkedCategoryID)

		#if distance value is actually selected to a distance
		if (distanceFilterVal != "all"):
			qStoreListing = qStoreListing.filter(latitude__gte=latLowerBounds, latitude__lte=latUpperBounds)
			qStoreListing = qStoreListing.filter(longitude__gte=lngLowerBounds, longitude__lte= lngUpperBounds)
		#generate list of store ID for store checkbox filter section
		qStoreIDs = qStoreListing.values_list('parentStore_id', flat=True).order_by().distinct()


	data = {
		'searchValue':searchValue,
		'qStoreIDs': list(qStoreIDs),
	}
	return JsonResponse(data)


#Function used to load map the first time
def indexStoreMap (request):

	saveFilter = False

	qCity = City.objects.all() #used for filtering
	qStores = Store.objects.all() #used for filtering
	qCategory = Category.objects.all() #used for filtering

	qStoreLocation = StoreLocation.objects.all() #used for plotting

	SearchTxt = "Search Store..."
	error = False

	if(request.GET.get('filterBtn')):
		
		cityList = request.GET.get('cityID')
		categoryList = request.GET.getlist('categoryID')
		storeList = request.GET.getlist('storeID')

		if (cityList):
			qStoreLocation = qStoreLocation.filter(locationCity=cityList)
		if (categoryList):
			qStoreLocation = qStoreLocation.filter(parentStore__sCategory__in=categoryList)
		if (storeList):
			qStoreLocation = qStoreLocation.filter(parentStore__in=storeList)
		saveFilter = True


	context = {
		'allCategory': Category.objects.all(),

		'qCity': qCity,
		'qStores':qStores,
		'qCategory':qCategory,
		'qStoreLocation':qStoreLocation,

		'SearchTxt': SearchTxt,
		'error':error,
		'saveFilter':saveFilter,
	}
	return render (request, 'store/storeIndexMap.html', context) 



