from django.urls import path

from user.views import register_view, login_view, logout_view, MyTokenObtainPairView

app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
