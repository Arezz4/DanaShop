from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('customers/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('customers/register/', views.RegisterView.as_view(), name='register'),
    path('customers/profile/update/', views.UpdateProfileView.as_view(), name='update-profile'),
    path('customers/update_password/', views.UpdatePasswordView.as_view(), name='update-password'),
    path('admin/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
]
