from rest_framework import serializers
from .models import Farmers,Vendor,userAuth,ProductInventory,AllProductList


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
 
 
 
       
class productInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductInventory
        fields="__all__"
    def create(self, validated_data):  
       
        product=ProductInventory.objects.create(farmerId=validated_data['farmerId'],productId=validated_data["productId"])
        print(validated_data["productId"])
        product.productName=validated_data['productName']
        
  
        product.productExpiryDate=validated_data['productExpiryDate']
        product.productQuantity=validated_data['productQuantity']
        if 'productDescription' in validated_data:
            product.productDescription=validated_data['productDescription']
        if 'productImages' in validated_data:
            product.productImages=validated_data['productImages']
        product.save()        
        
        return product
    
    
        