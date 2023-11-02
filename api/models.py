# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django.db import models
from cloudinary.models import CloudinaryField

class Election(models.Model):
    title = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        now = timezone.now() + timedelta(hours=6)
        if self.start_date <= now <= self.end_date:
            self.is_open = True
        else:
            self.is_open = False
        super().save(*args, **kwargs)


class Position(models.Model):
    name = models.CharField(max_length=20)
    max_vote = models.IntegerField()
    priority = models.IntegerField()
    election = models.ForeignKey(Election,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return  self.name

ACCOUNT_TYPE = (
    ('Admin', 'Admin'),
    ('Voter', 'Voter'),
)



class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voter')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE, default='Voter')
    verified = models.BooleanField(default=True)
    voted = models.BooleanField(default=False)
    election = models.ForeignKey(Election, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
      return self.user.username


@receiver(post_save, sender=User)
def create_user_voter(sender, instance, created, **kwargs):
    if created:
        Voter.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_voter(sender, instance, **kwargs):
    instance.voter.save()

class Candidate(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=20)
    # photo = models.ImageField(upload_to="candidates", blank=True)
    photo = CloudinaryField('image')
    bio = models.CharField(max_length=50)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    def __str__(self):
        return self.fullname


class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voter = models.ForeignKey(Voter,on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return self.voter.user.username


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    message = models.TextField()

    def __str__(self):
        return self.name