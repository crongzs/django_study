from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

from django.db import connection


# ------------------ Django操作数据库 ------------------
def to_do_sql(request):
    ''' Django 使用原生 sql 语句操作数据库 '''

    cursor = connection.cursor()

    # execute() 执行sql语句
    # cursor.execute("insert into sql_book(id, name, author) values (null, '三国演义', '罗贯中')")
    cursor.execute("select * from sql_book")

    # fetchone 执行了查询操作后 获取第一条数据
    # rows = cursor.fetchone()
    # fetchall 执行了查询操作后 获取所有数据
    rows = cursor.fetchall()
    # fetchmany(size) 在执行查询操作以后，获取多条数据。具体是多少条要看传的size参数。如果不传size参数，那么默认是获取第一条数据

    for row in rows:
        print(row)
    # (None, '三国演义', '罗贯中')

    context = {}

    return render(request, 'app3/app3-1Django使用原生sql.html', context=context)


# ------------------ 图书管理系统 ------------------

'''
Django 使用 原生sql语句 实现一个图书管理系统
'''


def to_do_sql1(request):
    ''' 图书管理系统首页 '''

    cursor = connection.cursor()
    cursor.execute("select id, name, author from sql_book")
    books = cursor.fetchall()
    # [(id,name,author), (...), ...]

    context = {'books': books}
    return render(request, 'app3/app3-2图书管理-图书首页.html', context=context)


def to_do_sql2(request):
    ''' 添加图书 '''
    if request.method == 'GET':
        context = {}
        return render(request, 'app3/app3-3图书管理-发布图书.html', context=context)
    else:
        cursor = connection.cursor()
        name = request.POST.get('name')
        author = request.POST.get('author')
        cursor.execute("insert into sql_book(id, name, author) values (null, '%s', '%s')" % (name, author))

        return redirect("app3:app3-2")


def to_do_sql3(request, id):
    ''' 图书详情 '''
    cursor = connection.cursor()
    cursor.execute("select id, name, author from sql_book where id=%s" % id)
    book = cursor.fetchone()
    context = {'book': book}
    return render(request, 'app3/app3-4图书管理-图书详情.html', context=context)


def to_do_sql4(request):
    ''' 删除图书 '''

    if request.method == 'POST':
        id = request.POST.get('id')
        cursor = connection.cursor()
        cursor.execute("delete from sql_book where id=%s" % id)

        return redirect('app3:app3-2')


# ------------------ ORM 外键与表关系 ------------------

from app3.models import ORMCategory, ORMArticle, ORMFrontUser, ORMTag, UserExtension


def orm1(request):
    category = ORMCategory(name='new')
    category.save()  # 在这里，先要将category保存才能被article引用

    article = ORMArticle(title='Python', content='This is Python Sex')
    article.category = category
    article.save()

    return HttpResponse('{}'.format(article.title))


def orm2(request):
    ''' 一对多 反向查询 '''
    # 获取某个分类下所有的文章
    category = ORMCategory.objects.get(pk=9)
    articles = category.ormarticle_set.all()  # 获取所有的文章
    article = category.ormarticle_set.first()  # 获取第一篇文章
    print(articles)
    return HttpResponse()


def orm3(request):
    ''' 一对多 反向添加 1 '''
    category = ORMCategory.objects.first()

    # 如果要使用如下反向添加的方式，必须保证 外键设置了 null=True，不然 article.save() 就会报错
    article = ORMArticle(title='Python', content='This is Python String')
    article.save()  # 这里必须保证外键 添加了 null=True

    category.ormarticle_set.add(article)
    category.save()

    return HttpResponse()


def orm4(request):
    ''' 一对多 反向添加 2 '''

    category = ORMCategory.objects.first()

    # 如果 外键引用没有设置 null=True, 在反向添加的add方法中添加参数 bulk=False， bulk=False会自动遍历所有对象，并将他们保存
    article = ORMArticle(title='Python', content='This is Python String')

    category.ormarticle_set.add(article, bulk=False)

    return HttpResponse()


def orm5(request):
    ''' 一对一 反向引用 '''

    # 如果模型 OneToOneField 没有设置 related_name，可以用以下方式反向引用
    front = ORMFrontUser.objects.first()
    ext = front.userextension

    # 如果模型 OneToOneField 设置了 related_name 那么必须使用 related_name 进行反向引用
    front = ORMFrontUser.objects.first()
    ext = front.ext  # 假设此时 OneToOneField 设置了 related_name='ext'

    print(ext)

    return HttpResponse()


def orm6(request):
    ''' 多对多 反向添加 '''

    article = ORMArticle.objects.first()
    tag = ORMTag(name='Language')
    tag.save()  # 再被反向添加之前必须save()，多对多关系(ManyToManyField)中的反向添加add方法没有 bulk 参数
    article.ormtag_set.add(tag)

    return HttpResponse(tag.name)


def orm7(request):
    ''' 多对多 正向添加 '''

    tag = ORMTag.objects.first()
    article = ORMArticle.objects.get(pk=10)
    tag.articles.add(article)

    return HttpResponse()


# ------------------ ORM 查询 ------------------
from app3.models import FilterArticle, FilterCategory
from datetime import datetime
from django.utils.timezone import make_aware  # 创建一个清醒的时间


def orm_filter1(request):
    ''' exact '''
    articles = FilterArticle.objects.filter(title__exact='Python')
    print(articles.query)
    print(articles)
    articles = FilterArticle.objects.filter(title__exact=None)
    print(articles.query)
    print(articles)
    return HttpResponse()


def orm_filter2(request):
    ''' iexact '''
    articles = FilterArticle.objects.filter(title__iexact='Python')
    print(articles.query)
    print(articles)
    return HttpResponse()


def orm_filter3(request):
    ''' contains '''
    articles = FilterArticle.objects.filter(title__contains='PYTHON')
    print(articles.query)
    print(articles)
    return HttpResponse()


def orm_filter4(request):
    ''' icontains '''
    articles = FilterArticle.objects.filter(title__icontains='PYTHON')
    print(articles.query)
    print(articles)
    return HttpResponse()


def orm_filter5(request):
    ''' in '''
    articles = FilterArticle.objects.filter(id__in=[1, 2, 3])
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(id__in=(1, 2, 3))
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(id__in=FilterArticle.objects.filter(content__icontains='this is'))
    print(articles.query)
    print(articles)

    categories = FilterCategory.objects.filter(filterarticle__in=[1, 2, 3])
    print(categories.query)
    print(categories)
    return HttpResponse()


def orm_filter6(request):
    ''' gt、gte、lt、lte '''
    articles = FilterArticle.objects.filter(id__gt=2)
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(id__gte=2)
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(id__lt=2)
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(id__lte=2)
    print(articles.query)
    print(articles)

    return HttpResponse()


def orm_filter7(request):
    ''' startswith、istartswith、endswith、iendswith '''

    # 大小写敏感
    articles = FilterArticle.objects.filter(title__startswith='python')
    print(articles.query)
    print(articles)
    articles = FilterArticle.objects.filter(title__endswith='python')
    print(articles.query)
    print(articles)

    # 大小写不敏感
    articles = FilterArticle.objects.filter(title__startswith='python')
    print(articles.query)
    print(articles)
    articles = FilterArticle.objects.filter(title__endswith='python')
    print(articles.query)
    print(articles)
    return HttpResponse()


def orm_filter8(request):
    ''' rang '''
    # make_aware 创建一个 aware time
    start_time = make_aware(datetime(year=2020, month=2, day=26, hour=12, minute=0, second=0))
    end_time = make_aware(datetime(year=2020, month=2, day=27, hour=12, minute=0, second=0))
    articles = FilterArticle.objects.filter(created__range=(start_time, end_time))
    print(articles.query)
    print(articles)
    return HttpResponse()


def orm_filter9(request):
    ''' date '''
    articles = FilterArticle.objects.filter(created__date=datetime(year=2020, month=2, day=26))
    print(articles.query)
    print(articles)

    ''' year、month、day、weekday '''
    articles = FilterArticle.objects.filter(created__year__gte=2019)
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(created__month=2)
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(created__day__lte=27)
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(created__week_day=3)
    print(articles.query)
    print(articles)

    return HttpResponse()


def orm_filter10(request):
    ''' isnull '''

    articles = FilterArticle.objects.filter(title__isnull=True)
    print(articles.query)
    print(articles)

    return HttpResponse()


def orm_filter11(request):
    ''' regex & iregex '''

    articles = FilterArticle.objects.filter(title__regex='Python')
    print(articles.query)
    print(articles)

    articles = FilterArticle.objects.filter(title__iregex='Python')
    print(articles.query)
    print(articles)

    return HttpResponse()


# ------------------ ORM 聚合函数 ------------------
from app3.models import FilterBook, FilterPublish, FilterAuthor, FilterBookOrder
from django.db.models import Avg, Count, Max, Min, Sum, F, Q
from django.db import connection


def orm_filter12(request):
    ''' Avg '''

    # 求图书定价的平均值
    result = FilterBook.objects.aggregate(Avg('price'))
    print(result)
    print(connection.queries)  # 使用 connection.queries 查看 sql 语句

    # aggregate 返回一个字典，字典内容为聚合函数执行的结果
    # django 默认 aggregate返回的字典的key为 字段名 加 双下划线 加 聚合函数的名称小写
    # 这个key可以自定义，如：
    result = FilterBook.objects.aggregate(avg=Avg('price'))
    print(result)
    print(connection.queries)

    # 获取每一本书售价的平均值
    result = FilterBook.objects.annotate(
        avg=Avg('filterbookorder__price'))  # 这里使用到的是反向查询，ForeignKey 中没有添加related_name 和 related_query_name
    for r in result:
        print(r.name, r.avg)
    print(connection.queries)

    return HttpResponse('Avg')


def orm_filter13(request):
    ''' Count '''

    # 求图书的总量
    result = FilterBook.objects.aggregate(count=Count('id'))
    print(result)

    # 求每一本书的销售总量
    result = FilterBook.objects.annotate(count=Count('filterbookorder__id'))
    for r in result:
        print(r.name, r.count)

    return HttpResponse('Count')


def orm_filter14(request):
    ''' Max & Min '''

    # 求所有图书的最大销售额和最小销售额
    p_max = FilterBook.objects.aggregate(p_max=Max('filterbookorder__price'))
    print(p_max)
    p_min = FilterBook.objects.aggregate(p_min=Min('filterbookorder__price'))
    print(p_min)

    # 求每一本图书的最大销售额和最小销售额
    result = FilterBook.objects.annotate(p_max=Max('filterbookorder__price'))
    for r in result:
        print(r.name, r.p_max)

    result = FilterBook.objects.annotate(p_min=Min('filterbookorder__price'))
    for r in result:
        print(r.name, r.p_min)

    return HttpResponse('Max & Min')


def orm_filter15(request):
    ''' Sum '''

    # 求说有图书的总销售额
    result = FilterBook.objects.aggregate(sum=Sum('filterbookorder__price'))
    print(result)

    # 求每一本书的销售总额
    result = FilterBook.objects.annotate(sum=Sum('filterbookorder__price'))
    for r in result:
        print(r.name, r.sum)

    return HttpResponse('Sum')


def orm_filter16(request):
    ''' F 表达式 '''

    # 给多有书籍的价格增加10
    FilterBook.objects.update(price=F('price') + 10)

    # 查重价格和销售价格相同的书籍
    result = FilterBook.objects.filter(price=F('filterbookorder__price'))
    for r in result:
        print(r.name)

    return HttpResponse('F 表达式 ')


def orm_filter17(request):
    ''' Q 表达式 '''
    # 或操作
    # 获取评分大于9.8 或者 价格大于100 的书籍
    # 或者、或者、或者 重要的事情说三遍

    result = FilterBook.objects.filter(Q(rating__gt=9.8) | Q(price__gte=100))
    for r in result:
        print(r.name)
    # 与操作
    # 获取评分大于9.8 并且 价格大于100 的书籍
    # 并且、并且、并且 重要的事情说三遍

    result = FilterBook.objects.filter(Q(rating__gt=9.8) & Q(price__gte=100))
    for r in result:
        print(r)

    # 非操作
    # 获取价格大于100 并且图书名称不包含'j'的书籍
    # 不包含'j'、不包含'j'、不包含'j'
    result = FilterBook.objects.filter(Q(price__gte=100) & ~Q(name__contains='j'))
    for r in result:
        print(r.name)
    return HttpResponse('Q 表达式')


# ------------------ object 对象所属类原理分析 ------------------


def orm_filter18(request):
    ''' object对象所属类原理分析 '''

    # 查看objects到底代表的是什么对象
    print(type(FilterBook.objects))  # 使用type查看FilterBook是属于哪个类
    # 返回结果为 <class 'django.db.models.manager.Manager'>
    # 因此 FilterBook 是属于 Manager 类的

    # 查看 Manager 类
    # from django.db.models.manager import Manager

    '''
    Manager:
    
    class Manager(BaseManager.from_queryset(QuerySet)):
    pass
    
    1.Manage 的父类 BaseManager.from_queryset(QuerySet) 是动态生成的，
    2.是由 BaseManager 调用类方法 from_queryset 方法
    3.from_queryset 传递了一个参数 QuerySet
    4.这里的 QuerySet 是一个类
    
    '''

    # 查看 from_queryset 方法
    '''
    from_queryset 方法:
    
    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
        return type(class_name, (cls,), {
            '_queryset_class': queryset_class,
            **cls._get_queryset_methods(queryset_class),
        })
        
    1.此时的 cls 是 BaseManager，因此 cls.__name__='BaseManager'
    
    2.此时的 queryset_class 是 QuerySet，因此 class_name = 'BaseManagerFromQuerySet'
    
    3.'_queryset_class': queryset_class, ==> '_queryset_class':QuerySet
    
    4.cls._get_queryset_methods(queryset_class) ==> cls._get_queryset_methods(QuerySet)
    
    5.使用 _get_queryset_methods()方法 收集 QuerySet类 的方法和属性
    
    6.使用 type(class_name, (cls,), {...}) 动态的创建一个类:
    type(BaseManagerFromQuerySet, (BaseManager,), {'_queryset_class':QuerySet, cls._get_queryset_methods(QuerySet)})
    
    7.返回type()方法创建的类
    
    '''

    '''
    type方法动态创建一个类
    type(class_name, (cls,), {...})
    第一个参数为 创建的类的类名名称
    第二个参数为 要创建的类的父亲类
    第三个参数为 要创建的类的属性和方法
    '''

    # 查看 _get_queryset_methods()方法
    '''
    _get_queryset_methods()方法:
    
    @classmethod
    def _get_queryset_methods(cls, queryset_class):
        def create_method(name, method):
            def manager_method(self, *args, **kwargs):
                return getattr(self.get_queryset(), name)(*args, **kwargs)
            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__
            return manager_method

        new_methods = {}
        for name, method in inspect.getmembers(queryset_class, predicate=inspect.isfunction):
            # Only copy missing methods.
            if hasattr(cls, name):
                continue
            # Only copy public methods or methods with the attribute `queryset_only=False`.
            queryset_only = getattr(method, 'queryset_only', None)
            if queryset_only or (queryset_only is None and name.startswith('_')):
                continue
            # Copy the method onto the manager.
            new_methods[name] = create_method(name, method)
        return new_methods
        
        
        1.此时的 queryset_class 是 QuerySet
        
        2.inspect.getmembers(queryset_class, predicate=inspect.isfunction)获取所有成员(属性和方法):
        predicate=inspect.isfunction 表示只获取函数方法
        ==> inspect.getmembers(QuerySet, predicate=inspect.isfunction) 获取 QuerySet 的所有方法
        
        3.将 QuerySet 中的方法 放到 new_methods
        
        因此，这里 _get_queryset_methods()方法 是将 QuerySet的所有方法拷贝出来
    '''

    # 总结：objects 拥有 QuerySet 的所有方法

    return HttpResponse('objects')


# ------------------ QuerySet API 详解 ------------------


def queryset1(request):
    ''' exclude '''

    # 获取评分不小于9.8的书籍
    # 用Q表达式
    result = FilterBook.objects.filter(~Q(rating__lt=9.8))
    for book in result:
        print(book.name)

    # 使用 exclude 方法
    result = FilterBook.objects.exclude(rating__lt=9.8)
    for book in result:
        print(book.name)

    return HttpResponse('QuerySet API -- exclude')


def queryset2(request):
    ''' order_by '''

    # 通过价格排序
    result = FilterBook.objects.order_by('price')
    print(result)

    # 通过价格倒叙排序
    result = FilterBook.objects.order_by('-price')
    print(result)

    # 先通过价格倒叙排序，如果价格相同，再通过页数排序
    result = FilterBook.objects.order_by('-price', 'page')
    print(result)

    return HttpResponse('QuerySet API -- order_by')


def queryset3(request):
    ''' annotate '''

    # 给每一本书籍添加一个作者名
    result = FilterBook.objects.annotate(author_name=F('author__name'))
    # 通过这样的方式一次就可以查询出来，而如果使用book.author.name需要再进行一次查询
    for book in result:
        print(book.author_name)

    return HttpResponse('QuerySet API -- annotate')


def queryset4(request):
    ''' values '''

    result = FilterBook.objects.values('name', 'price')
    for book in result:
        print(book)

    result = FilterBook.objects.values('name', author_name=F('author__name'), publisher_name=F('publisher__name'))
    for book in result:
        print(book)

    return HttpResponse('QuerySet API -- values')


def queryset5(request):
    ''' values_list '''

    result = FilterBook.objects.values_list('name', 'page')
    print(result)

    result = FilterBook.objects.values_list('name')
    print(result)

    result = FilterBook.objects.values_list('name', flat=True)
    print(result)

    return HttpResponse('QuerySet API -- values_list')


def queryset6(request):
    ''' select_related '''

    result = FilterBook.objects.select_related('author', 'publisher')
    for book in result:
        print(book.author, book.publisher)

    return HttpResponse('QuerySet API -- select_related')


from django.db.models import Prefetch


def queryset7(request):
    ''' prefetch_related '''

    result = FilterBook.objects.prefetch_related('filterbookorder_set')
    for book in result:
        bookorders = book.filterbookorder_set.all()
        print(book.name)
        for order in bookorders:
            print(order.price)

    result = FilterBook.objects.prefetch_related('filterbookorder_set')
    for book in result:
        bookorders = book.filterbookorder_set.filter(price__gte=90)
        print(book.name)
        for order in bookorders:
            print(order.price)

    prefetch = Prefetch('filterbookorder_set', queryset=FilterBookOrder.objects.filter(price__gte=90))
    result = FilterBook.objects.prefetch_related(prefetch)
    for book in result:
        print(book.name)
        orders = book.filterbookorder_set.all()
        for order in orders:
            print(order.price)

    return HttpResponse('QuerySet API -- prefetch_related')


def queryset8(request):
    ''' defer & only '''

    # defer
    result = FilterBook.objects.defer('page')  # 将page过滤调

    for book in result:
        print(book.page)  # 如果再获取了已经过滤掉的字段，那么它就会去重新查询

    # only
    result = FilterBook.objects.only('page')  # 只获取page

    return HttpResponse('QuerySet API -- defer & only')


def queryset9(request):
    ''' get_or_create & bulk_create '''

    # get_or_create
    resutl = FilterPublish.objects.get_or_create(name='kurong')  # 数据库中有
    print(resutl)  # 结果：(< FilterPublish: kurong >, True)
    resutl = FilterPublish.objects.get_or_create(name='qinghua')  # 数据库中没有
    print(resutl)  # 结果：(< FilterPublish: qinghua >, False)

    # bulk_create
    resutl = FilterPublish.objects.bulk_create([
        FilterPublish(name='chenrong'),
        FilterPublish(name='ronggege'),
        FilterPublish(name='rong_ku')
    ])

    print(resutl)  # 结果：[<FilterPublish: chenrong>, <FilterPublish: ronggege>, <FilterPublish: rong_ku>]

    return HttpResponse('QuerySet API -- get_or_create & bulk_create')


def queryset10(request):
    ''' count、exists、distinct、update、delete、切片操作 '''

    # count
    result = FilterBook.objects.filter(filterbookorder__price__gt=90).count()
    print(result)  # 7

    # exists
    result = FilterBook.objects.filter(author__name='Kurong').exists()
    print(result)  # False

    # exists 效率比 count 高
    if FilterBook.objects.filter(author__name='Kurong').count() > 0:
        print(result)

    # exists 效率比 QuerySet 高
    if FilterBook.objects.filter(author__name='Kurong'):
        print(result)

    # distinct
    result = FilterBook.objects.filter(filterbookorder__price__gt=90).distinct()
    print(result)
    # <QuerySet [<FilterBook: python>, <FilterBook: linux>, <FilterBook: react>, <FilterBook: flask>, <FilterBook: javascript>]>

    # update
    result = FilterBook.objects.update(price=F('price') + 5)
    print(result)
    result = FilterPublish.objects.filter(pk=3).update(name='ku_rong')
    print(result)

    # delete
    # FilterPublish.objects.get(pk=1).delete()

    # 切片操作
    result = FilterPublish.objects.all()[:3]
    print(result)
    result = FilterPublish.objects.get_queryset()[:3]
    print(result)

    return HttpResponse('QuerySet API -- count、exists、distinct、update、delete、切片操作')


def queryset11(request):
    return HttpResponse('QuerySet API -- ')
