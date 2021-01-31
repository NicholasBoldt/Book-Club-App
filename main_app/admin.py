from django.contrib import admin
<<<<<<< HEAD
from .models import Club, Meeting, Discussion, Book, Rec, Rating
=======
from .models import *
>>>>>>> 78e6f94b370fba9cca9fc553967e10d7de2c6fc3

# Register your models here.
admin.site.register(Club)
admin.site.register(Meeting)
admin.site.register(Discussion)
admin.site.register(Book)
admin.site.register(Rec)
admin.site.register(Rating)