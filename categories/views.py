from django.shortcuts import render, get_object_or_404
from .models import Category, subCategory
from django.template.loader import get_template
from django.http import HttpResponse




def indexCategories (request):
	allCategory = Category.objects.all().order_by('cName')
	allSubcat = subCategory.objects.all().order_by('scName')
	

	numberOfCol = 4
	indexSize = len(allCategory)-1
	remainder = indexSize % numberOfCol
	quotient = indexSize-remainder
	looped = (quotient / numberOfCol) + 1


	context = {
		'allCategory': allCategory,
		'allSubcat': allSubcat,
		'looped': looped,
		'numberOfCol': numberOfCol,
		'size':len(allCategory,),

	
	}
	return render(request, 'categories/categoryIndex.html', context)


