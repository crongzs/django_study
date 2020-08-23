from django.db import models


# Create your models here.


# ----------------- 创建ORM模型 -----------------


class ORMBook(models.Model):
    # int 类型 自增长
    id = models.AutoField(primary_key=True)
    # varchar(50)
    name = models.CharField(max_length=50, null=False)
    # varchar(20)
    authot = models.CharField(max_length=20, null=False)
    # float
    price = models.FloatField(null=False, default=0)

    class Meta:
        # 定义数据表名
        db_table = 'orm_book'


# ----------------- 外键与表关系 -----------------


class ORMCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '<category:%s>' % self.name

    class Meta:
        db_table = 'orm_category'


def category_default():
    return ORMCategory.objects.get(pk=1)


class ORMArticle(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # on_delete=models.CASCADE 级联操作，如果外键对应的那条数据被删除了，那么这条数据也会被删除
    category = models.ForeignKey("ORMCategory", on_delete=models.CASCADE)

    # on_delete=models.PROTECT 受保护。即只要这条数据引用了外键的那条数据，那么就不能删除外键的那条数据。
    # category = models.ForeignKey("ORMCategory", on_delete=models.PROTECT)

    # on_delete=models.SET_NULL 设置为空。如果外键的那条数据被删除了，那么在本条数据上就将这个字段设置为空。如果设置这个选项，前提是要指定这个字段可以为空。
    # category = models.ForeignKey("ORMCategory", on_delete=models.SET_NULL, null=True)

    # on_delete=models.SET_DEFAULT 设置默认值。如果外键的那条数据被删除了，那么本条数据上就将这个字段设置为默认值。如果设置这个选项，前提是要指定这个字段一个默认值。
    # category = models.ForeignKey("ORMCategory", on_delete=models.SET_DEFAULT, default=ORMCategory.objects.get(pk=1))

    # on_delete=models.SET() SET()：如果外键的那条数据被删除了。那么将会获取SET函数中的值来作为这个外键的值。SET函数可以接收一个可以调用的对象（比如函数或者方法），如果是可以调用的对象，那么会将这个对象调用后的结果作为值返回回去。
    # category = models.ForeignKey("ORMCategory", on_delete=models.SET(ORMCategory.objects.get(pk=1)))
    # category = models.ForeignKey("ORMCategory", on_delete=models.SET(category_default))

    # 不采取任何行为。一切全看数据库级别的约束
    # category = models.ForeignKey("ORMCategory", on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<article:%s>' % self.title

    class Meta:
        db_table = 'orm_article'
        ordering = ['-created', 'id']  # 先按时间排序，如果时间相同按照id排序


# 自关联
class ORMComment(models.Model):
    content = models.TextField()
    origin_comment = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return '<comment:%s>' % self.id

    class Meta:
        db_table = 'orm_comment'


# 一对一
class ORMFrontUser(models.Model):
    username = models.CharField(max_length=200)

    def __str__(self):
        return '<front:%s>' % self.username

    class Meta:
        db_table = 'orm_front'


class UserExtension(models.Model):
    school = models.CharField(max_length=100)
    user = models.OneToOneField("ORMFrontUser", on_delete=models.CASCADE, related_name='ext')

    def __str__(self):
        return '<user_ext:%s>' % self.user.username

    class Meta:
        db_table = 'orm_user_ext'


# 多对多
class ORMTag(models.Model):
    name = models.CharField(max_length=100)
    articles = models.ManyToManyField("ORMArticle")

    def __str__(self):
        return '<tag:%>' % self.name

    class Meta:
        db_table = 'orm_tag'


# ----------------- ORM查询 -----------------


class FilterArticle(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.ForeignKey("FilterCategory", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '<article:%s>' % self.title

    class Meta:
        db_table = 'filter_article'


class FilterCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'filter_category'


class FilterAuthor(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'filter_author'


class FilterPublish(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'filter_publish'


class FilterBook(models.Model):
    name = models.CharField(max_length=50)
    page = models.IntegerField()
    price = models.FloatField()
    rating = models.FloatField()
    author = models.ForeignKey("FilterAuthor", on_delete=models.CASCADE)
    publisher = models.ForeignKey("FilterPublish", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'filter_book'


class FilterBookOrder(models.Model):
    book = models.ForeignKey("FilterBook", on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.book.name

    class Meta:
        db_table = 'filter_book_order'
