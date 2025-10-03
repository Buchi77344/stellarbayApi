
from rest_framework import serializers
from .models import *

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