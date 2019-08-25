from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from categories.models import Category, subCategory



def indexHome(request):




	context = {
		'allCategory': Category.objects.all().order_by('cName')


	}

	return render(request,'homePage/homeIndex.html', context)