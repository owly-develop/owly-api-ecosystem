"""
User serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    full_name = serializers.CharField(read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'avatar', 'company', 'company_name',
            'role', 'status', 'assigned_projects', 'territories',
            'performance_metrics', 'sales_target', 'settings',
            'signature', 'calendar_url', 'social_media',
            'manager', 'is_staff', 'is_active',
            'date_joined', 'last_login', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 'created_at', 'updated_at'
        ]
        extra_kwargs = {'password': {'write_only': True}}


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone',
            'company', 'role', 'assigned_projects', 'territories', 'manager'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        assigned_projects = validated_data.pop('assigned_projects', [])
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        if assigned_projects:
            user.assigned_projects.set(assigned_projects)
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user details
    """
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'avatar',
            'role', 'status', 'assigned_projects', 'territories',
            'sales_target', 'settings', 'signature',
            'calendar_url', 'social_media', 'manager'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Passwords don't match"})
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile (current user)
    """
    full_name = serializers.CharField(read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'avatar', 'company', 'company_name',
            'role', 'status', 'settings', 'signature',
            'calendar_url', 'social_media', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'email', 'company', 'role', 'status', 'date_joined', 'last_login']

