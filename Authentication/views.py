from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from .serializers import farmerSerializer,userAuthSerializer,vendorSerializer
from .models import Farmers,Vendor,userAuth
from rest_framework import status


#farmers
@api_view(["POST"])
def farmerSignUp(request):
   try:
    print("hello")     
    data=json.loads(request.body)
    print("hello")
    serializer=userAuthSerializer(data={'id':data['id'],"roll":"farmer"})
  
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        data['farmer']=user   
        serializer=farmerSerializer(data=data)
        print("Sssss")
        print(serializer.is_valid(raise_exception=True))
        if serializer.is_valid(raise_exception=True):
            farmer=serializer.save()
            token=RefreshToken.for_user(user)
            return Response({"token":str(token.access_token) },status=status.HTTP_201_CREATED)
   except Exception as e:
       return Response(e.args,status=status.HTTP_400_BAD_REQUEST)   
  
@api_view(["POST"])
def farmerLogin(request):
   try:
    data=json.loads(request.body)
    farmer=Farmers.objects.get(farmer=data['id'])
    
    data=farmerSerializer(farmer).data
    token=RefreshToken.for_user(farmer.farmer)
    data['token']=str(token.access_token)
    return Response(data,status=status.HTTP_202_ACCEPTED)
     
   except Exception as e:
       return Response(e.args,status=status.HTTP_204_NO_CONTENT)   
  
  
  
  
  
  
#vendors
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
            serializer.save()
            token=RefreshToken.for_user(user)
            return Response({"token":str(token.access_token) },status=status.HTTP_201_CREATED)
  except Exception as e:
      return Response(e.args,status=status.HTTP_400_BAD_REQUEST)      
              
    
@api_view(["POST"])    
def vendorLogin(request):
   try:
       
    data=json.loads(request.body)         
    vendor=Vendor.objects.get(vendor=data['id'])
    
    data=vendorSerializer(vendor).data
    token=RefreshToken.for_user(vendor.vendor)
    data['token']=str(token.access_token)
    return Response(data,status=status.HTTP_202_ACCEPTED)
     
   except Exception as e:
       return Response(e.args,status=status.HTTP_204_NO_CONTENT)  
     
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def tp(request):
    return Response("hello")     
  
  
  
  
  
#common Routes
@api_view(["POST"])
def phoneNumberCheck(request):
  try:  
    data="+91"+str(json.loads(request.body)['phone'])
    print(data)
    farmer=Farmers.objects.filter(phone=data)
    print(farmer)
    if farmer:
        return Response({"exist":True},status=status.HTTP_200_OK)
    vendor=Vendor.objects.filter(phone=data)
    if vendor:
      return Response({"exist":True},status=status.HTTP_200_OK)
    return Response({"exist":False},status=status.HTTP_200_OK) 

  except Exception as e:   
      return Response(e.args,status=status.HTTP_400_BAD_REQUEST)    




       
@api_view(["POST"])
def delete(request):
    res=userAuth.objects.all().delete()
    return Response(res)   
    
                
  
        
  




