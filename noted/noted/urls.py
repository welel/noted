from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes.urls')),
    path('notes/', include('notes.urls')),
    path('accounts/', include('allauth.urls')),
]
