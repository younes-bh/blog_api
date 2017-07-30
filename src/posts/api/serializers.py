from rest_framework.serializers import (
        ModelSerializer,
        HyperlinkedIdentityField,
        SerializerMethodField,
        )

from posts.models import Post

from comments.models import Comment
from comments.api.serializers import CommentSerializer


post_detail_url = HyperlinkedIdentityField(
        view_name= "posts-api:detail",
        lookup_field="slug"
        )


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'id',
            'title',
            'slug',
            'content',
            'publish',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'url',
            'title',
            'user',
            'slug',
            'content',
            'html',
            'publish',
            'image',
            'comments',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_html(self, obj):
        return obj.get_markdown()

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
        ]