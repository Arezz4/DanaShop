from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import  RegisterSerializer, UpdateProfileSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Permission
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import CustomUser
from drf_yasg import openapi
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from .docs.swagger_docs import *

@method_decorator(name='post', decorator=update_profile)
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    
    def post(self, request):
        user = request.user  # Get the currently authenticated user
        serializer = UpdateProfileSerializer(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@method_decorator(name='post', decorator=update_password)

class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    def post(self, request):
        user = request.user  # Get the currently authenticated user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        if not user.check_password(current_password):
            return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password or len(new_password) < 8:
            return Response({"error": "New password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
@method_decorator(name='post', decorator=register_user)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        
        user = serializer.save()
        # permission = Permission.objects.get(codename='add_product')
        # user.user_permissions.add(permission)
        # user.save()
    

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Authenticate the user manually
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Update the last_login field
            user.last_login = timezone.now()  # Set the current time as last_login
            user.save()  # Save the user instance to update the last_login field

            # Call the parent class's post method to perform the actual login and token generation
            response = super().post(request, *args, **kwargs)
            return response
        else:
            # If authentication failed, return an error response
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
