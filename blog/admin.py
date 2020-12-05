from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Article, Comment, Category, Contact

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title', 'tags', 'category', 'created_on', 'status', 'description')
    summernote_fields = ('content',)

admin.site.register(Article, ArticleAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')