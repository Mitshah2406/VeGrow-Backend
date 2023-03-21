from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes,parser_classes
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser ,FormParser,JSONParser
import uuid
from PIL import Image
from .serializers import farmerSerializer,userAuthSerializer,vendorSerializer,productInventorySerializer,AllProductListSerializer
from .models import Farmers,Vendor,userAuth,ProductInventory,AllProductList     
from rest_framework import status
import random



#farmers
@api_view(["POST"])
def farmerSignUp(request):
   try:
  
    data=json.loads(request.body)

    serializer=userAuthSerializer(data={'id':data['id'],"role":"farmer"})
  
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        data['id']=user   
        serializer=farmerSerializer(data=data)
     
        print(serializer.is_valid(raise_exception=True))
        if serializer.is_valid(raise_exception=True):
            farmer=serializer.save()
            token=RefreshToken.for_user(user)
            print(f"this is user {user.id}")
            return Response({"token":str(token.access_token) ,"id":user.id},status=status.HTTP_201_CREATED)
   except Exception as e:
       print(e)
       return Response(e.args,status=status.HTTP_400_BAD_REQUEST)   
  
  
@api_view(["POST"])  
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def addFarmerLocationDetails(request):
 try:
  data=json.loads(request.body)
  farmer=Farmers.objects.filter(id=data['id']).update(location=data['location'])
  return Response("done",status=status.HTTP_200_OK)  
 except Exception as e:
  print(e.args)
  return Response(e.args,status=status.HTTP_400_BAD_REQUEST)  

    
@api_view(["POST"])
def farmerLogin(request):
   try:
    data=json.loads(request.body)
    farmer=Farmers.objects.get(farmer=data['id'])
    
    data=farmerSerializer(farmer).data
    token=RefreshToken.for_user(farmer.id)
    data['token']=str(token.access_token)
    return Response(data,status=status.HTTP_202_ACCEPTED)
     
   except Exception as e:
       print(e)
       return Response(e.args,status=status.HTTP_204_NO_CONTENT)   
  
  
  
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])    
@parser_classes([MultiPartParser,FormParser,JSONParser])     
def addProductToInventory(request):
 try:    
   path=settings.MEDIA_ROOT+"/farmers/produce/"
   data={} 
   print(request.FILES.getlist('images'))   
   print(request.POST.get('productId'))
   product=AllProductList.objects.get(id=request.POST.get('productId'))
   data['productName']=product.productName
   data['productId']=product.pk
   print(data["productName"])
   data['productDescription']=request.POST.get('productDescription')
   data['productExpiryDate']=request.POST.get('productExpiryDate')
   data['productQuantity']=json.loads(request.POST.get('productQuantity'))
   data['farmerId']=request.POST.get('farmerId')
      
   imagelist=''
   images=request.FILES.getlist('images')
   if len(images) != 0:
    for x in images:
     rawByte=x.read()
     img=ContentFile(rawByte) 
     img=Image.open(img)  
     uid=str(uuid.uuid4())
     imagelist=imagelist+uid+".png"+","
     img.save(path+uid+".png",'png')
   else:
     imagelist=''  
     
   data['productImages']=imagelist
   
   serialaizer=productInventorySerializer(data=data)
   if serialaizer.is_valid(raise_exception=True):
      serialaizer.save()
      return Response("Done",status=status.HTTP_200_OK) 
   
 except Exception as e:
   print(e)
   return Response(e.args,status=status.HTTP_400_BAD_REQUEST)    
  
    
@api_view(["POST"]) 
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getMyListedProductList(request):   
 try:     
  data=json.loads(request.body)
  
  productList=ProductInventory.objects.filter(farmerId=data['farmerId']).values("inventoryId","productName","productExpiryDate","productQuantity")
    
  return Response(productList,status=status.HTTP_200_OK)
 except Exception as e:
    print(e.args)
    return Response(e.args,status=status.HTTP_400_BAD_REQUEST)
 
 
@api_view(["POST"]) 
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getMyListedProductDetails(request):
  try:
    data=json.loads(request.body)
    inventory=ProductInventory.objects.get(inventoryId=data["inventoryId"])
    print(data)  
    data=productInventorySerializer(inventory).data
    return Response(data)
    
  except Exception as e:
    print(e.args)
    return Response(e.args,status=status.HTTP_400_BAD_REQUEST)
    
  
      
  
#vendors
@api_view(["POST"])
def vendorSignUp(request):
  try:  
    data=json.loads(request.body)
    serializer=userAuthSerializer(data={"id":data['id'],"role":"vendor"})
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        data['id']=user
        print(data)
        serializer=vendorSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            token=RefreshToken.for_user(user)
            return Response({"token":str(token.access_token) },status=status.HTTP_201_CREATED)
  except Exception as e:
      print(e)
      return Response(e.args,status=status.HTTP_400_BAD_REQUEST)      
              

    
@api_view(["POST"])    
def vendorLogin(request):
   try:
       
    data=json.loads(request.body)         
    vendor=Vendor.objects.get(id=data['id'])
    
    data=vendorSerializer(vendor).data
    token=RefreshToken.for_user(vendor.id)
    data['token']=str(token.access_token)
    return Response(data,status=status.HTTP_202_ACCEPTED)
     
   except Exception as e:
       return Response(e.args,status=status.HTTP_204_NO_CONTENT)  
  
  
     
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def tp(request):
    return Response("hello")     
  
  
  
  
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def searchProductforFarmer(request):  
 try:    
  data=json.loads(request.body)
  dataList=AllProductList.objects.filter(productName__istartswith=data['search'])
  
  dataList=AllProductListSerializer(dataList,many=True).data
  print(dataList)
  return Response(dataList,status=status.HTTP_200_OK)
 except Exception as e:
   print(e.args)
   return Response(e.args,status=status.HTTP_400_BAD_REQUEST)
  
    
  
  
#common Routes
@api_view(["POST"])
def phoneNumberCheck(request):
  try:  
    data="+91"+str(json.loads(request.body)['phone'])
    print(data)
    farmer=Farmers.objects.get(phone=data)
    farmerData=farmerSerializer(farmer).data
    token=AccessToken.for_user(farmer.id)
    newRes = {"exist":True,"token":str(token),"role":"farmer"}
    newRes.update(farmerData)
    return  Response(newRes,status=status.HTTP_200_OK) 
    
    
  except Exception as e: 
      print("farmer")
      print(e)
      
      try:
        vendor=Vendor.objects.get(phone=data)
        token=AccessToken.for_user(vendor.id)
        vendordata=vendorSerializer(vendor).data
       
        newRes = {"exist":True,"token":str(token),"role":"vendor"}
        newRes.update(vendordata)
        return  Response(newRes,status=status.HTTP_200_OK) 
    
      except : 
            return  Response({"exist":False},status=status.HTTP_200_OK) 
         



       
@api_view(["POST"])
def delete(request):
    res=userAuth.objects.all().delete()
    return Response(res)   
    
@api_view(["POST"])
def insertInAllProducts(request):
  data=json.loads(request.body)             
  products=data['list']
  for x in products:
    print(x)
    print()
    serializer=AllProductListSerializer(data={"productName":x,"productMarketPrice":"%.2f"%random.uniform(40,200)})
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      print(x)
  return Response(products)      
  




