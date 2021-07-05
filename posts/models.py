from django.db import models

import uuid
from decimal import Decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from versatileimagefield.fields import VersatileImageField


POST_STATUS = Choices(
    (0, 'pending', 'Pending'),
    (2, 'like', 'Like'),
    (4, 'dislike', 'Dislike'),
)


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = 'posts_tag'
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.tag

    def save(self, *args, **kwargs):
        super(Tag, self).save(*args, **kwargs)
        self.tag = self.tag.lower()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=128)
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        db_table = 'posts_post'
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        # ordering = ('-timestamp',)

    def __str__(self):
        return self.description



class PostImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    image = VersatileImageField('Image', upload_to="posts/images")
    tags = models.ManyToManyField('posts.Tag',)

    class Meta:
        db_table = 'posts_post_image'
        verbose_name = _('post image')
        verbose_name_plural = _('posts images')

    def __str__(self):
        return str(self.post)

    

class PostStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=POST_STATUS, default=POST_STATUS.pending)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        db_table = 'posts_post_status'
        verbose_name = _('post status')
        verbose_name_plural = _('posts statuses')

    def __str__(self):
        return str(self.post)