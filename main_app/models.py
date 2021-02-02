from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Club(models.Model):
    club_name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500, blank=True, null=True)
    desc = models.TextField(max_length=10000, blank=True, null=True)
    isbn = models.CharField(max_length=15, blank=True, null=True)
    image = models.CharField(max_length=1000, blank=True, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    # meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, primary_key=True)
    # ratings = models.ForeignKey(Rating, on_delete=models.CASCADE)

class Meeting(models.Model):
    date = models.DateField()
    meeting_link = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    chapters = models.CharField(max_length=100, default='All')
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    book = models.OneToOneField(Book, on_delete=models.CASCADE, blank=True, null=True)

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

class Rec(models.Model):
    votes = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # rating = models.IntegerField()
    # book = models.ForeignKey(Book, on_delete=models.CASCADE)







    # meetings = models.ForeignKey(Meeting, on_deletee=models.CASCADE)
