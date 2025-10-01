from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login-api'),
     path('auth/google/', google_auth, name='google_auth'),
]
