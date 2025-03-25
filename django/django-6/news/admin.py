from django.contrib import admin
from .models import News, Comment

# Register your models here.

class CommentInline(admin.TabularInline):
    """Display comments inline (inside news item)."""
    model = Comment
    extra = 5  


class NewsAdmin(admin.ModelAdmin):
    """Configure display of news in the admin panel."""
    list_display = ("title", "content", "created_at", "has_comments")  
    inlines = [CommentInline] 
    def has_comments(self, obj):
        return obj.comments.exists()


admin.site.register(News, NewsAdmin)