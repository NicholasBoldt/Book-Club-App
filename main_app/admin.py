from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Club)
admin.site.register(Meeting)
admin.site.register(Discussion)
admin.site.register(Book)
admin.site.register(Rating)