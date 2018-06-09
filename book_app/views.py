from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.http import JsonResponse
from book_app.form import *
from book_app.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from book_app.model_form import *
from django.contrib.auth.decorators import login_required


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
    return redirect('/book/')

@login_required
def log_out(request):
    auth.logout(request)
    return redirect('/login/')

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
    return render(request,'login.html',{'loginForm': loginForm,'next_url':next_url})

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

@login_required
def book_list(request):
    page = request.GET.get("page")
    if page is None:
        page = "1"
    book_all = Book.objects.all().order_by('nid')
    paginator = Paginator(book_all, 10)
    if page.isdigit():
        current_page = int(page)
    try:
        book_list = paginator.page(page)
    except EmptyPage:
        current_page = paginator.num_pages
        book_list = paginator.page(current_page)

    except PageNotAnInteger:
        book_list = paginator.page(1)
        current_page = 1
    return render(request, 'book.html', locals())

@login_required
def publish_list(request):
    page = request.GET.get("page")
    if page is None:
        page = "1"
    publish_all = Publish.objects.all().order_by('nid')
    paginator = Paginator(publish_all, 10)
    if page.isdigit():
        current_page = int(page)
    try:
        publish_list = paginator.page(page)
    except EmptyPage:
        current_page = paginator.num_pages
        publish_list = paginator.page(current_page)

    except PageNotAnInteger:
        publish_list = paginator.page(1)
        current_page = 1
    return render(request, 'publish.html', locals())

@login_required
def author_list(request):
    page = request.GET.get("page")
    if page is None:
        page = "1"
    author_all = Author.objects.all().order_by('nid')
    paginator = Paginator(author_all, 10)
    if page.isdigit():
        current_page = int(page)
    try:
        author_list = paginator.page(page)
    except EmptyPage:
        current_page = paginator.num_pages
        author_list = paginator.page(current_page)

    except PageNotAnInteger:
        author_list = paginator.page(1)
        current_page = 1
    return render(request, 'author.html', locals())

@login_required
def author_add(request):
    if request.method == 'POST':
        model_form = AuthorModelForm(request.POST)
        if model_form.is_valid():
            model_form.save(commit=True)
            return redirect('/author/')
    else:
        model_form = AuthorModelForm()
        return render(request,'author_add.html',{'model_form':model_form})

@login_required
def book_add(request):
    if request.method == 'POST':
        model_form = BookModelForm(request.POST)
        if model_form.is_valid():
            model_form.save(commit=True)
            return redirect('/book/')
    else:
        model_form = BookModelForm()
        return render(request,'book_add.html',{'model_form':model_form})

@login_required
def publish_add(request):
    if request.method == 'POST':
        model_form = PublishModelForm(request.POST)
        if model_form.is_valid():
            model_form.save(commit=True)
            return redirect('/publish/')
    else:
        model_form = PublishModelForm()
        return render(request,'publish_add.html',{'model_form':model_form})

@login_required
def book_info(request,nid):
    if request.method == 'GET':
        obj = Book.objects.get(nid=nid)
        model_form = BookModelForm(instance=obj)

        return render(request, 'book_info.html', {'model_form': model_form,'obj':obj})

@login_required
def book_update(request,nid):
    if request.method == 'GET':
        obj = Book.objects.get(nid=nid)
        model_form = BookModelForm(instance=obj)
        return render(request, 'book_update.html', {'model_form': model_form,'obj':obj})
    elif request.method == 'POST':
        obj = Book.objects.filter(nid=nid).first()
        model_form = BookModelForm(request.POST,instance=obj)
        if model_form.is_valid():
            model_form.save()
        return redirect('/manage/book_info/%s' % nid)

@login_required
def book_delete(request):
    if request.is_ajax():
        nid = request.POST.get('nid')
        deleteResponse = {'nid':None,'error_msg':''}
        res = Book.objects.filter(nid=nid).delete()
        if res:
            deleteResponse['nid'] = nid
        return JsonResponse(deleteResponse)

@login_required
def author_info(request,nid):
    if request.method == 'GET':
        obj = Author.objects.get(nid=nid)
        model_form = AuthorModelForm(instance=obj)
        page = request.GET.get("page")
        if page is None:
            page = "1"
        book_all = obj.book_set.all().order_by('nid')
        paginator = Paginator(book_all, 10)
        if page.isdigit():
            current_page = int(page)
        try:
            book_list = paginator.page(page)
        except EmptyPage:
            current_page = paginator.num_pages
            book_list = paginator.page(current_page)

        except PageNotAnInteger:
            book_list = paginator.page(1)
            current_page = 1
        return render(request, 'author_info.html', locals())

@login_required
def author_update(request,nid):
    if request.method == 'GET':
        obj = Author.objects.get(nid=nid)
        model_form = AuthorModelForm(instance=obj)
        return render(request, 'author_update.html', {'model_form': model_form,'obj':obj})
    elif request.method == 'POST':
        obj = Author.objects.filter(nid=nid).first()
        model_form = AuthorModelForm(request.POST,instance=obj)
        if model_form.is_valid():
            model_form.save()
        return redirect('/manage/author_info/%s' % nid)

def author_delete(request):
    if request.is_ajax():
        nid = request.POST.get('nid')
        deleteResponse = {'nid':None,'error_msg':''}
        res = Author.objects.filter(nid=nid).delete()
        if res:
            deleteResponse['nid'] = nid
        return JsonResponse(deleteResponse)

@login_required
def publish_info(request,nid):
    if request.method == 'GET':
        obj = Publish.objects.get(nid=nid)
        model_form = PublishModelForm(instance=obj)

        page = request.GET.get("page")
        if page is None:
            page = "1"
        book_all = Book.objects.filter(publish=obj).order_by('nid')
        paginator = Paginator(book_all, 10)
        if page.isdigit():
            current_page = int(page)
        try:
            book_list = paginator.page(page)
        except EmptyPage:
            current_page = paginator.num_pages
            book_list = paginator.page(current_page)

        except PageNotAnInteger:
            book_list = paginator.page(1)
            current_page = 1

        return render(request, 'publish_info.html', locals())

@login_required
def publish_update(request,nid):
    if request.method == 'GET':
        obj = Publish.objects.get(nid=nid)
        model_form = PublishModelForm(instance=obj)
        return render(request, 'publish_update.html', {'model_form': model_form,'obj':obj})
    elif request.method == 'POST':
        obj = Publish.objects.filter(nid=nid).first()
        model_form = PublishModelForm(request.POST,instance=obj)
        if model_form.is_valid():
            model_form.save()
        return redirect('/manage/publish_info/%s' % nid)

@login_required
def publish_delete(request):
    if request.is_ajax():
        nid = request.POST.get('nid')
        deleteResponse = {'nid':None,'error_msg':''}
        res = Publish.objects.filter(nid=nid).delete()
        if res:
            deleteResponse['nid'] = nid
        return JsonResponse(deleteResponse)

