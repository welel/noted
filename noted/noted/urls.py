from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from noted import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('', include('notes.urls')),
    path('notes/', include(('notes.urls', 'notes'), namespace='notes')),
    path('accounts/', include('allauth.urls')),
    path('tags/', include(('tags.urls', 'tags'), namespace='tags')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('actions/', include(('actions.urls', 'actions'), namespace='actions')),
]

handler404 = 'noted.views.handler404'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, 
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
