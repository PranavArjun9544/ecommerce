from django.urls import path
from .views import *

urlpatterns=[


    path('sellerregister/',sellerReg),
    path('sellerlogin/',login_seller),
    path('sellerprof/',seller_profile),
    path('sellerindex/',seller_index),
    path('addproduct/',productadd),
    path('pdtview/',view_pdt),
    path('edit/<int:eid>',edit_pdt),
    path('delete/<int:did>',dlt_pdt)
]