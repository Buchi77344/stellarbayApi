from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import redirect, render
from base.formapi import *
from .models import *


from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import json
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# Authentication Views
class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

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



# API Platform Views
class APIEndpointViewSet(viewsets.ModelViewSet):
    serializer_class = APIEndpointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return APIEndpoint.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        endpoint = self.get_object()
        endpoint.is_active = not endpoint.is_active
        endpoint.save()
        return Response({'status': 'toggled', 'is_active': endpoint.is_active})

class APIRequestLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = APIRequestLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return APIRequestLog.objects.filter(user=self.request.user)

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Calculate real-time stats
        user_endpoints = APIEndpoint.objects.filter(created_by=request.user)
        user_logs = APIRequestLog.objects.filter(user=request.user)
        
        # Last 7 days logs for trend calculation
        week_ago = timezone.now() - timedelta(days=7)
        recent_logs = user_logs.filter(created_at__gte=week_ago)
        
        total_endpoints = user_endpoints.count()
        total_requests = user_logs.count()
        
        # Calculate success rate (assuming 2xx status codes are successful)
        successful_requests = user_logs.filter(status_code__range=[200, 299]).count()
        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
        
        # Calculate average response time
        avg_response_time = user_logs.aggregate(avg_time=models.Avg('response_time'))['avg_time'] or 0
        
        # Recent activity
        recent_activity = user_logs.select_related('endpoint').order_by('-created_at')[:5]
        
        stats = {
            'total_endpoints': total_endpoints,
            'total_requests': total_requests,
            'success_rate': round(success_rate, 1),
            'avg_response_time': round(avg_response_time, 1),
            'recent_activity': APIRequestLogSerializer(recent_activity, many=True).data
        }
        
        return Response(stats)

class APIProxyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Proxy for API testing from the playground
        """
        method = request.data.get('method', 'GET')
        url = request.data.get('url')
        headers = request.data.get('headers', {})
        body = request.data.get('body')
        
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Prepare request parameters
        request_kwargs = {
            'method': method,
            'url': url,
            'headers': headers,
            'timeout': 30
        }
        
        if body and method in ['POST', 'PUT', 'PATCH']:
            if headers.get('Content-Type') == 'application/json':
                request_kwargs['json'] = body
            else:
                request_kwargs['data'] = body
        
        # Make the request
        start_time = timezone.now()
        try:
            response = requests.request(**request_kwargs)
            response_time = (timezone.now() - start_time).total_seconds() * 1000
            
            # Log the request
            APIRequestLog.objects.create(
                user=request.user,
                method=method,
                url=url,
                status_code=response.status_code,
                response_time=response_time
            )
            
            # Prepare response
            response_data = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'response_time': round(response_time, 2),
                'data': response.text
            }
            
            # Try to parse JSON response
            try:
                response_data['data'] = response.json()
            except:
                pass
            
            return Response(response_data)
            
        except requests.exceptions.Timeout:
            return Response({'error': 'Request timeout'}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Quick Actions
class QuickActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        action_type = request.data.get('action')
        
        if action_type == 'test_all_endpoints':
            return self.test_all_endpoints(request.user)
        elif action_type == 'generate_docs':
            return self.generate_documentation(request.user)
        elif action_type == 'export_config':
            return self.export_configuration(request.user)
        else:
            return Response({'error': 'Unknown action'}, status=status.HTTP_400_BAD_REQUEST)
    
    def test_all_endpoints(self, user):
        endpoints = APIEndpoint.objects.filter(created_by=user, is_active=True)
        results = []
        
        for endpoint in endpoints:
            try:
                start_time = timezone.now()
                response = requests.request(
                    method=endpoint.method,
                    url=endpoint.url,
                    timeout=10
                )
                response_time = (timezone.now() - start_time).total_seconds() * 1000
                
                # Log the test request
                APIRequestLog.objects.create(
                    user=user,
                    endpoint=endpoint,
                    method=endpoint.method,
                    url=endpoint.url,
                    status_code=response.status_code,
                    response_time=response_time
                )
                
                results.append({
                    'endpoint': endpoint.name,
                    'status': 'success' if response.status_code < 400 else 'error',
                    'status_code': response.status_code,
                    'response_time': round(response_time, 2)
                })
            except Exception as e:
                results.append({
                    'endpoint': endpoint.name,
                    'status': 'error',
                    'error': str(e)
                })
        
        return Response({'results': results})
    
    def generate_documentation(self, user):
        endpoints = APIEndpoint.objects.filter(created_by=user)
        docs = {
            'title': f'API Documentation - {user.username}',
            'endpoints': APIEndpointSerializer(endpoints, many=True).data,
            'generated_at': timezone.now().isoformat()
        }
        return Response(docs)
    
    def export_configuration(self, user):
        endpoints = APIEndpoint.objects.filter(created_by=user)
        config = {
            'user': user.username,
            'exported_at': timezone.now().isoformat(),
            'endpoints': APIEndpointSerializer(endpoints, many=True).data
        }
        return Response(config)


def Index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')

def product(request):
    return render(request, 'product.html')


def dash(request):
    return render(request, 'dash.html')

def customer(request):
    return render(request, 'customer.html')


def orders(request):
    return render(request, 'orders.html')

def analysis(request):
    return render(request, 'analysis.html')


def discount(request):
    return render(request, 'discount.html')


def settings(request):
    return render(request, 'settings.html')