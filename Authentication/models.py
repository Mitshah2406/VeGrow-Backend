from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
import uuid
class userAuthManager(BaseUserManager):
    # def create_superuser(self, id, password=None ):
    
    #     user = self.create_user(
    #        id=id
            
    #     )
    #     user.set_unusable_password()
        
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user
    def create_user(self,id):
        if not id: 
            raise ValueError("user must have an id")
        user=self.model(id=id)
        # user.set_unusable_password()
        user.save(using=self._db)
        return user
          
class userAuth(AbstractBaseUser):
    
    id=models.CharField(max_length=254,primary_key=True)
    role=models.CharField(max_length=254,null=False)
     
    objects=userAuthManager()
    USERNAME_FIELD='id'
    REQUIRED_FIELDS=['role']
    
    def __str__(self):   
        return self.id
    def has_perm(self, perm, obj=None):

        return True

    def has_module_perms(self, app_label):
       

        return True

    @property
    def is_staff(self):
     
        return self.id
           
       
class Vendor(models.Model):
    id=models.OneToOneField(userAuth,on_delete=models.CASCADE,primary_key=True)
    fName=models.CharField(max_length=254)
    lName=models.CharField(max_length=254)
    location=models.JSONField(default=dict,null=True)    
    phone=PhoneNumberField(region='IN',null=True)
    email=models.EmailField(null=True)
    
class Farmers(models.Model):
    id=models.OneToOneField(userAuth,on_delete=models.CASCADE,primary_key=True)
    fName=models.CharField(max_length=254)
    lName=models.CharField(max_length=254)
    location=models.JSONField(default=dict,null=True) 
    phone=PhoneNumberField(region='IN',null=True)
    email=models.EmailField(null=True)
    
  
  
class AllProductList(models.Model):
    id=models.AutoField(primary_key=True)
    productName=models.CharField(max_length=254,unique=True)
    imgage=models.ImageField(upload_to="farmers/allProductList",null=True)  
    productMarketPrice=models.DecimalField(max_digits=10,decimal_places=2)           
             
class ProductInventory(models.Model):
    productId=models.ForeignKey(AllProductList,on_delete=models.PROTECT)
    inventoryId=models.UUIDField(primary_key=True,default=uuid.uuid4)
    farmerId=models.ForeignKey(Farmers,on_delete=models.CASCADE)
    productName=models.CharField(max_length=254)
    productDescription=models.TextField(null=True)
    productListedDate=models.DateField(auto_now_add=True)
    productExpiryDate=models.DateField(null=True)
    productImages=models.TextField(default='',null=True,blank=True)
    productUnit=models.CharField(max_length=254,null=True)
    productQuantity=models.CharField(max_length=254,null=True)
    initialBidPrice=models.DecimalField(max_digits=15,decimal_places=2)
    
                 
                 

    
    
    
                     