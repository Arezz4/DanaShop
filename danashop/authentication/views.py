from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import  RegisterSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Permission


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        permission = Permission.objects.get(codename='add_product')

        user.user_permissions.add(permission)

        user.save()
    

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
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
