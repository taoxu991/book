from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.http import JsonResponse
from book_app.form import *
from django.contrib.auth.decorators import login_required
from book_app.page import *
from book import settings
from book_app import models as hmodels
from book_app import model_form as hmform


# 生成动态验证码
def get_valid_img(request):
    """
    生成动态验证码
    """
    from PIL import Image,ImageDraw,ImageFont
    import random
    from io import BytesIO

    def get_random_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    def get_random_char():
        random_num = str(random.randint(0,9))
        random_upper_alph = chr(random.randint(65,90))
        random_lowwer_alph = chr(random.randint(97,122))
        random_char = random.choice([random_num,random_lowwer_alph,random_upper_alph])
        return random_char
    image = Image.new(mode='RGB',size=(260,40), color=get_random_color())
    draw = ImageDraw.Draw(image,mode='RGB')
    font = ImageFont.truetype('book_app/static/kumo.ttf',32)
    valid_code_str = ''
    for i in range(1,6):
        char = get_random_char()
        valid_code_str += char
        draw.text([i*40,5],char,get_random_color(),font=font)
    f = BytesIO()
    image.save(f,'png')
    data = f.getvalue()
    print(valid_code_str)
    request.session['valid_code_str'] = valid_code_str
    return HttpResponse(data)

def index(request):
    return redirect('/manage/list/book/')


# 登出
@login_required
def log_out(request):
    auth.logout(request)
    return redirect('/login/')


# 登录
def log_in(request):
    if request.is_ajax():
        loginForm = LoginForm(request,request.POST)
        loginResponse = {'user':None,'error_msg':''}
        if loginForm.is_valid():
            user = auth.authenticate(username=loginForm.cleaned_data.get('user'),password=loginForm.cleaned_data.get('pwd'))
            if user:
                auth.login(request,user)
                loginResponse['user'] = user.username
            else:
                loginResponse['error_msg'] = {'pwd':['密码错误！']}
        else:
            loginResponse['error_msg'] = loginForm.errors
        return JsonResponse(loginResponse)
    loginForm = LoginForm(request)
    next_url = request.GET.get("next", '/index/')
    return render(request, 'login.html', {'loginForm': loginForm,'next_url':next_url})


# 管理员注册
def register(request):
    if request.is_ajax():
        regForm = RegForm(request,request.POST)
        regResponse = {'user': None, 'errors': None}
        if regForm.is_valid():
            # 注册
            data = regForm.cleaned_data
            user = data.get('user')
            pwd = data.get('pwd')
            email = data.get('email')
            avatar_img = request.FILES.get('file_img')
            if not avatar_img:
                UserInfo.objects.create_user(username=user,password=pwd,email=email)
            else:
                UserInfo.objects.create_user(username=user, password=pwd, email=email,avatar=avatar_img)
            regResponse['user'] = user
        else:
            regResponse['errors'] = regForm.errors

        return JsonResponse(regResponse)
    regForm = RegForm(request)
    return render(request, 'register.html', {'regForm': regForm})


# 增加图书、出版社、作者
@login_required
def add_handle(request, model_type):
    try:
        str_model_form = getattr(hmform, model_type.capitalize() + "ModelForm")
        if request.method == 'POST':
            model_form = str_model_form(request.POST)
            if model_form.is_valid():
                model_form.save(commit=True)
                return redirect('/manage/list/%s' % model_type)
        else:
            model_form = str_model_form()
            return render(request, '%s_add.html' % model_type, {'model_form': model_form})
    except AttributeError:
        return redirect('/index/')


# 查看图书、出版社、作者信息
@login_required
def info_handle(request, model_type, nid):
    try:
        str_model = getattr(hmodels, model_type.capitalize())
        if request.method == 'GET':
            obj = str_model.objects.get(nid=nid)
            if model_type != 'book':
                current_page = int(request.GET.get("page", 1))
                if model_type == 'author':
                    book_all = obj.book_set.all().order_by('nid')
                elif model_type == 'publish':
                    book_all = hmodels.Book.objects.filter(publish=obj).order_by('nid')
                paginator = CustomPagination(current_page, '/manage/info/%s/%s' % (model_type, nid), book_all,
                                             settings.PAGE_ROW_NUM)
                return render(request, '%s_info.html' % model_type,
                              {'obj': obj, 'book_list': paginator.res_list, 'page_html': paginator.html})
            else:
                model_form = hmform.BookModelForm(instance=obj)
                return render(request, 'book_info.html', {'model_form': model_form, 'obj': obj})
    except AttributeError:
        return redirect('/index/')


# 修改图书、出版社、作者
@login_required
def update_handle(request, model_type, nid):
    try:
        str_model = getattr(hmodels, model_type.capitalize())
        str_model_form = getattr(hmform, model_type.capitalize() + "ModelForm")
        if request.method == 'GET':
            obj = str_model.objects.get(nid=nid)
            model_form = str_model_form(instance=obj)
            return render(request, '%s_update.html' % model_type,
                          {'model_form': model_form, 'obj': obj})
        elif request.method == 'POST':
            obj = str_model.objects.filter(nid=nid).first()
            model_form = str_model_form(request.POST, instance=obj)
            if model_form.is_valid():
                model_form.save()
            return redirect('/manage/info/%s/%s' % (model_type, nid))
    except AttributeError:
        return redirect('/index/')


# 删除图书、出版社、作者
@login_required
def delete_handle(request, model_type):
    deleteResponse = {'nid': None}
    try:
        str_model = getattr(hmodels, model_type.capitalize())
        if request.is_ajax():
            nid = request.POST.get('nid')
            res = str_model.objects.filter(nid=nid).delete()
            if res:
                deleteResponse['nid'] = nid
    except AttributeError:
        pass
    return JsonResponse(deleteResponse)


# 图书表、出版社表、作者表
@login_required
def list_handle(request, model_type):
    try:
        str_model = getattr(hmodels, model_type.capitalize())
        current_page = int(request.GET.get("page", 1))
        book_all = str_model.objects.all().order_by('nid')
        paginator = CustomPagination(current_page, "/manage/list/%s/" % model_type, book_all, settings.PAGE_ROW_NUM)
        list_name = '%s_list' % model_type
        return render(request, '%s.html' % model_type, {list_name: paginator.res_list, 'page_html': paginator.html})
    except AttributeError:
        return redirect('/index/')




