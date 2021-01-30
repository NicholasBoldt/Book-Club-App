from django.contrib import admin
from .models import Club, Meeting, Discussion, Book, Rec, Rating

# Register your models here.
admin.site.register(Club)
admin.site.register(Meeting)
admin.site.register(Discussion)
admin.site.register(Book)
admin.site.register(Rec)
admin.site.register(Rating)