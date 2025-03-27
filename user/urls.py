from django.urls import path, include
from user.views import ChangePasswordView,CustomAuthToken, EmailVerificationView, LoginAPIView, UserDetailView, UserRegistrationAPIView, ValidateUserView

app_name = 'user'
urlpatterns = [
    # path('api/token-auth/', CustomAuthToken.as_view(), name='custom-token-auth'),
    path('login/', LoginAPIView.as_view(), name='auth'),
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('user/', UserDetailView.as_view(), name='user-detail'), 
    path('validate_user/', ValidateUserView.as_view(), name='validate_user'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'), 
]
