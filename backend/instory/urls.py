"""
URL configuration for instory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from posts.views import PostCreateView, UserPostsView, PostView, PostLikesView
from users.views import LoginView, LogoutView, CurrentUserView, RegisterView, EmailVerificationLinkSendView, \
    EmailVerifyView, PasswordResetView, PasswordResetConfirmView, EmailChangeView, PasswordChangeView, \
    ProfileSettingsView, UsernameChangeView, AvatarUpdateView, UserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/login/', LoginView.as_view(), name='login'),
    path('api/v1/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/v1/auth/register/', RegisterView.as_view(), name='register'),
    path('api/v1/users/me/', CurrentUserView.as_view(), name='current_user'),
    path('api/v1/email/verify/', EmailVerificationLinkSendView.as_view(), name='email.verify.send'),
    path('api/v1/email/verify/<uidb64>/<token>/', EmailVerifyView.as_view(), name='email.verify'),
    path('api/v1/password/reset/', PasswordResetView.as_view(), name='password.reset'),
    path('api/v1/password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password.reset.confirm'),
    path('api/v1/settings/security/email/', EmailChangeView.as_view(), name='email.change'),
    path('api/v1/settings/security/password/', PasswordChangeView.as_view(), name='password.change'),
    path('api/v1/settings/profile/', ProfileSettingsView.as_view(), name='profile.update'),
    path('api/v1/settings/profile/username/', UsernameChangeView.as_view(), name='username.change'),
    path('api/v1/settings/profile/avatar/', AvatarUpdateView.as_view(), name='username.change'),
    path('api/v1/posts/', PostCreateView.as_view(), name='posts.create'),
    path('api/v1/users/<username>/', UserView.as_view(), name='users.get'),
    path('api/v1/users/<username>/posts/', UserPostsView.as_view(), name='user.posts'),
    path('api/v1/posts/<id>/', PostView.as_view(), name='post'),
    path('api/v1/posts/<post_id>/likes/', PostLikesView.as_view(), name='post.likes'),
]
