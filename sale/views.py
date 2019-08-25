from django.shortcuts import render
from categories.models import Category, subCategory

from store.models import StoreLocation, City
from products.models import GeneralItemDictionary, Product, Color, ShoeStyle, Gender, Brand, ProductPhoto, StoreInventory, Size

from functions.commonFunctions import loopCalculator


# Create your views here.


def saleItems(request, SaleCategory_cName):
    numOfCol = 4
    noResults = False

    if (SaleCategory_cName=='footwear'):
        qProducts = StoreInventory.objects.filter(sale=True).order_by("product__id","storeLocation__id")
       # qSaleDictList = StoreInventory.objects.filter(sale=True).order_by()
        qSaleDictList = qProducts
        numOfRow = loopCalculator(len(qSaleDictList), numOfCol)

        product_StoreLoc = qSaleDictList.values('product', 'storeLocation').distinct()


        #qProducts = qSaleDictList.values('storeLocation__id').annotate(productIDs=sum('id'))
    #qProducts = []
   


    

    context = {
        #Confirmed----------------------
        'allCategory': Category.objects.all().order_by('cName'),
        'saleCategory': SaleCategory_cName,

        #-------------------------------
        
        #Starting to Implement---------------
        'qProducts':qProducts,
 #       'TESTamountOfProducts': int(len(qProducts)),
  #      'TESTnumOfRow': range(int(TESTnumOfRow)),
   #     'TESTnumOfColRange': range(int(TESTnumOfCol)),
    #    'TESTnumOfCol': TESTnumOfCol,

 #       'numOfSizes': numOfSizes,
        #Temporary---------------------------

        'qSaleDictList': qSaleDictList,
        'amountOfProducts': int(len(qSaleDictList)),

        
        'numOfRow': range(int(numOfRow+1)),
        'numOfColRange': range(int(numOfCol)),
        'numOfCol': numOfCol,

        #unused---------------------------------
        'noResults': noResults,


    }
    return render(request, 'sale/saleListingIndex.html' , context)















