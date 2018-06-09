from django.forms import ModelForm
from django.forms import widgets as wid
from django.forms import fields as fld
from book_app import models

class BookModelForm(ModelForm):
    class Meta:
        model = models.Book
        fields = "__all__"
        # fields = ['name','sex','age','phone']
        # exclude = ['username',]
        # error_messages = {
        #     "username": {'required':'用户名不能为空'}
        # }
        widgets = {
            "title":wid.TextInput(attrs={'class': "form-control" ,'placeholder': '书名'}),
            'price':wid.NumberInput(attrs={'class': "form-control" ,'placeholder': '价格'}),
            'date':wid.DateInput(attrs={'class': "form-control" ,'placeholder': '出版日期'}),
            'publish':wid.Select(attrs={'class': "form-control" ,'placeholder': '出版社'}),
            'authors':wid.SelectMultiple(attrs={'class': "form-control" ,'placeholder': '作者'}),
        }
        labels = {
            'authors':'作者'
        }
        # help_texts = {
        #     'username': '别瞎写，瞎写打你哦'
        # }
        #
        # field_classes = {
        #     'username': fld.EmailField
        # }

class AuthorModelForm(ModelForm):
    class Meta:
        model = models.Author
        fields = ['nid','name', 'sex', 'age', 'phone']
        # exclude = ['username',]
        # error_messages = {
        #     "username": {'required':'用户名不能为空'}
        # }
        widgets = {
            "nid": wid.NumberInput(attrs={'class': "form-control", 'placeholder': '序号'}),
            "name": wid.TextInput(attrs={'class': "form-control", 'placeholder': '姓名'}),
            'sex': wid.Select(attrs={'class': "form-control", 'placeholder': '性别'}),
            'age': wid.NumberInput(attrs={'class': "form-control", 'placeholder': '年龄'}),
            'phone': wid.Input(attrs={'class': "form-control", 'placeholder': '手机'}),
        }

class PublishModelForm(ModelForm):
    class Meta:
        model = models.Publish
        fields = ['title','address']
        # exclude = ['username',]
        # error_messages = {
        #     "username": {'required':'用户名不能为空'}
        # }
        widgets = {
            "title": wid.TextInput(attrs={'class': "form-control", 'placeholder': '名称'}),
            "address": wid.TextInput(attrs={'class': "form-control", 'placeholder': '地址'}),
        }