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

     path("api/profiles/", views.ProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name="profile-list"),
    path("api/profiles/<int:pk>/", views.ProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="profile-detail"),

    # ✅ Category
    path("api/categories/", views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name="category-list"),
    path("api/categories/<slug:slug>/", views.CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="category-detail"),

    # ✅ Product
    path("api/products/", views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name="product-list"),
    path("api/products/<slug:slug>/", views.ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="product-detail"),

    # ✅ Cart
    path("api/carts/", views.CartViewSet.as_view({'get': 'list', 'post': 'create'}), name="cart-list"),
    path("api/carts/<int:pk>/", views.CartViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="cart-detail"),
    path("api/carts/<int:pk>/add-item/", views.CartViewSet.as_view({'post': 'add_item'}), name="cart-add-item"),
    path("api/carts/<int:pk>/remove-item/", views.CartViewSet.as_view({'post': 'remove_item'}), name="cart-remove-item"),

    # ✅ Orders
    path("api/orders/", views.OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name="order-list"),
    path("api/orders/<int:pk>/", views.OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="order-detail"),

    # ✅ Address
    path("api/addresses/", views.AddressViewSet.as_view({'get': 'list', 'post': 'create'}), name="address-list"),
    path("api/addresses/<int:pk>/", views.AddressViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="address-detail"),

    # ✅ Payment
    path("api/payments/", views.PaymentViewSet.as_view({'get': 'list', 'post': 'create'}), name="payment-list"),
    path("api/payments/<int:pk>/", views.PaymentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="payment-detail"),

]
