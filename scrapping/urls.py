from django.urls import path
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os
from django.contrib import admin
from django.conf.urls.static import static
from main.views import *


def list_files(request):
    # Get the path to your STATIC_ROOT directory
    static_root = settings.MEDIA_ROOT

    # List all files in the directory
    files = os.listdir(static_root)

    # Create an HTML response with links to the files
    file_links = []
    for file in files:
        if file.endswith('.mp4') or file.endswith('.jpg') or 'video' in str(file):
            # file_path = os.path.join(static_root, file)
            file_links.append(f'<a href="/downloads/{file}/">{file}</a>')
        elif 'video' in str(file) and not file.endswith('.mp4') or not file.endswith('.jpg') and 'admin' not in str(file):
            file_links.append(f'<a href="/downloads/{file}/">{file}</a>')
            # entries = os.listdir(current_folder)
    return HttpResponse("<br>".join(file_links))


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
    elif os.path.isdir(file):
        file_links = []
        files = os.listdir(file)
        if not files: return HttpResponse("Folder is empty",status=200)
        for file in files:
            if file.endswith('.mp4') or file.endswith('.jpg') or 'video' in str(file):
                # file_path = os.path.join(static_root, file)
                file_links.append(f'<a href="/downloads/{file}/">{file}</a>')
            elif 'video' in str(file) and not file.endswith('.mp4') or not file.endswith('.jpg') and 'admin' not in str(file):
                file_links.append(f'<a href="/downloads/{file}/">{file}</a>')
        return HttpResponse("<br>".join(file_links))
    else:
        HttpResponse("Folder not found.", status=404)


def csv_file(request):
    # Construct the full path to the file using the MEDIA_ROOT setting.
    media_root = settings.BASE_DIR
    file = os.path.join(media_root, 'brazzers_videos_details.csv')

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
    path('list_files/', list_files, name='list_file'),
    path('csv/', csv_file, name='csv_file'),
    path('', data_flair),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)