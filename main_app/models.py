from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import string
import random

# Create your models here.
class Club(models.Model):
    club_name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
    invite = models.CharField(max_length=6, default=''.join(random.choice(string.ascii_uppercase+string.digits) for i in range(6)))

    def __str__(self):
     return self.club_name
    
    def get_absolute_url(self):
     return reverse('club', kwargs={'club_id': self.id})

class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500, blank=True, null=True)
    desc = models.TextField(max_length=10000, blank=True, null=True)
    isbn = models.CharField(max_length=15, blank=True, null=True)
    image = models.CharField(max_length=1000, blank=True, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    # meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, primary_key=True)
    # ratings = models.ForeignKey(Rating, on_delete=models.CASCADE)

    def __str__(self):
     return self.title
    

class Meeting(models.Model):
    date = models.DateField(blank=True, null=True)
    meeting_link = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    chapters = models.CharField(max_length=100, default='All')
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    book = models.OneToOneField(Book, on_delete=models.CASCADE, blank=True, null=True)

    # def __str__(self):
    #  return self.date
    

class Discussion(models.Model):
    COMMENT_TYPES = (
            ('comment', 'Comment'),
            ('quesiton', 'Discussion Question'),
            ('quote', 'Quote')
    )

    disc_type =  models.CharField(max_length=100, choices=COMMENT_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    comment = models.TextField(max_length=10000)

# class Rec(models.Model):
#     votes = models.IntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     club = models.ForeignKey(Club, on_delete=models.CASCADE)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
