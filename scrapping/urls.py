from django.urls import path
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os
from django.contrib import admin

def download_file(request, file_path):
    # Construct the full path to the file using the MEDIA_ROOT setting.
    media_root = settings.MEDIA_ROOT
    file = os.path.join(media_root, file_path)

    # Check if the file exists.
    if os.path.isfile(file):
        with open(file, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file)}"'
            return response
    else:
        return HttpResponse("File not found", status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('downloads/<path:file_path>/', download_file, name='download_file'),
]