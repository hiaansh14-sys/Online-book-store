from django.db import models



# Create your models here.
class Enquiry(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    contactno=models.CharField(max_length=15)
    subject=models.CharField(max_length=200)
    message=models.TextField()
    enqdate=models.DateTimeField(auto_now_add=True)


class Logininfo(models.Model):
    usertype=models.CharField(max_length=15,default='user')
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=250)

    def __str__(self):

        return f"{self.username}-{self.usertype}"


class Usreinfo(models.Model):
    login = models.OneToOneField(Logininfo,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField( max_length=254)
    contactno=models.CharField(max_length=15 )
    address=models.CharField(max_length=255)
    picture = models.ImageField(upload_to='user_profiles')
