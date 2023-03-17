from django.urls import path;
from .import views

urlpatterns = [
    path('farmerSignUp/',views.farmerSignUp,name='farmerSignUp'),
    path('vendorSignUp/',views.vendorSignUp,name="vendorSignUp"),
     path('farmerLogin/',views.farmerLogin,name="farmerLogin"),
    path('vendorLogin/',views.vendorLogin,name="vendorLogin"),    
    
    
    
    path("deleteAllUsers/",views.delete),
]
