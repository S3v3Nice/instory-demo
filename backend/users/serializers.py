from rest_framework import serializers
from rest_framework.request import Request

from users.models import User, UserFollow


class UserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    date_verified_email = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_verified_email', 'avatar', 'first_name', 'last_name', 'followers',
                  'following']

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
