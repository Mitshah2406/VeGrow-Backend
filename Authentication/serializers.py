from rest_framework import serializers
from .models import Farmers,Vendor,userAuth,ProductInventory
from phonenumber_field.modelfields import PhoneNumberField

class farmerSerializer(serializers.ModelSerializer):
    class Meta:
    
        model=Farmers
        fields=[
            'farmer',
                'fName',
                'lName',
                'email',
                'phone',
                'location'
                ]
    def create(self, validated_data):
        user=Farmers.objects.create(farmer=validated_data['farmer'])
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
            'roll'
        ]    


class vendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
      
        fields=[
            'vendor',
            'location',
                'fName',
                'lName',
                'email',
                'phone',
                
                ]
    
    def create(self, validated_data):
        user=Vendor.objects.create(vendor=validated_data['vendor'])
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
      
class productInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductInventory
        fields='__all__'
    def create(self, validated_data):  
        product=ProductInventory.objects.create(farmerId=validated_data['farmerId'])
        # product.farmerId=validated_data['farmerId']
        product.productName=validated_data['productName']
        
  
        product.productExpiryDate=validated_data['productExpiryDate']
        product.productQuantity=validated_data['productQuantity']
        if 'productDiscription' in validated_data:
            product.productDescription=validated_data['productDiscription']
        if 'productImages' in validated_data:
            product.productImages=validated_data['productImages']
        product.save()        
        
        return product