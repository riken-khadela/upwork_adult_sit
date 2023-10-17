from django.contrib import admin
from .models import videos_collection,configuration
# Register your models here.

admin.site.register(videos_collection)
admin.site.register(configuration)
