from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

class userAuthManager(BaseUserManager):
    def create_superuser(self, id, password=None ):
       
        user = self.create_user(
           id=id
            
        )
        user.set_unusable_password()
        
        user.is_admin = True
        user.save(using=self._db)
        return user
    def create_user(self,id):
        if not id: 
            raise ValueError("user must have an id")
        user=self.model(id=id)
        user.save(using=self._db)
        return user
          
class userAuth(AbstractBaseUser):
    
    id=models.CharField(max_length=254,primary_key=True)
    roll=models.CharField(max_length=254,null=False)
     
    objects=userAuthManager()
    USERNAME_FIELD='id'
    REQUIRED_FIELDS=['roll']
    
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
    vendor=models.OneToOneField(userAuth,on_delete=models.CASCADE,primary_key=True)
    fName=models.CharField(max_length=254)
    lName=models.CharField(max_length=254)
    location=models.JSONField(default=dict,null=True)    
    phone=PhoneNumberField(region='IN',null=True)
    email=models.EmailField(null=True)
    
class Farmers(models.Model):
    farmer=models.OneToOneField(userAuth,on_delete=models.CASCADE,primary_key=True)
    fName=models.CharField(max_length=254)
    lName=models.CharField(max_length=254)
    location=models.JSONField(default=dict,null=True) 
    phone=PhoneNumberField(region='IN',null=True)
    email=models.EmailField(null=True)
             