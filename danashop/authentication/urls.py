from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # get new access token
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update-profile'),
    path('update_password/', views.UpdatePasswordView.as_view(), name='update-password'),

]
