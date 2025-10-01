from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny

from base.formapi import SignupSerializer
from .models import *

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import logout
from django.shortcuts import redirect ,get_object_or_404
from django.db import IntegrityError




# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny] 




class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Login is open to anyone

    def post(self, request):
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                # Create JWT tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can logout

    def post(self, request, format=None):
        logout(request)  # This clears the user's session
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    


from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import requests

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    access_token = request.data.get('access_token')

    if not access_token:
        return JsonResponse({'detail': 'No access token provided'}, status=400)

    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    try:
        response = requests.get(
            user_info_url,
            headers={'Authorization': f'Bearer {access_token}'}
        )
    except requests.RequestException as e:
        return JsonResponse({'detail': f'Error contacting Google: {str(e)}'}, status=502)

    if response.status_code != 200:
        return JsonResponse({'detail': 'Invalid Google access token'}, status=400)

    user_info = response.json()
    email = user_info.get('email')
    name = user_info.get('name')

    if not email:
        return JsonResponse({'detail': 'Google account has no email'}, status=400)

    user, created = User.objects.get_or_create(
        username=email,
        defaults={'email': email, 'first_name': name or ''}
    )

 

    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        'detail': 'Login successful',
        'email': user.email,
        'name': user.first_name,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }, status=200)

