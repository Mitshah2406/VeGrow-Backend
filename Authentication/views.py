from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes,parser_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import os
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser ,FormParser,JSONParser
import uuid
from PIL import Image

from .serializers import farmerSerializer,userAuthSerializer,vendorSerializer,productInventorySerializer
from .models import Farmers,Vendor,userAuth,ProductInventory
from rest_framework import status

from django.core import serializers


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
  
  
  
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])    
@parser_classes([MultiPartParser,FormParser,JSONParser])     
def addProductToInventory(request):
 try:    
   print(request.data)
   queryDict=request.data
   myDict = dict(queryDict)
   print(myDict)
   path=settings.MEDIA_ROOT+"/farmers/produce/"  
   imgF=myDict['image'][0].file
   img=Image.open(imgF)
   print(type(imgF))
   
   
   path = default_storage.save(path+str(uuid.uuid4)+".jpeg", ContentFile(imgF))
   tmp_file = os.path.join(settings.MEDIA_ROOT, path)
   
  #  print(type(myDict['image'][0]))
  #  img=ContentFile(imgF,str(uuid.uuid4)+"png")
  #  img=Image.open(img)
  #  img.show()
   
  #  img=Image.open(myDict['image'][0])
  #  img.save(path+str(uuid.uuid4),'png')
  # #  img=Image.open(img)
  #  print(img)
  #  img.show()
   
  
  # data=json.loads(request.body)
  
  # print(data)
  # serializer=productInventorySerializer(data=data)
  # if serializer.is_valid(raise_exception=True):
  #     print("hi")      
  #     product=serializer.save()
  #     data=productInventorySerializer(product).data
  #     print("hii",data)
   return Response("data",status=status.HTTP_200_OK)
 except Exception as e:
   return Response(e.args,status=status.HTTP_400_BAD_REQUEST)    
  
  
#vendors
@api_view(["POST"])
def vendorSignUp(request):
  try:  
    data=json.loads(request.body)
    serializer=userAuthSerializer(data={"id":data['id'],"roll":"vendor"})
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
        token=RefreshToken.for_user(farmer)
        return Response({"exist":True,"token":str(token.access_token)},status=status.HTTP_200_OK)
    vendor=Vendor.objects.filter(phone=data)
    if vendor:
      token=RefreshToken.for_user(vendor)
      return Response({"exist":True,"token":str(token.access_token)},status=status.HTTP_200_OK)
    return Response({"exist":False},status=status.HTTP_200_OK) 

  except Exception as e:   
      return Response(e.args,status=status.HTTP_400_BAD_REQUEST)    




       
@api_view(["POST"])
def delete(request):
    res=userAuth.objects.all().delete()
    return Response(res)   
    
                
  
        
  




