from django.shortcuts import render,redirect
from django.http import HttpResponse

from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from ecomapp.models import *


# Create your views here.
def sellerReg(request):
    if(request.method=='POST'):
        form=SellerRegistration(request.POST) #request.POST which is the method used to pass your POST data into SellerRegistration form
        if(form.is_valid()): #is_valid() -->in django is valid is method used with forms to check if the data provided meets the validation criteria
            password=form.cleaned_data.get('password')  #cleaned_data-->it is refers to the validated datas that has been submited through form the forms cleaned data attribute is populated when the datas are passes the isvalid method
            cpassword=form.cleaned_data.get('cpassword')
            if(password != cpassword):
                messages.error(request, message='passwords not match')
            else:
                user=form.save(commit=False)
                user.set_password(password)
                user.save()
                messages.success(request,message='Registration successful')
                return HttpResponse('registration completed')
    else:
        form=SellerRegistration()

    return render(request,template_name='seller_register.html',context={'form':form})


def login_seller(request):
    if(request.method == 'POST'):
        form=AuthenticationForm(request, data=request.POST)
        if(form.is_valid()):
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            #authenticate() is called it checks the provided username and password against the user
            #recod stored in the django authentication system if it is found it returns the object else it returns none
            if(user is not None):
                login(request,user) #it is used to login authenticated system
                request.session['sellerid'] = user.id
                # messages.success(request,message=f'you are now logged as {username}.')
                return redirect(seller_index)
            else:
                messages.error(request,'invalid username or password')
        else:
            messages.error(request,'invalid form')
    else:
        form=AuthenticationForm()
    return render(request,'seller_login.html',context={'form':form})

def seller_index(request):
    db=request.session['sellerid']
    return render(request,'seller_index.html',{'db':db})

def seller_profile(request):
    id=request.session['sellerid']
    s_db=User.objects.get(id=id)
    return render(request,'seller_profile.html',{'data':s_db})

def productadd(request):
    if(request.method=='POST'):
        pdtname=request.POST.get('pdtname')
        pdtprice=request.POST.get('pdtprice')
        pdtimage=request.FILES.get('pdtimage')
        pdtsize=request.POST.get('pdtsize')
        category=request.POST.get('category')
        pdtdesc=request.POST.get('pdtdesc')
        data=addProduct(pdtname=pdtname,pdtprice=pdtprice,pdtimage=pdtimage,pdtsize=pdtsize,category=category,pdtdesc=pdtdesc)
        data.save()
        return HttpResponse("product added successfully")
    return render(request,template_name='products.html')

def view_pdt(request):
    db=addProduct.objects.all()
    return render(request,'pdt_view.html',{'db':db})

def edit_pdt(request,eid):
    data=addProduct.objects.get(id=eid)
    if(request.method=='POST'):
        data.pdtname=request.POST.get('pdtname')
        data.pdtprice=request.POST.get('pdtprice')
        data.pdtsize=request.POST.get('pdtsize')
        data.category=request.POST.get('category')
        data.pdtdesc=request.POST.get('pdtdesc')
        if(request.FILES.get('pdtimage')==None):
            data.save()
        else:
            data.pdtimage=request.FILES.get('pdtimage')
        data.save()
        return redirect(view_pdt)
    return render(request,'pdt_edit.html',{'data':data})

def dlt_pdt(request,did):
    addProduct.objects.get(id=did).delete()
    return redirect(view_pdt)