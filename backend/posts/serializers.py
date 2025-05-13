from PIL import Image
from rest_framework import serializers

from posts.models import Post, PostComment
from users.serializers import UserSerializer


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['image', 'description']

    def validate_image(self, image):
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

    # def create(self, validated_data):
    #     # image = validated_data.get('image')
    #     # if image:
    #     #     img = Image.open(image)
    #     #
    #     #     if img.mode in ("RGBA", "P"):
    #     #         img = img.convert("RGB")
    #     #
    #     #     buffer = BytesIO()
    #     #     img.save(buffer, format='JPEG')
    #
    #     return Post.objects.create(**validated_data)


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
