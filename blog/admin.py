from django.contrib import admin
#from django.db import models
from blog import models
# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Post)