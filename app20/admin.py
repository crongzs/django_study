from django.contrib import admin

# Register your models here.

from app20.models import Article, Author, Category, Book, BookOrder, Publish


# 给Article表创建一个管理器
class ArticleModelAdmin(admin.ModelAdmin):
    pass


# 将管理器注册进admin
admin.site.register(Article, ArticleModelAdmin)
