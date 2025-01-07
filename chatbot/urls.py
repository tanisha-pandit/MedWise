from django.urls import path
from . import views

urlpatterns = [
    path('image/', views.image_upload_view, name='image_upload'),
]
