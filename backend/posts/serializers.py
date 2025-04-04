from rest_framework import serializers

from posts.models import Post, PostComment
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'description', 'date_created', 'comments_count', 'likes_count', 'is_liked']

    def get_user(self, obj):
        if self.context.get('with_user', False):
            return UserSerializer(obj.user).data

    def get_comments_count(self, obj):
        return getattr(obj, 'comments_count', None)

    def get_likes_count(self, obj):
        return getattr(obj, 'likes_count', None)

    def get_is_liked(self, obj):
        return getattr(obj, 'is_liked', None)


class PostCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ['id', 'user', 'post', 'parent_comment', 'content', 'date_created', 'likes_count']
        depth = 1

    def get_user(self, obj):
        if self.context.get('with_user', False):
            return UserSerializer(obj.user).data

    def get_post(self, obj):
        if self.context.get('with_post', False):
            return PostSerializer(obj.post).data

    def get_likes_count(self, obj):
        return getattr(obj, 'likes_count', None)

    def get_is_liked(self, obj):
        return getattr(obj, 'is_liked', None)
