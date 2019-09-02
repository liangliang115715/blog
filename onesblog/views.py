from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from screen import models, pagination
import json, time, requests, chunk, os
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def onesindex(request, *args, **kwargs):
    user_id = request.COOKIES.get('cookie_user', None)
    if user_id:
        user = models.Users.objects.get(uid=int(user_id))
        blog = models.Blog.objects.get(user_id=int(user_id))
    else:
        blog = models.Blog.objects.get(surfix=kwargs['type'])

    artical_sort_list = models.Articals_sort.objects.filter(Fk=blog.bid)
    artical_lable_list = models.Articals_lable.objects.filter(Fk=blog.bid)
    base_url = '/onesindex/%s/' % blog.surfix

    if 'type' in kwargs.keys():
        type = kwargs['type']
        type_id = kwargs['type_id']
        conditions = {'blog': blog.bid}
        conditions[type] = type_id
        filtered_articals = models.Articals.objects.filter(**conditions)
    else:
        filtered_articals = models.Articals.objects.filter(blog_id=blog.bid)
    data_count = filtered_articals.count()
    page_obj = pagination.Pagination(request.GET.get('p'), data_count)
    page_str = page_obj.page_str(base_url)
    artical_list = filtered_articals.order_by('-ctime')[page_obj.start:page_obj.end]

    return render(request, 'onesindex.html', locals())


def PostAvatar(request, *args, **kwargs):
    msg = {'status': False, 'error': None, 'posted_img_name': []}
    uid = request.headers.get('uid', None)
    user = models.Users.objects.get(uid=uid) if uid else None
    print('user>>>>>', user)
    # get请求表示点击了提交  当有前端有图片时post_ensure=True
    if request.method == 'GET':
        post_ensure = request.GET.get('post_ensure')
        if post_ensure == 'None':
            if user:
                print(str(user.img))
                os.remove(str(user.img))
                user.img = None
                user.save()
            msg['error'] = '头像获取失败'
        elif post_ensure == 'True':
            msg['status'] = '头像上传成功！'
    if request.method == 'POST':
        if request.FILES:
            img_obj = request.FILES.getlist('file')[0]
            print(img_obj)
            if user:
                user.img = img_obj
                user.save()

    return HttpResponse(json.dumps(msg))


@csrf_exempt
def ChangeAvatar(request, *args, **kwargs):
    img_obj = None
    submit_img_obj = None
    if request.method == 'POST':
        if request.FILES:
            img_obj = request.FILES.get('image')
            submit_img_obj = request.FILES.get('Avatarfile')
        if submit_img_obj:
            bid = request.POST.get('bid', None)
            print(submit_img_obj)
            blog = models.Blog.objects.get(bid=bid)
            surfix = blog.surfix
            blog.user.img = submit_img_obj
            blog.user.save()
            return redirect('/index/%s'%surfix)
        elif img_obj:
            msg = {'status': False, 'error': None, 'img_src': None}
            if img_obj.size > 10000000:
                msg['error'] = '图片超过指定大小！'
            else:
                with open('static/upload/changeAvatar/' + str(img_obj.name), 'wb') as f:
                    for i in img_obj.chunks():
                        f.write(i)
                msg['img_src'] = '/static/upload/changeAvatar/' + str(img_obj.name)
                msg['status'] = 'true'
            return HttpResponse(json.dumps(msg))
        else:
            return HttpResponse(json.dumps({"error":"啥情况？"}))
