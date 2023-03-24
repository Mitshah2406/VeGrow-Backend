import zoneinfo
from django.conf import settings
import pprint
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

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
from .serializers import farmerSerializer,userAuthSerializer,vendorSerializer,productInventorySerializer,AllProductListSerializer,ProductBiddingSerializer,PurchaseTransactionsSerializer
from .models import Farmers,Vendor,userAuth,ProductInventory,AllProductList,ProductBidding,PurchaseTransactions     
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
            serializer.save()
            farmer=serializer.data
            print(farmer)   
            
            token=AccessToken.for_user(user)
            print(token)
            farmer.update({"token":str(token),"role":"farmer"})  
            
            print(f"this is user {user.id}")
            return Response( farmer,status=status.HTTP_201_CREATED)
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])   
def specificFarmerData(request):
 try: 
  data=json.loads(request.body)
  farmer=Farmers.objects.get(id=data['id'])
  serializer=farmerSerializer(farmer).data
  print(serializer['location'])
  if not serializer["location"]:
    del serializer["location"]
  return Response(serializer,status=status.HTTP_200_OK)
 except Exception as e:
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
   farmer=Farmers.objects.get(id=request.POST.get('farmerId'))
   data['productName']=product.productName
   data['initialBidPrice']=request.POST.get('initialBidPrice')
   print(f"ininit {data['initialBidPrice']}")
   data['productUnit']=request.POST.get('productUnit')
   data['productQuantity']=request.POST.get('productQuantity')  
   data['productId']=product.pk
   print(data["productName"])
   data['productDescription']=request.POST.get('productDescription')
   data['productExpiryDate']=request.POST.get('productExpiryDate')
   
   
   data['farmerId']=farmer.id
   data['farmerLocation']=farmer.location
      
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
 
    filter_=data["filter"]
    if filter_=="pending":
     productList=ProductInventory.objects.filter(farmerId=data['farmerId'],status="listed")
    elif filter_=="bidded":
      productList=ProductInventory.objects.filter(farmerId=data['farmerId'],status="bidded")
    elif filter_=="confrimed":
      productList=ProductInventory.objects.filter(farmerId=data['farmerId'],status="confrimed")
    elif filter_=="All":
     productList=ProductInventory.objects.filter(farmerId=data['farmerId'])
        

    data=productInventorySerializer(productList,many=True).data
    print(data)
    return Response(data,status=status.HTTP_200_OK)
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
           vendor=serializer.save()
           data=vendorSerializer(vendor).data
           token=RefreshToken.for_user(user)
           data.update({"token":str(token.access_token) ,"role":"vendor"})
           return Response(data,status=status.HTTP_201_CREATED)
  except Exception as e:
      print(e)
      return Response(e.args,status=status.HTTP_400_BAD_REQUEST)      
              
@api_view(["POST"])  
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def addVendorLocationDetails(request):
 try:
  data=json.loads(request.body)
  vendor=Vendor.objects.filter(id=data['id']).update(location=data['location'])
  return Response("done",status=status.HTTP_200_OK)  
 except Exception as e:
  print(e.args)
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
def specificVendorData(request):
 try: 
  data=json.loads(request.body)
  farmer=Vendor.objects.get(id=data['id'])
  serializer=vendorSerializer(farmer).data
  print(serializer['location'])
  if not serializer["location"]:
    del serializer["location"]
  return Response(serializer,status=status.HTTP_200_OK)
 except Exception as e:
   return Response(e.args,status=status.HTTP_400_BAD_REQUEST)   
     
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def tp(request):
    return Response("hello")     
  
  
  
  
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def searchProductsForVendorFilter(request): 
 try:
  data=json.loads(request.body)
  vendor=Vendor.objects.get(id=data['vendorId'])
  # 
  if "filter" in data:
    filter_=data['filter']
  else:
    data['filter']="distance"
    filter_=data['filter']
  productList=ProductInventory.objects.filter(productName__istartswith=data['productName'])
  productList=productInventorySerializer(productList,many=True).data
  data=productInventorySerializer.harvasineFilter(productList=productList,vendorLocation=vendor.location,filter=filter_)
  
  
  return Response(data,status=status.HTTP_200_OK)
 except Exception as e:
   print(e.args)
   return Response(e.args,status=status.HTTP_400_BAD_REQUEST) 


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def inventoryProductListForVendor(request):
  try:   
    
    productList=list(ProductInventory.objects.all().values_list("productName"))    
    print() 
    productList1=[]
    for x in productList:
      productList1.append(x[0])
      
    return Response(productList1,status=status.HTTP_200_OK)
  except Exception as e:
    print(e.args)
    return Response(e.args,status=status.HTTP_200_OK)
    



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def specificProductDetailsForVendor(request):  
 try: 
   data=json.loads(request.body)
   vendor=Vendor.objects.get(id=data['vendorId'])
   product=ProductInventory.objects.get(inventoryId=data['productId'])
   farmer=Farmers.objects.get(id=product.farmerId)
   distance=productInventorySerializer.calculateSingleDistance(lat1=farmer.location['lat'],lon1=farmer.location['lon'],lat2=vendor.location['lat'],lon2=vendor.location['lon'])
   farmerData={"farmerName":farmer.fName+" "+farmer.lName,"distance":distance}
   productData=productInventorySerializer(product).data
   print("inventoryId")
   print(productData["inventoryId"])
   bidData=ProductBidding.objects.filter(inventoryId=productData['inventoryId']).order_by('-bidAmount')
   bidData=ProductBiddingSerializer(bidData,many=True).data
   print(bidData)  
   productData["previousBids"]=bidData
   
   productData.update(farmerData)
   return Response(productData,status=status.HTTP_200_OK)
 except Exception as e:
   print(e.args)
   return Response(e.args,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def topfiveProductFromInventory(request):
  try:  
    productList=ProductInventory.objects.all().order_by("-productListedDate")[:5]
    productList=productInventorySerializer(productList,many=True).data
    
    return Response(productList,status=status.HTTP_200_OK)
  except Exception as e:
    print(e.args) 
    return Response(e.args,status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def productBidList(request):
  data=json.loads(request.body)
  filter_=data['filter']
  if filter_=="latest":
   productBids=ProductBidding.objects.filter(inventoryId=data['inventoryId']).order_by('-dateTime')
   productBids=ProductBiddingSerializer(productBids,many=True).data
   return Response(productBids,status=status.HTTP_200_OK)
  elif filter_=="highestPrice":
    productBids=ProductBidding.objects.filter(inventoryId=data['inventoryId']).order_by('-bidAmount')
    productBids=ProductBiddingSerializer(productBids,many=True).data
    return Response(productBids,status=status.HTTP_200_OK)
  elif filter_=="highestQuantity":
    productBids=ProductBidding.objects.filter(inventoryId=data['inventoryId']).order_by('-bidQuantity')
    productBids=ProductBiddingSerializer(productBids,many=True).data
    return Response(productBids,status=status.HTTP_200_OK)
    
    

def specificProductDetailsForFarmer(request):
  try:
    data=json.loads(request.body)
    product=ProductInventory.objects.get(inventoryId=data['inventoryId'],farmerId=data['farmerId'])
    productdata=productInventorySerializer(productdata).data
    
  except Exception as e:
    print(e.args)  


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])     
def bidOnProduct(request): 
 try: 
  data=json.loads(request.body)
  data['dateTime']=timezone.localtime(timezone.now())
  print(data)
  try:
   updateBid=ProductBidding.objects.get(inventoryId=data['inventoryId'],vendorId=data['vendorId'])
   updateBid.dateTime=timezone.localtime(timezone.now())
   print(timezone.localtime(timezone.now()))
  #  print(zoneinfo.available_timezones())
   updateBid.bidAmount=data['bidAmount']
   updateBid.bidQuantity=data['bidQuantity']
   updateBid.save()
   ProductInventory.objects.filter(inventoryId=data['inventoryId']).update(currentBidPrice=updateBid.bidAmount,status="bidded")
   return Response("done",status=status.HTTP_200_OK)
  except ObjectDoesNotExist as e:
     bidSrializer=ProductBiddingSerializer(data=data)
     if bidSrializer.is_valid(raise_exception=True):
        bid=bidSrializer.save()
        ProductInventory.objects.filter(inventoryId=data['inventoryId']).update(currentBidPrice=data['bidAmount'],status="bidded")  
      
        return Response("done",status=status.HTTP_200_OK)
    
  
 except Exception as e:
 
  
     return Response(e.args,status=status.HTTP_400_BAD_REQUEST)     
  
  
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])   
def farmerAcceptOrRejectBid(request):
 try: 
  data=json.loads(request.body)
  product=ProductBidding.objects.filter(bidId=data['bidId']).update(bidStatus="rejected")
 except Exception as e:
   print(e.args)
   return Response(e.args,status=status.HTTP_400_BAD_REQUEST) 
  
    

# @api_view(["POST"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated]) 
# def     
  
  
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def searchProductforFarmer(request):  
 try:    
  
  dataList=AllProductList.objects.all()
  
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
    
      except Exception as e:
            print(e.args) 
        
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


@api_view(["POST"])
def deleteAllProductList(request):
  res=AllProductList.objects.all().delete()
  return Response(res)   
  
@api_view(["POST"])
def deleteSpecificUser(request):
  data=json.loads(request.body)
  res=userAuth.objects.get(id=data['id']).delete()
  return Response(res)  




