from django.contrib import admin
from .models import videos_collection,configuration, send_mail, sender_mail
# Register your models here.

admin.site.register(videos_collection)
admin.site.register(configuration)
admin.site.register(send_mail)
admin.site.register(sender_mail)
