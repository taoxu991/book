from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.BigAutoField(primary_key=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    telephone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    avatar = models.FileField(verbose_name='头像', upload_to='avatar/',default='avatar/default.png')
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    def __str__(self):
        return self.username

class Book(models.Model):
    """
    书籍信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="书名",max_length=32)
    price = models.DecimalField(verbose_name="价格",max_digits=10,decimal_places=2)
    date = models.DateField(verbose_name="出版日期",default="2018-01-20")
    publish = models.ForeignKey(verbose_name="出版社",to="Publish",to_field="nid", on_delete=models.CASCADE)
    authors = models.ManyToManyField("Author")

    def __str__(self):
        return self.title

class Author(models.Model):
    """
    作者信息
    """
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,verbose_name="名字")
    sex = models.IntegerField(choices=((0,'男'),(1,'女'),),verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    phone = models.CharField(max_length=11,blank=True,unique=True,verbose_name='手机号码')

    class Meta:
        unique_together = [
            ('name','phone'),
        ]

    def __str__(self):
        return self.name

class Publish(models.Model):
    """
    出版社信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,verbose_name='名称')
    address = models.CharField(max_length=255,verbose_name='地址')

    def __str__(self):
        return self.title

# class Book2Author(models.Model):
#     """
#     书籍和作者对应表
#     """
#     nid = models.AutoField(primary_key=True)
#     book = models.ForeignKey(verbose_name="书籍",to='Book',to_field='nid')
#     author = models.ForeignKey(verbose_name="作者",to='Author',to_field='nid')
#
#     class Meta:
#         unique_together = [
#             ('book','author'),
#         ]
#
#     def __str__(self):
#         return "%s --> %s" %(self.book,self.author)