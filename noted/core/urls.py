from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('', include(('content.urls', 'content'), namespace='content'))
]
