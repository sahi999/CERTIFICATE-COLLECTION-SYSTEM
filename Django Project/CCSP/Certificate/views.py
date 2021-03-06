from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from Certificate.models import FacLogin,Document
from Certificate.forms import *
import csv
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.http import require_http_methods
# Create your views here.
def base(request):
	return render(request,'Certificate/base.html')

def student_signup(request):
	if request.method=='POST':
		form = student_signup_form(request.POST)
		if form.is_valid():
			print("valid")
			user=form.save()
			return redirect('facdata')
	else:
		form=student_signup_form()
	return render(request,"Certificate/student_signup.html",{'form':form})
def signin(request):
	if request.method=="POST":
	       username=request.POST['username']
	       password=request.POST['password']
	       user = authenticate(username=username,password=password)
	       if user is not None :
	       	 login(request,user)
	       	 return redirect('student_dashboard')
	       else :
	       	return redirect('loginerror')

	return render(request,"Certificate/signin.html")  


@login_required(login_url="/signin")
def uploadhtml(request):
	if request.method == 'POST':
		form=DocumentForm(request.POST,request.FILES)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.userid=request.user
			instance.save()
			return redirect('showdocument')
	else :
		form=DocumentForm()
	return render(request,'Certificate/uploadhtml.html',{'form':form})

def exportcsv(request):
	details=Login.objects.all()
	response=HttpResponse('text/csv')
	response['Content-Disposition']='attachment;filename=login.csv'
	writer=csv.writer(response)
	writer.writerow(['userid','pwd'])
	fields=details.values_list('userid','pwd')
	for i in fields:
		writer.writerow(i)
	return response	
def showlogin(request):
	logins=User.objects.all()
	return render(request,"Certificate/showlogin.html",{'login':logins})
#@login_required("/signin")
def showdocument(request):
	try :
		docs=Document.objects.filter(userid=request.user) 
		return render(request,"Certificate/showdocument.html",{'document':docs})
	except:
		return redirect('student_dashboard')
def loginerror(request):
	return render(request,"Certificate/loginerror.html")
def facerror(request):
	return render(request,"Certificate/facerror.html")
def faclogin(request):
	if request.method=="POST":
		userid=request.POST['userid']
		pwd=request.POST['pwd']
		try:
			fac=Faculty.objects.get(name=userid)
			if fac.name==userid:
				user = authenticate(username=userid,password=pwd)
				if user is not None :
					login(request,user)
					return redirect('facdata')
				else :
					return redirect('facerror')
		except :
			return redirect('facerror')
	return render(request,"Certificate/faclogin.html")
def base1(request):
	return render(request,"Certificate/base1.html")

@login_required(login_url="/faclogin")
def facdata(request):
	try:
		if request.method=="POST":
			username=request.POST['username']
			ds=User.objects.get(username=username,)
			docs=Document.objects.filter(userid=ds.id)
			return render(request,"CCS/facdata.html",{'document':docs})
	except :
		messages.info(request,"Incorrect username")
		return redirect('facdata')
	return render(request,"Certificate/facdata.html")

def fac_data_fail(request):
	return render(request,"Certificate/fac_data_fail.html")
def student_dashboard(request):
	return render(request,"Certificate/student_dashboard.html")
#@login_required("/signin")
def user_logout(request):
	logout(request)
	messages.info(request, 'Logout Successfull!')
	return redirect('base')