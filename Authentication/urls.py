from django.urls import path;
from .import views

urlpatterns = [
    path('farmerSignUp/',views.farmerSignUp,name='farmerSignUp'),
    path('farmerLogin/',views.farmerLogin,name="farmerLogin"),
    path("addProductToInventory/",views.addProductToInventory),
    path('vendorSignUp/',views.vendorSignUp,name="vendorSignUp"),
    path('vendorLogin/',views.vendorLogin,name="vendorLogin"),  
    
    
    path('tp/',views.tp,name="vendorLogin"),   
    path("phoneNumberCheck/",views.phoneNumberCheck,name="phoneNumberCheck"),
    
    
    
    
     
    path("deleteAllUsers/",views.delete),
]
