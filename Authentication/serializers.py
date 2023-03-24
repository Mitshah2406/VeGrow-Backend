import pprint
from rest_framework import serializers
from .models import Farmers,Vendor,userAuth,ProductInventory,AllProductList,ProductBidding,PurchaseTransactions
from math import radians, cos, sin, asin, sqrt

class farmerSerializer(serializers.ModelSerializer):
    class Meta:
    
        model=Farmers
        fields='__all__'
    def create(self, validated_data):
        user=Farmers.objects.create(id=validated_data['id'])
        
        user.fName=validated_data['fName']
        user.lName=validated_data['lName']
        if "email" in validated_data:    
         user.email=validated_data['email']
        if "phone" in validated_data: 
         user.phone=validated_data['phone']
        if "location" in validated_data:
            user.location=validated_data['location']    
        user.save()
        print(user)
        return  user 
        
class userAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model=userAuth
        fields=[
            
            'id',
            'role'
        ]    


class vendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
      
        fields="__all__"
    def create(self, validated_data):
        user=Vendor.objects.create(id=validated_data['id'])
        user.fName=validated_data['fName']
        user.lName=validated_data['lName']
      
        if "email" in validated_data:    
         user.email=validated_data['email']
        if "phone" in validated_data: 
         user.phone=validated_data['phone']
        if "location" in validated_data:
            user.location=validated_data['location']   
        user.save()
        print(user)
        return  user 
   
   
   
class AllProductListSerializer(serializers.ModelSerializer):
   class Meta:
       model=AllProductList
       fields="__all__"
 
 
class ProductBiddingSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductBidding
        fields="__all__"
 
class PurchaseTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseTransactions
        fields="__all__"       
    
 
       
class productInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductInventory
        fields="__all__"
    def create(self, validated_data):  
        product=ProductInventory.objects.create(farmerId=validated_data['farmerId'],productId=validated_data["productId"],initialBidPrice=validated_data['initialBidPrice'])
        product.productName=validated_data['productName']
        product.currentBidPrice=validated_data['initialBidPrice']
        product.productExpiryDate=validated_data['productExpiryDate']
        product.productUnit=validated_data['productUnit']
        product.productQuantity=validated_data['productQuantity']
        product.farmerLocation=validated_data['farmerLocation']
        product.productQuantityLeftInInventory=validated_data['productQuantity']
        if 'productDescription' in validated_data:
            product.productDescription=validated_data['productDescription']
        if 'productImages' in validated_data:
            product.productImages=validated_data['productImages']
        product.save()        
        
        return product
   
    def haversine(lon1, lat1, lon2, lat2):
   

     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
     dlon = lon2 - lon1 
     dlat = lat2 - lat1 
     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
     c = 2 * asin(sqrt(a)) 
     r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
     return c * r
    
    def distanceCalculating(self,productList,vendorLocation):

        for y,x in enumerate(productList):
              x=dict(x)
            
              distance=self.haversine(x["farmerLocation"]['lon'],x["farmerLocation"]['lat'],vendorLocation['lon'],vendorLocation['lat'])
             
              productList[y]['distanceFromVendor']=distance
              del productList[y]['farmerLocation']
                      
              print(productList[y]['distanceFromVendor'],"  ",x['productDescription'])
              
        return productList
              
 
     
    @classmethod
    def calculateSingleDistance(self,lon1,lat1,lon2,lat2):
        return self.haversine(lon1=lon1,lat1=lat1,lon2=lon2,lat2=lat2)
     
    @classmethod
    def harvasineFilter(self,productList,vendorLocation,filter):
        print(type(productList))  
        print(len(productList))
        print(vendorLocation)
        
        if filter== "distance" :
            sortedList=self.distanceCalculating(self=self,productList=productList,vendorLocation=vendorLocation)
            return sorted(sortedList, key=lambda x: x['distanceFromVendor'])
        elif filter== "highestQuantity":
             sortedList=self.distanceCalculating(self=self,productList=productList,vendorLocation=vendorLocation)
             sortedList=sorted(sortedList,key=lambda x:x['productQuantityLeftInInventory'],reverse=True)
             return sortedList
        elif filter=="lowestPrice" : 
             print("ddddddd")
             sortedList=self.distanceCalculating(self=self,productList=productList,vendorLocation=vendorLocation)
             sortedList=sorted(sortedList,key=lambda x:float(x['currentBidPrice']))
             return sortedList
             
            
        
        
        
        