import hashlib
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.request import Request

from users.models import User, UserFollow


class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']

    def validate_avatar(self, image):
        max_file_size = 2 * 1024 * 1024
        if image.size > max_file_size:
            raise serializers.ValidationError("The file size should not exceed 2 MB.")

        min_width = 150
        min_height = 150

        try:
            img = Image.open(image)
            width, height = img.size
        except Exception:
            raise serializers.ValidationError("Unable to process image.")

        if width < min_width or height < min_height:
            raise serializers.ValidationError(
                f"Minimum image resolution — {min_width}x{min_height} px."
            )

        image.seek(0)
        return image

    def update(self, instance: User, validated_data):
        image = validated_data.get('avatar')
        if image:
            img = Image.open(image)
            width, height = img.size
            min_dim = min(width, height)

            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            right = (width + min_dim) // 2
            bottom = (height + min_dim) // 2
            img = img.crop((left, top, right, bottom))

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            buffer = BytesIO()
            img.save(buffer, format='JPEG')

            hash_digest = hashlib.sha256(buffer.getvalue()).hexdigest()[:12]
            file_name = f"{instance.pk}_{hash_digest}.jpg"

            old_file_name = instance.avatar.name if instance.avatar else None
            instance.avatar.save(file_name, ContentFile(buffer.getvalue()), save=False)

            if old_file_name and old_file_name != instance.avatar.name:
                instance.avatar.storage.delete(old_file_name)

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    date_verified_email = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_verified_email', 'avatar', 'first_name', 'last_name', 'followers',
                  'following']

    def get_avatar(self, obj):
        if obj.avatar:
            return f"{settings.APP_URL}{obj.avatar.url}"
        return None

    def get_email(self, obj):
        """Show email only to it's owner and superusers"""
        request: Request | None = self.context.get('request')
        if request and (request.user == obj or request.user.is_superuser):
            return obj.email

    def get_date_verified_email(self, obj):
        """Show email verification date only to it's owner and superusers"""
        request: Request | None = self.context.get('request')
        if request and (request.user == obj or request.user.is_superuser):
            return obj.date_verified_email

    def get_followers(self, obj):
        if self.context.get('with_followers', False):
            return FollowerSerializer(obj.followers.all(), many=True).data

    def get_following(self, obj):
        if self.context.get('with_following', False):
            return FollowingSerializer(obj.following.all(), many=True).data


class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer()

    class Meta:
        model = UserFollow
        fields = ['follower', 'date_created']


class FollowingSerializer(serializers.ModelSerializer):
    following = UserSerializer()

    class Meta:
        model = UserFollow
        fields = ['following', 'date_created']
