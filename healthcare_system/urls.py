"""
URL configuration for healthcare_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URLs principales
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')), # Use 'users' for custom user app
    path('patients/', include('patients.urls')),
    path('medical-records/', include('medical_records.urls')), # Using hyphenated URL
    path('appointments/', include('appointments.urls')),
    path('', include('core.urls')), # Include core app URLs for dashboard/home
]

# URLs API
api_urlpatterns = [
    path('patients/', include('patients.api_urls', namespace='api_patients')),
    path('medical-records/', include('medical_records.api_urls', namespace='api_medical_records')),
]

urlpatterns += [
    path('api/', include((api_urlpatterns, 'api'), namespace='api')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)