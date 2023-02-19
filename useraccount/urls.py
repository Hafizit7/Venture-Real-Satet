from django.urls import path
from .views import *

urlpatterns = [
    path('register/',register, name='register'),
    path('register-view/',register_view, name='register_view'),
    path('register-update<str:id>/',register_edit, name='register_edit'),
    path('register-delete<str:id>/',register_delete, name='register_delete'),
    path('register-change/',change_password, name='change_password'),
]