from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.conf import settings
import stripe
from django.core.mail import send_mail
from datetime import datetime,timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags




# Create your views here.



def index(request):
    return render(request,template_name='index.html')


def registerUser(request):
    if(request.method=='POST'):
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        propic=request.FILES.get('propic')
        gender=request.POST.get('gender')
        password=request.POST.get('password')
        conpassword=request.POST.get('conpassword')
        if(password==conpassword):
            data=UserRegister(name=name,email=email,phone=phone,propic=propic,gender=gender,password=password)
            data.save()
            return redirect(loginuser)
        else:
            return HttpResponse('registration failed check password')
    return render(request,template_name='registration.html')


def loginuser(request):
    if(request.method=='POST'):
        email=request.POST.get('email')
        password=request.POST.get('password')
        data=UserRegister.objects.all()
        for i in data:
            if(i.email==email and i.password==password):
                request.session['userid']=i.id   #stored login id in session
                return redirect(userprofile)
        else:
            return HttpResponse('login failed')
    return render(request,template_name='userlogin.html')

def userprofile(request):
    try:
     id1=request.session['userid']  #session called here
     data=UserRegister.objects.get(id=id1)

     category=request.GET.get('category','all')  #get selected category , if there is no category selected all option will work
     if(category == 'all'):
         db = addProduct.objects.all() #all category fetches
     else:
         db = addProduct.objects.filter(category=category) #filter by category
     for item in db:
         item.pdtsize = item.pdtsize.split(',')
     return render(request,template_name='userprofile.html',context={'data':data,'db':db})
    except:
        return redirect('loginuser')


def header(request):
    usid=request.session['userid']
    data=UserRegister.objects.get(id=usid)
    return render(request,template_name='header.html',context={'data':data})

def viewdetail(request,id):
    data=UserRegister.objects.get(id=id)
    return render(request,template_name='view_det.html',context={'data':data})


def updateuser(request,id):
    updt=UserRegister.objects.get(id=id)
    if(request.method=='POST'):
        updt.name=request.POST.get('name')
        updt.email=request.POST.get('email')
        updt.phone=request.POST.get('phone')
        updt.gender=request.POST.get('gender')
        if(request.FILES.get('propic')==None):
            updt.save()
        else:
            updt.propic=request.FILES.get('propic')
        updt.save()
        return redirect(userprofile)
    return render(request,template_name='user_update.html',context={'data':updt})




def itemdisplay(request):
    db=addProduct.objects.all()   #[(shirt,shirt.jpg,100,[s,m,l]),(shirt,shirt.jpg,100,[s,m,l])] this done on userprofile function
    #preprocessing
    for item in db:
        item.pdtsize=item.pdtsize.split(',')



def addtocart(request,itemid):
    item=addProduct.objects.get(id=itemid)  #to fetch the details of item with particular id
    cart=CartItem.objects.all()
    size=''
    if(request.method=='GET'):
        size=request.GET.get('size')
    for i in cart:
        if(i.item.id==itemid and i.selected_size==size and i.userid==request.session['userid']):
            i.quantity+=1
            i.save()
            return redirect(CartDisplay)
    else:
        db=CartItem(userid=request.session['userid'],item=item,selected_size=size)
        db.save()
        return redirect(CartDisplay)


def CartDisplay(request):
    userid=request.session['userid']
    db=CartItem.objects.filter(userid=userid)
    total=0
    count=0
    for i in db:
        i.item.pdtprice*=i.quantity
        total+=i.item.pdtprice
        count+=1
    return render(request,template_name='display_cart.html',context={'data':db,'total':total,'count':count})


def inc_dec(request,itemid):
    db=CartItem.objects.get(id=itemid)
    action=request.GET.get('action')
    if(action == 'increment'):
        db.quantity+=1
        db.save()
    elif(action == 'decrement' and db.quantity>0):
        db.quantity-=1
        db.save()
    return redirect(CartDisplay)

def removecart(request,cid):
    citem=CartItem.objects.get(id=cid)
    citem.delete()
    return redirect(CartDisplay)


def wishlistAdd(request,pdtid):
    product=addProduct.objects.get(id=pdtid)
    wish=AddWishlist.objects.all()
    for i in wish:
        if(i.product.id==product and i.userid==request.session['userid']):
            i.save()
            return HttpResponse('product already in wishlist')
    else:
        db=AddWishlist(userid=request.session['userid'],product=product)
        db.save()
        return redirect(userprofile)

def displayWish(request):
    userid=request.session['userid']
    data=AddWishlist.objects.filter(userid=userid)
    return render(request,template_name='wishlist.html',context={'data':data})


def removewish(request,id):
    dltid=AddWishlist.objects.get(id=id)
    dltid.delete()
    return redirect(displayWish)

def viewwish(request,pdtid):
    item=addProduct.objects.get(id=pdtid)
    wish=AddWishlist.objects.all()
    for i in wish:
        if(i.product.id==item):
            return render(request,template_name='wish_detail.html',context={'data':i})


def addAddress(request):
    userid=request.session['userid']
    userdata=UserRegister.objects.get(id=userid)
    if(request.method=='POST'):
        address1=request.POST.get('address1')
        address2=request.POST.get('address2')
        pincode=request.POST.get('pincode')
        city=request.POST.get('city')
        state=request.POST.get('state')
        cname = request.POST.get('cname')
        cnumber = request.POST.get('cnumber')
        data=Addressdetails(userdetail=userdata,address_line1=address1,address_line2=address2,pincode=pincode,city=city,state=state,contact_name=cname,contact_number=cnumber)
        data.save()
        return redirect(delivery_details)
    return render(request,template_name='add_address.html',context={'data':userdata})


def delivery_details(request):
    userid=request.session['userid']
    data=Addressdetails.objects.filter(userdetail__id=userid)
    return render(request,template_name='delivery_address.html',context={'data':data})

def summary_details(request):
    userid=request.session['userid']
    address_id=request.GET.get('address')
    address=Addressdetails.objects.get(id=address_id)
    cart=CartItem.objects.filter(userid=userid)
    key=settings.STRIPE_PUBLISHABLE_KEY
    total=0
    striptotal=0
    for i in cart:
        total+=i.item.pdtprice
        striptotal=total*100
    return render(request,template_name='summary_page.html',context={'address':address,'cart':cart,'total':total,'paytotal':striptotal,'key':key})


def create_order(request):                                    #after payment its work
    if(request.method == 'POST'):
        order_items=[]
        total_price=0
        userid=request.session['userid']                      #userid calling
        user=UserRegister.objects.get(id=userid)              #fetch user details using userid session
        address_id=request.POST.get('address_id')             #hidden field address id
        address=Addressdetails.objects.get(id=address_id)     #fetch the particular address using addess id
        cart=CartItem.objects.filter(userid=userid)
        order=Order.objects.create(userdetails=user,address=address)              #create is used to create a new instance of a model and save it to the data base
        #process each item in the cart
        for i in cart:
            OrderItem.objects.create(
                order=order,
                order_pic=i.item.pdtimage,
                pro_name=i.item.pdtname,
                quantity=i.quantity,
                price=i.item.pdtprice
            )
             #for email
            total_price += i.item.pdtprice*i.quantity
            order_items.append({
                'product':i.item.pdtname,
                'quantity':i.quantity,
                'price':i.item.pdtprice * i.quantity
            })
        expected_delivery_date=datetime.now() + timedelta(days=7)

        #construct email content
        subject='Order Confirmation'

        html_message=render_to_string(template_name='order_conf_email.html',  context={
            'order_items':order_items,
            'total_price':total_price,
            'expected_delivery_date':expected_delivery_date.strftime('%y-%m-%d')
        })
        plain_message=strip_tags(html_message)
        from_email='pranavka007@gmail.com'
        to_email=[user.email]

        #send email
        send_mail(subject,plain_message,from_email,to_email,html_message=html_message)

        cart.delete()
        return HttpResponse('Order created successfully')



def order_view(request):
    userid=request.session['userid']
    order=OrderItem.objects.filter(order__userdetails__id=userid).order_by('order__ordered_date')
    return render(request,template_name='order_list.html',context={'order':order})



def cancel_order(request,ordr_id):
    order_id=OrderItem.objects.get(id=ordr_id)
    order_id.order_status=False
    order_id.save()

    subject="your order cancelled"
    userid=request.session['userid']
    user=UserRegister.objects.get(id=userid)

    html_message=render_to_string(template_name='cancel_order.html',context={
        'item':order_id.pro_name,
        'price':order_id.price
    })
    plain_message=strip_tags(html_message)
    from_email='pranavka007@gmail.com'
    to_email=[user.email]
    send_mail(subject,plain_message,from_email,to_email,html_message=html_message)
    return HttpResponse('your item cancelled')


def change_pw(request):
    uid=request.session['userid']
    udata=UserRegister.objects.get(id=uid)
    if(request.method=='POST'):
        oldpw=request.POST.get('oldpassword')
        newpw = request.POST.get('newpassword')
        cnewpw = request.POST.get('cnewpassword')
        if(udata.password==oldpw):
            if(newpw==cnewpw):
                udata.password=request.POST.get('newpassword')
                udata.save()
                return redirect(loginuser)

            else:
                return HttpResponse('password not match')
        else:
            return HttpResponse('Enter correct password')
    return render(request,'password_update.html')

def logout(request):
    request.session.flush()
    return redirect(index)