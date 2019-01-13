from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile/')
    neighbourhood = models.ForeignKey('Neighbourhood', blank=True, null=True)
    pub_date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.full_name

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profiles(cls):
        profiles = cls.objects.all()
        return profiles


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Neighbourhood(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='neighimage/', null=True)
    admin = models.ForeignKey(Profile, related_name='hoods', null=True)
    description = models.CharField(max_length = 100,default='this is my hood y all...')
    def save_neighbourhood(self):
        self.save()
    def delete_neighbourhood(self):
        self.delete()

class Business(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    image = models.ImageField(upload_to='bsimage/')
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='businesses')
    description = models.CharField(max_length = 100)
    profile = models.ForeignKey(Profile, related_name='profiles')
    def save_business(self):
        self.save()
    def delete_business(self):
        self.delete()
    @classmethod
    def search_by_name(cls,search_term):
        business = cls.objects.filter(title__icontains=search_term)
        return business


class Post(models.Model):
    user = models.ForeignKey(Profile, related_name='profile')
    post = models.CharField(max_length=100)
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='posts')
    
