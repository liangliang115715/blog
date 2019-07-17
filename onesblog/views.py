from django.shortcuts import render
from django.urls import reverse
from screen import models,pagination
# Create your views here.
def onesindex(request,*args,**kwargs):
    user_id =  request.COOKIES.get('cookie_user', None)
    if user_id:
        user = models.Users.objects.get(uid=int(user_id))
        blog = models.Blog.objects.get(user_id=int(user_id))
    else:
        blog = models.Blog.objects.get(surfix=kwargs['type'])

    artical_sort_list = models.Articals_sort.objects.filter(Fk=blog.bid)
    artical_lable_list = models.Articals_lable.objects.filter(Fk=blog.bid)
    base_url = '/onesindex/%s/'%blog.surfix

    if 'type' in kwargs.keys():
        type = kwargs['type']
        type_id = kwargs['type_id']
        conditions = {'blog':blog.bid}
        conditions[type] = type_id
        filtered_articals = models.Articals.objects.filter(**conditions)
    else:
        filtered_articals =models.Articals.objects.filter(blog_id=blog.bid)
    data_count = filtered_articals.count()
    page_obj = pagination.Pagination(request.GET.get('p'), data_count)
    page_str = page_obj.page_str(base_url)
    artical_list = filtered_articals.order_by('-ctime')[page_obj.start:page_obj.end]

    return render(request,'onesindex.html',locals())

