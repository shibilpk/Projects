from rest_framework import serializers
from posts.models import Post, PostImage, PostStatus, POST_STATUS
from django.urls import reverse


class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'pk',
            'description',
            'timestamp',
            'images',
            'status'

        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_likes'] = PostStatus.objects.filter(post=instance, status=POST_STATUS.like).count()
        data['total_dislikes'] = PostStatus.objects.filter(post=instance, status=POST_STATUS.dislike).count()

        return data

    def get_images(self, instance):
        request = self.context.get('request')
        post_images = PostImage.objects.filter(post=instance)
        return [request.build_absolute_uri(i.image.url) for i in post_images]

    def get_status(self, instance):
        request = self.context.get('request')
        status = POST_STATUS.pending
        if request.user.is_authenticated:
            if PostStatus.objects.filter(post=instance,user=request.user).exists():
                status = PostStatus.objects.get(post=instance,user=request.user).status

        return status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostStatus
        fields = (
            'pk',
            'status',
        )
