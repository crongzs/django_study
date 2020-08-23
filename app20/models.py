from django.db import models


# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name='分类')
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='添加时间')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'app20_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'app20_category'


class Author(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'app20_author'


class Publish(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'app20_publish'


class Book(models.Model):
    name = models.CharField(max_length=50)
    page = models.IntegerField()
    price = models.FloatField()
    rating = models.FloatField()
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    publisher = models.ForeignKey("Publish", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'app20_book'


class BookOrder(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.book.name

    class Meta:
        db_table = 'app20_book_order'
