from django.urls import path;
from .import views      

urlpatterns = [
    path('farmerSignUp/',views.farmerSignUp,name='farmerSignUp'),
    path('farmerLogin/',views.farmerLogin,name="farmerLogin"),
    path('searchProductForFarmer/',views.searchProductforFarmer),
    path("specificFarmerData/",views.specificFarmerData),
    path("addFarmerLocationDetails/",views.addFarmerLocationDetails),
    path("addProductToInventory/",views.addProductToInventory),
    path("getMyListedProductDetails/",views.getMyListedProductDetails),
    path("getMyListedProductList/",views.getMyListedProductList),
    path('vendorSignUp/',views.vendorSignUp,name="vendorSignUp"),
    path('vendorLogin/',views.vendorLogin,name="vendorLogin"),
    path("addVendorLocationDetails",views.addVendorLocationDetails),
    path("specificVendorData/",views.specificVendorData),
    path("searchProductsForVendorFilter/",views.searchProductsForVendorFilter),
    path("specificProductDetailsForVendor/",views.specificProductDetailsForVendor),
    path("inventoryProductListForVendor/",views.inventoryProductListForVendor),
    # path("specificProductDetailsForFarmers",views.sp),
    path("topfiveProductFromInventory/",views.topfiveProductFromInventory),
    path("bidOnProduct/",views.bidOnProduct),
    path("productBidList/",views.productBidList),
    
    path('insertAllProductList/',views.insertInAllProducts),
    path('deleteAllproductList/',views.deleteAllProductList),
    path("deleteSpecificUser/",views.deleteSpecificUser),
    
    
    path('tp/',views.tp,name="vendorLogin"),   
    path("phoneNumberCheck/",views.phoneNumberCheck,name="phoneNumberCheck"),
    
    
    
    
     
    path("deleteAllUsers/",views.delete),
]
