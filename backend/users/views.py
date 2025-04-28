from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.forms import LoginForm, RegisterForm
from users.models import User
from users.serializers import UserSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        form = LoginForm(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        user = form.cleaned_data['user']
        remember_me = form.cleaned_data['remember_me']

        login(request, user)
        if remember_me:
            request.session.set_expiry(2592000)  # 30 дней
        else:
            request.session.set_expiry(86400)  # 1 день

        return Response({'success': True}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        response = Response({'success': True}, status=status.HTTP_200_OK)
        response.delete_cookie('sessionid')
        return response


class CurrentUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(
                request.user,
                context={
                    'request': request,
                    'with_followers': True,
                    'with_following': True,
                }
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        form = RegisterForm(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=form.cleaned_data['email'],
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            is_active=True
        )

        login(request, user)
        request.session.set_expiry(86400)

        return Response({'success': True}, status=status.HTTP_201_CREATED)
