from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

@register.simple_tag
def display_all_comments(comment_obj,s=''):
    for obj in comment_obj.reply.all():
        ctime = obj.ctime
        username = obj.user.username
        content = obj.content
        s=s + '<p class="fbtime"><span>%s</span>%s --> %s </p><p class="fbinfo">%s</p>'%(ctime,username,comment_obj.user.username,content)
        if obj.reply.all():
            s = display_all_comments(obj,s)
    return mark_safe(s)



