from django.shortcuts import render,redirect
from django.http import HttpResponse
from Certificate.models import Login
from Certificate.forms import DocumentForm 

# Create your views here.
def base(request):
	return render(request,'CCS/base.html')
def signin(request):
	
	if request.method=="POST":
	       userid=request.POST['userid']
	       pwd=request.POST['pwd']
	       data=Login.objects.create(userid=userid,pwd=pwd)
	       return redirect('uploadhtml')
	return render(request,"Certificate/signin.html")              

        
def uploadhtml(request):
	if request.method == 'POST':
		form=DocumentForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('uploadhtml')
	else :
		form=DocumentForm()
	return render(request,'Certificate/uploadhtml.html',{'form':form})
	     		