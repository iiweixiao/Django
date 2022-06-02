from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    # 帖子状态选项，后面会用到
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    # 帖子标题，CharField数据库中会转换为VARCHAR
    title = models.CharField(max_length=250)
    # 简短的标记
    # slug指有效URL的一部分，能使URL更加清晰易懂。
    # 比如有这样一篇文章，标题是"13岁的孩子"，
    # 它的 URL 地址是"/posts/13-sui-de-hai-zi"，后面这一部分便是 slug 。
    # 通过它构建有较好外观，SEO友好的URL
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    # 作者，外键
    # 一个作者可以有多篇帖子
    # 当作者被删除，相应的帖子也会被删除
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    # 正文，TextField会转换为TEXT
    body = models.TextField()
    # 发布日期，timezone.now：以时区格式返回当前的时间
    publish = models.DateTimeField(default=timezone.now)
    # 创建时间，auto_now_add：当「创建」某个对象时，日期将被自动保存
    created = models.DateTimeField(auto_now_add=True)
    # 最后一次更新时间，auto_now：当「保存」某对象时候，日期将被自动保存
    update = models.DateTimeField(auto_now=True)
    # 帖子的状态，choices选择STATUS_CHOICES元祖中的某一个状态
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        # 对publish字段进行排列，由「-」确定为降序
        ordering = ('-publish',)

    def __str__(self):
        # 增加人们可读对象表达方式
        return self.title
