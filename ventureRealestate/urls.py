
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('ventureadmin/', admin.site.urls),
    path('', include('indexApp.urls')),
    path('', include('useraccount.urls')),
    path('venturedashboard/', include('dashboard.urls')),
    path('auth-login/',auth_login,name='auth_login'),
    path('auth-logout/',auth_logout,name='auth_logout'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


