from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.forms.models import model_to_dict
from screen import models,Forms,pagination
from django.urls import reverse
import json,chunk


# Create your views here.

def index(request,*args,**kwargs):
    user = request.COOKIES.get('cookie_user', None)
    if user:
        user = models.Users.objects.get(uid=int(user))

    article_type_list = models.Articals.type_choices
    if kwargs:
        article_type_id = int(kwargs["article_type_id"])
        base_url = reverse("home", kwargs=kwargs,args=args)
    else:
        article_type_id = None
        base_url = '/'

    data_count = models.Articals.objects.filter(**kwargs).count()
    page_obj = pagination.Pagination(request.GET.get('p'), data_count)
    if article_type_id:
        artical_list = models.Articals.objects.filter(**kwargs).order_by('-id')[page_obj.start:page_obj.end]
    else:
        artical_list=models.Articals.objects.all().order_by('-ctime')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(base_url)

    return render(request, 'index.html',locals())

def artical_detail(request,*args,**kwargs):
    artical_id = kwargs['artical_id']
    artical_obj = models.Articals.objects.get(id=artical_id)
    comment_obj_list = models.Comments.objects.filter(articls=artical_id)

    blog = artical_obj.blog
    user = blog.user

    artical_sort_list = models.Articals_sort.objects.filter(Fk=blog.bid)
    artical_lable_list = models.Articals_lable.objects.filter(Fk=blog.bid)


    return render(request,'artical_detail.html',locals())


def ckediter_uploadimg(request):
    t =request.FILES
    if t:
        with open('/static/upload/user_comment_img'+t.name,'wb') as f:
            for i in t.chunks:
                f.write(i)
    dict ={
        "uploaded": 1,
        "fileName":t.name ,
        "url": "/static/upload/user_comment_img"+t.name,
    }

    return JsonResponse(dict)

def login(request):
    msg = None
    if request.method == "POST":
        username=request.POST.get('username')
        pwd = request.POST.get('pwd')
        try:
            user_obj = models.Users.objects.get(username=username,pwd=pwd)
            response = redirect('home')
            response.set_cookie('cookie_user', user_obj.uid, 3600)
            return response
        except Exception:
            msg = '用户名或密码错误，请重新登录!'
    loginForm = Forms.LoginForm()
    registForm = Forms.RegistForm()
    response_msg = request.GET.get('response_msg', None)
    if response_msg:
        response_msg=json.loads(response_msg)
    return render(request, 'login.html',locals())


def regist(request):
    response_msg = {'status': False, 'error_msg': None}
    if request.method == 'POST':
        registForm = Forms.RegistForm(data=request.POST)
        if registForm.is_valid():
            # models.Users.objects.create(**registForm.cleaned_data)
            registForm.save()
            response_msg['status']=True

    msg = json.dumps(response_msg)
    return redirect('/login/?response_msg=%s'%msg)


def logout(request):
    response = redirect('home')
    response.delete_cookie('cookie_user')
    return response

def regBlog(request,*args,**kwargs):
    user = models.Users.objects.get(uid=int(kwargs['user']))
    if request.method == 'GET':
        regBlogForm = Forms.RegBlogForm(initial={'user':user})
        regBlogForm.Meta.current_user = user
    elif request.method == 'POST':
        regBlogForm = Forms.RegBlogForm(request.POST)
        if regBlogForm.is_valid():
            regBlogForm.save()
            return redirect('home')

    return render(request,'regBlog.html',locals())
