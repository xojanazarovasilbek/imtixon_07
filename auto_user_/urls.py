from django.urls import path 
from .views import *

urlpatterns = [
    path('regis/', RegisterApi.as_view()),
    path('login/',LoginApi.as_view()),
    path('lagout/',LogautApi.as_view()),
    path('profile/', ProfileApi.as_view())

]