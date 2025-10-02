from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api-endpoints', views.APIEndpointViewSet, basename='api-endpoints')
router.register(r'api-logs', views.APIRequestLogViewSet, basename='api-logs')

urlpatterns = [ 
    path('', views.Index, name='index'),
    path('login/', views.login, name='login'),
    path('api/', include(router.urls)),
    path('api/auth/signup/', views.SignupAPIView.as_view(), name='signup'),
    path('api/auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('api/auth/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('api/auth/google/', views.google_auth, name='google-auth'),
    path('api/dashboard/stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'), 
    path('api/proxy/test/', views.APIProxyView.as_view(), name='api-proxy'),
    path('api/user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('api/quick-actions/', views.QuickActionView.as_view(), name='quick-actions'),
    path('product/', views.product, name='product'),
    path('dashboard/', views.dash, name='dashboard'),
    path('customer/', views.customer, name='customer'),
    path('orders/', views.orders, name='orders'),
    path('analysis/', views.analysis, name='analysis'),
    path('discount/', views.discount, name='discount'),
    path('settings/', views.settings, name='settings'),
]
