from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users.apps import UsersConfig
from users.views import UserRegisterView, email_verification, reset_password, UserListView

app_name = UsersConfig.name

urlpatterns = [
    path('list/', UserListView.as_view(), name='list'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('email-confirm/<str:token>/', email_verification, name='email_confirm'),
    path('reset-password/', reset_password, name='reset_password')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)