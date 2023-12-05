"""
URL configuration for colorglimmer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static

from app import views
from colorglimmer import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accessibility_report/', views.AccessibilityReportView.as_view(), name='accessibility_report'),
    path('score_report/', views.ScoreReportView.as_view(), name='score_report'),
    path('modification_suggestion/', views.ModificationSuggestion.as_view(), name='modification_suggestion'),
    path('image_recoloring/', views.ImageRecoloringView.as_view(), name='image_recoloring'),
    path('upload_file/', views.upload_file, name='upload_file'),

    path('about/', views.AboutUsView.as_view(), name='about_us'),
    path('contact/', views.ContactUsView.as_view(), name='contact_us'),
    path('', views.IndexView.as_view(), name='index'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)