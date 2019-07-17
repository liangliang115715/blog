from django.db import models
import time
# Create your models here.
class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField("用户", max_length=16)
    pwd = models.CharField("用户密码", max_length=16)
    email = models.EmailField("用户邮箱", max_length=32)
    img = models.ImageField("用户头像", upload_to="static/upload/users",blank=True,null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "用户"


class Blog(models.Model):
    bid = models.AutoField(primary_key=True)
    surfix = models.CharField("blog后缀", max_length=32)
    title = models.CharField("博客标题", max_length=32)
    summary = models.TextField("博客简介", max_length=120)
    user = models.OneToOneField("Users", on_delete=models.CASCADE, verbose_name="博客主人")

    def __str__(self):
        return self.surfix

    class Meta:
        verbose_name_plural = "个人博客"


class Fans(models.Model):
    star = models.IntegerField("明星ID")
    fans = models.IntegerField("粉丝ID")

    def __str__(self):
        return self.id

    class Meta:
        verbose_name_plural = "互粉"


# 知识库

class Articals_sort(models.Model):
    caption = models.CharField("类名", max_length=16)
    Fk = models.ForeignKey("Blog", on_delete=models.CASCADE, verbose_name="博主")

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name_plural = "文章分类"


class Articals_lable(models.Model):
    caption = models.CharField("标签", max_length=16)
    Fk = models.ForeignKey("Blog", on_delete=models.CASCADE, verbose_name="博主")

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name_plural = "文章标签"


class Articals(models.Model):
    title = models.CharField("文章标题", max_length=32)
    summary = models.CharField("文章简介", max_length=100)
    detail = models.TextField("文章内容", max_length=1000)
    sort = models.ForeignKey("Articals_sort", on_delete=models.CASCADE, verbose_name="文章类型")
    blog = models.ForeignKey("Blog", on_delete=models.CASCADE, verbose_name="文章所属博客")
    ctime = models.DateTimeField("上传时间", auto_now=True,null=True)
    type_choices = [
        (1, "Python"),
        (2, "Linux"),
        (3, "OpenStack"),
        (4, "GoLang"),
    ]
    article_type_id = models.IntegerField(choices=type_choices, default=None)

    lable = models.ManyToManyField(
        to="Articals_lable",
        through="AL_reletion",
        through_fields=("Aid", "Lid")
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "文章"


class AL_reletion(models.Model):
    Aid = models.ForeignKey("Articals", on_delete=models.CASCADE, verbose_name="文章ID")
    Lid = models.ForeignKey("Articals_lable", on_delete=models.CASCADE, verbose_name="标签ID")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "文章标签关系表"


class Attribute(models.Model):
    Aid = models.ForeignKey("Articals", on_delete=models.CASCADE, verbose_name="文章ID")
    Uid = models.ForeignKey("Users", on_delete=models.CASCADE, verbose_name="用户ID")
    attribute_type_choices = ((0,"赞"),(1,"踩"))
    attribute = models.SmallIntegerField("赞与踩",choices=attribute_type_choices)

    def __str__(self):
        return self.id

    class Meta:
        unique_together = ["Aid", "Uid"]
        verbose_name_plural = "赞踩表"


class Comments(models.Model):
    user = models.ForeignKey("Users", on_delete=models.CASCADE, verbose_name="用户")
    articls = models.ForeignKey("Articals", on_delete=models.CASCADE, verbose_name="评论的文章",related_name='comments')
    content = models.TextField("评论内容", max_length=1000)
    ctime = models.DateTimeField("评论时间", auto_now=True, null=True)
    Interaction = models.ForeignKey(
        to='self', to_field='id', null=True, on_delete=models.CASCADE, verbose_name="互动",blank=True,
        related_name='reply'
    )

    def __str__(self):
        return '%s 评论席:%s楼'%(self.articls.title,self.id)

    class Meta:
        verbose_name_plural = "评论"


class Manager(models.Model):
    name = models.CharField("处理者", max_length=16)
    weight = models.IntegerField("权限级别")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "管理员"


class Kill(models.Model):
    manager = models.ForeignKey("Manager", on_delete=models.CASCADE, verbose_name="处理人员")
    method = models.OneToOneField("Trouble", on_delete=models.CASCADE, verbose_name="解决方案", blank=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name_plural = "报障处理"


class Trouble(models.Model):
    maker = models.ForeignKey("Users", on_delete=models.CASCADE, verbose_name="报障用户")
    ctime = models.DateTimeField("创建时间", auto_now=True, null=True)
    title = models.CharField("报障标题", max_length=32)
    detail = models.TextField("详细描述", max_length=2000)
    status = models.NullBooleanField("处理状态", default=0)
    method = models.ForeignKey("Kill", on_delete=models.CASCADE, blank=True, verbose_name="解决方案")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "报障单"
