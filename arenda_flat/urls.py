"""arenda_flat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),
    path('api/rest_auth/', include('rest_auth.urls')), #точка входа /rest_auth/login/ точка выхода /rest_auth/logout/
    path('api/rest_auth/registration/', include('rest_auth.registration.urls')), # сброс пароля rest_auth/password/reset/confirm/
    path('', include('rest_framework.urls')),

    path('', include('flat.urls')),
    path('arenda/', include('arenda.urls')),
    path('accounts/', include('allauth.urls')),

    path('', include('custom_user.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,\
    document_root=settings.STATIC_ROOT)