from django.forms import ModelForm,ValidationError
from django import forms
from screen import models
class LoginForm(ModelForm):

    class Meta:
        model = models.Users
        fields = ['username','pwd']


class RegistForm(ModelForm):

    class Meta:
        model = models.Users
        fields = '__all__'
        exclude = ['img']

class RegBlogForm(ModelForm):

    def __new__(cls, *args, **kwargs):

        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({"class": "form-control"})

            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs.update({"disabled": "true"})


        return ModelForm.__new__(cls)

    def clean(self):
        if self.errors:
            raise ValidationError(("Please fix errors befo re-submit"))
        # 防止篡改提交对象
        if self.cleaned_data['user'] != self.Meta.current_user:
            self.add_error('user','小伙儿想干啥？')
    class Meta:
        model=models.Blog
        fields='__all__'
        readonly_fields=['user']
        current_user = None





