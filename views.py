from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def signinpage(request):
	return render(request,'signin.html')
