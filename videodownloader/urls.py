from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('downloader.urls')),  # Include your app's URLs here
    # Add other URL patterns for your project as needed
]
