from django.contrib import admin
from.models import PostImage,Tag,PostStatus,Post,POST_STATUS

admin.site.site_header = "Custom Admin"
admin.site.site_title = "Custom"
admin.site.index_title = "Welcome to Custom Admin"


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', )
    search_fields = ('id', 'tag', )

admin.site.register(Tag, TagAdmin)




class PostImageInlineAdmin(admin.TabularInline):
    list_display = ('id', 'post',)
    model = PostImage

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        if obj:
            if obj.postimage_set.count() >= 1:
                extra = 0
        return extra

class PostStatusInlineAdmin(admin.TabularInline):
    list_display = ('id', 'post',)
    model = PostStatus

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra



class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'timestamp', 'likes')
    exclude = ('timestamp',)
    search_fields = ('id', 'description', )

    inlines = [
        PostImageInlineAdmin,PostStatusInlineAdmin
    ]

    def likes(self, obj):
        count = PostStatus.objects.filter(post=obj,status=POST_STATUS.like).count()
        return count
    likes.short_description = 'No. likes'
    likes.admin_order_field = 'post__status'

admin.site.register(Post, PostAdmin)