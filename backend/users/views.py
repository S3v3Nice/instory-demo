from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from users.emails import send_verification_email, send_password_reset_email
from users.forms import LoginForm, RegisterForm, EmailChangeForm
from users.models import User
from users.serializers import UserSerializer
from users.utils import EmailVerificationTokenGenerator


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
            request.session.set_expiry(2592000)  # 30 days
        else:
            request.session.set_expiry(86400)  # 1 day

        return Response(status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        response = Response(status=status.HTTP_200_OK)
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
            password=form.cleaned_data['password']
        )

        login(request, user)
        request.session.set_expiry(86400)

        send_verification_email(user)

        return Response(status=status.HTTP_201_CREATED)


class EmailVerificationLinkSendView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'email-send'

    def post(self, request):
        user: User = request.user
        if user.date_verified_email is None:
            send_verification_email(user)
            return Response(status=status.HTTP_200_OK)

        return Response({'detail': 'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None

        if user and EmailVerificationTokenGenerator().check_token(user, token):
            user.date_verified_email = timezone.now()
            user.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'email-send'

    def post(self, request):
        form = PasswordResetForm(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            send_password_reset_email(user)

        return Response(status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None

        if not user or not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'is_invalid_token': True}, status=status.HTTP_400_BAD_REQUEST)

        form = SetPasswordForm(user=user, data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        form.save()
        return Response(status=status.HTTP_200_OK)


class EmailChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        form = EmailChangeForm(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        user: User = request.user
        user.email = form.cleaned_data['email']
        user.date_verified_email = None
        user.save()

        send_verification_email(user)

        return Response(status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        form = PasswordChangeForm(request.user, data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        form.save()
        update_session_auth_hash(request, request.user)

        return Response(status=status.HTTP_200_OK)
