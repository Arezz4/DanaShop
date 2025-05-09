from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializers import UpdatePasswordSerializer

register_user = swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
            'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date of birth'),
            'profile_picture': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Base64-encoded image string (e.g., "data:image/jpeg;base64,...")'
            ),
        },
        required=['email', 'username', 'password']
    ),
    responses={
        201: openapi.Response('User registered successfully'),
        400: openapi.Response('Bad Request'),
    }
)
update_profile = swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        },
    ),
    responses={
        201: openapi.Response('User updated successfully'),
        400: openapi.Response('Bad Request'),
    }
)
update_password  = swagger_auto_schema(
        operation_description="Update the user's password",
        request_body=UpdatePasswordSerializer,
        responses={
            200: openapi.Response(
                description="Password updated successfully",
                examples={
                    "application/json": {
                        "message": "Password updated successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "current_password": ["Current password is incorrect."],
                        "new_password": ["This password is too short. It must contain at least 8 characters."]
                    }
                }
            ),
        }
    )