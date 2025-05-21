import re
from django.forms import ValidationError
from rest_framework import serializers
from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField 

class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        try:
            validate_password(value) 
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class RegisterSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField(required=False)  

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'profile_picture', 'is_staff', 'date_of_birth', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},  
            'email': {'validators': []},  
            'username': {'validators': []}, 
        }
        
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists. Please use a different email.")
        return value
    
    def validate_username(self, value):
        return value

    def validate(self, attrs):
        if 'is_staff' in self.initial_data:
            request = self.context.get('request')
            if not request or not request.user.is_superuser: 
                raise serializers.ValidationError({
                    'is_staff': "You do not have permission to set this field."
                })
            attrs['is_staff'] = self.initial_data['is_staff']  
        return attrs

    def validate_username(self, value):
        if re.match(r'^\d', value):
            raise serializers.ValidationError("Username cannot start with a number.")
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("That username is taken. Please use a different one.")

        return value

    def validate_profile_picture(self, value):
        max_size_mb = 5
        max_size_bytes = max_size_mb * 1024 * 1024 
        if value.size > max_size_bytes:
            raise serializers.ValidationError(f"Profile picture size cannot exceed {max_size_mb} MB.")
        return value

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                date_of_birth=validated_data.get('date_of_birth', None),
                profile_picture=validated_data.get('profile_picture', None),
                is_staff=validated_data.get('is_staff', False), 
            )
            return user
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username','date_of_birth']
        extra_kwargs = {
            'username': {'validators': []},
        }

    def validate(self, attrs):
        print((f"Updating user profile with data: {attrs}"))
        if not any(attrs.values()):
            raise serializers.ValidationError({
                "error": "At least one field must be provided to update the profile."
            })
        return attrs

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value
