
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
        fields = ('username', 'first_name' ,'currency', 'email', 'password', 'password2')
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