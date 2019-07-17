from django.forms import ModelForm,ValidationError
from django import forms
from screen import models
class LoginForm(ModelForm):

    # def __new__(cls, *args, **kwargs):
    #
    #     for field_name,field_obj in  cls.base_fields.items():
    #         field_obj.widget.attrs.update({'class': 'form-control'})
    #
    #
    #     return ModelForm.__new__(cls)

    class Meta:
        model = models.Users
        fields = ['username','pwd']
        # widgets = {'class': "form-control"}

class RegistForm(ModelForm):

    # def __new__(cls, *args, **kwargs):
    #     for field_name,field_obj in  cls.base_fields.items():
    #         field_obj.widget.attrs.update({'class': "form-control"})
    #     return ModelForm.__new__(cls)
    class Meta:
        model = models.Users
        fields = '__all__'
        exclude = ['img']


