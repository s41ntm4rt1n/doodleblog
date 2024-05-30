from django.contrib import admin
from articles.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)


class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_moderator','is_author',]
    # prepopulated_fields = {'slug': ('name',)}
    # def save_model(self, request, obj, form, change):
    #     if obj.is_author:
    #         author=Author.objects.create(member=obj)
    #         author.save()
    #     else:
    #         author=Author.objects.filter(member=obj)
    #         author.delete()
    #     if obj.is_moderator:
    #         moderator=Moderator.objects.create(member=obj)
    #         moderator.save()
    #     else:
    #         moderator=Moderator.objects.filter(member=obj)
    #         moderator.delete()
    #     super().save_model(request, obj, form, change)

admin.site.register(Member, MemberAdmin)

            
class AuthorAdmin(admin.ModelAdmin):
    list_display = [ 'name','is_author',]
    
    def name(self, obj):
        return obj.member.name

    def save_model(self, request, obj, form, change):
        if not obj.is_author:
            obj.member.is_author=False
            obj.member.save()
        super().save_model(request, obj, form, change)
admin.site.register(Author, AuthorAdmin)

class ModeratorAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_moderator',]
    
    def name(self, obj):
        return obj.member.name
    
    def save_model(self, request, obj, form, change):
        if not obj.is_moderator:
            obj.member.is_moderator=False
            obj.member.save()
        super().save_model(request, obj, form, change)

admin.site.register(Moderator, ModeratorAdmin)


class CommentInLine(admin.StackedInline):
    model=Comment
    extra=1

class ArticleAdmin(admin.ModelAdmin):
    model=Article
    extra = 0
    prepopulated_fields = {'slug': ('title',)}
    inlines=(CommentInLine, )
    list_display=('category', 'title',  'created_at')
    list_filter=('title', 'category', 'created_at')
    
    def author(self, obj):
        return obj.author.member

admin.site.register(Article, ArticleAdmin)

