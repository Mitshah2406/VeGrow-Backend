from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication
import json
from .serializers import farmerSerializer,userAuthSerializer,vendorSerializer
from .models import Farmers,Vendor,userAuth
from rest_framework import status

@api_view(["POST"])
# @authentication_classes(["TokenAuthentication"])
def farmerSignUp(request):
   try:
    data=json.loads(request.body)
    serializer=userAuthSerializer(data={'id':data['id'],"roll":"farmer"})
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        data['farmer']=user   
        serializer=farmerSerializer(data=data)
        print("Sssss")
        print(serializer.is_valid(raise_exception=True))
        if serializer.is_valid(raise_exception=True):
            farmer=serializer.save()
            return Response(farmer.fName,status=status.HTTP_201_CREATED)
   except Exception as e:
       return Response(e.args)   
  
  
@api_view(["POST"])
def vendorSignUp(request):
  try:  
    data=json.loads(request.body)
    serializer=userAuthSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        data['vendor']=user
        print(data)
        serializer=vendorSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response(user.fName,status=status.HTTP_201_CREATED)
  except Exception as e:
      return Response(e.args,status=status.HTTP_400_BAD_REQUEST)      
              
  
@api_view(["POST"])
def farmerLogin(request):
   try:
    data=json.loads(request.body)
    farmer=Farmers.objects.get(farmer=data['id'])
    
    data=farmerSerializer(farmer).data
    return Response(data,status=status.HTTP_202_ACCEPTED)
     
   except Exception as e:
       return Response(e.args,status=status.HTTP_204_NO_CONTENT) 
     
     
@api_view(["POST"])    
def vendorLogin(request):
   try:
       
    data=json.loads(request.body)         
    vendor=Vendor.objects.get(vendor=data['id'])
    
    data=vendorSerializer(vendor).data
    return Response(data,status=status.HTTP_202_ACCEPTED)
     
   except Exception as e:
       return Response(e.args,status=status.HTTP_204_NO_CONTENT)  
   
   
   
       
@api_view(["POST"])
def delete(request):
    res=userAuth.objects.all().delete()
    return Response(res)   
    
                
  
        
  




