from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    full_name = models.CharField(max_length=30)
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