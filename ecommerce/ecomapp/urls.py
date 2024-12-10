from django.urls import path
from .views import *


urlpatterns=[


    path('register/',registerUser),
    path('index/',index),
    path('loginuser/',loginuser),
    path('userprofile/',userprofile),
    path('viewdetail/<int:id>',viewdetail),
    path('update/<int:id>',updateuser),

    path('addtocart/<int:itemid>',addtocart),
    path('cartdisplay/',CartDisplay),
    path('incdec/<int:itemid>',inc_dec),
    path('cartremove/<int:cid>',removecart),
    path('addwish/<int:pdtid>',wishlistAdd),
    path('wishlist/',displayWish),
    path('deletewish/<int:id>',removewish),
    path('viewwish/<int:pdtid>',viewwish),
    path('addAddress/',addAddress),
    path('delivery_address/',delivery_details),
    path('summary/',summary_details),
    path('create_order/',create_order),
    path('order_list/',order_view),
    path('cancelorder/<int:ordr_id>',cancel_order),
    path('pwchange/',change_pw),
    path('logout/',logout)




]