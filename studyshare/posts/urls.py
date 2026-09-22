from django.urls import path
from . import views
import uuid

urlpatterns = [
    path('', views.home, name='home'),
    path('resource/<int:resource_id>/', views.resource_details, name='resource_details'),
    path('upload/', views.upload, name='upload'),
    path('profile/', views.profile, name='profile'),
    path('browse/', views.browse, name='browse')
]
 
