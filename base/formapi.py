
from rest_framework import serializers
from .models import *

from django_countries.serializer_fields import CountryField


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'}, 
        required=True 
    )
    password2 = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'}, 
        required=True, 
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ('username' , 'email', 'password', 'password2')
        extra_kwargs = {
            'email': {'required': True},
        }
        

    def validate(self, data):
        """
        Check that the two password entries match.
        """
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove password2 from the validated data
        validated_data.pop('password2')
        # Use create_user to ensure the password is hashed properly
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

    
from django.contrib.auth import get_user_model
from .models import APIEndpoint, APIRequestLog, DashboardStats

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class APIEndpointSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = APIEndpoint
        fields = [
            'id', 'name', 'method', 'url', 'description', 'is_active',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class APIRequestLogSerializer(serializers.ModelSerializer):
    endpoint_name = serializers.CharField(source='endpoint.name', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = APIRequestLog
        fields = [
            'id', 'endpoint', 'endpoint_name', 'user', 'user_name',
            'method', 'url', 'status_code', 'response_time', 'created_at'
        ]
        read_only_fields = ['id', 'endpoint', 'user', 'created_at']


class DashboardStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardStats
        fields = ['total_endpoints', 'total_requests', 'success_rate', 'avg_response_time', 'calculated_at']




# ✅ Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True, required=False)

    class Meta:
        model = Profile
        fields = ["id", "avatar", "address", "city", "country", "created_at"]
        read_only_fields = ["id", "created_at"]


# ✅ Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "created_at"]
        read_only_fields = ["id", "created_at"]


# ✅ Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True
    )
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "seller", "category", "category_id",
            "name", "slug", "description", "price",
            "stock", "image", "is_active",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "seller", "created_at", "updated_at"]


# ✅ CartItem Serializer
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source="product", queryset=Product.objects.all(), write_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()


# ✅ Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "items", "total_price"]
        read_only_fields = ["id", "user", "created_at", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()


# ✅ OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()


# ✅ Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "user", "status", "total_amount",
            "shipping_address", "paid", "payment_reference",
            "created_at", "updated_at", "items"
        ]
        read_only_fields = [
            "id", "user", "created_at", "updated_at", "total_amount", "payment_reference"
        ]


# ✅ Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Address
        fields = [
            "id", "user", "full_name", "phone", "street",
            "city", "state", "country", "postal_code", "is_default"
        ]
        read_only_fields = ["id", "user"]


# ✅ Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id", "order", "user", "amount", "payment_method",
            "status", "transaction_id", "created_at"
        ]
        read_only_fields = ["id", "order", "user", "created_at"]