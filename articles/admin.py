from django.contrib import admin
from articles.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_author',]
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Author, AuthorAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_moderator','is_author',]
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Member, MemberAdmin)

class ModeratorAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_moderator',]
    
    def name(self, obj):
        return obj.member.name

admin.site.register(Moderator, ModeratorAdmin)

class CommentInLine(admin.StackedInline):
    model=Comment
    extra=1

class ArticleAdmin(admin.ModelAdmin):
    model=Article
    extra = 0
    prepopulated_fields = {'slug': ('title',)}
    inlines=(CommentInLine,)
    list_display=('category', 'title', 'author', 'created_at')
    list_filter=('title', 'category', 'created_at')
    
    def author(self, obj):
        return obj.author.user

admin.site.register(Article, ArticleAdmin)
