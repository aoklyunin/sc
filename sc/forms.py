# -*- coding: utf-8 -*-
import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import FileInput

from sc.models import Submission, CreativeType
from users.models import ScUser


class UserForm(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z_]*$',
                                  'Это поле может содержать только латинские буквы, '
                                  'числа и символ _.')

    username = forms.CharField(widget=forms.TextInput(
        attrs=
        {'class': "form-control",
         'placeholder': "Логин",
         'required': '',
         'autofocus': ''}),
        max_length=20,
        min_length=3,
        required=True,
        validators=[alphanumeric])
    password = forms.CharField(widget=forms.PasswordInput(
        attrs=
        {'class': "form-control",
         'placeholder': "Пароль",
         'required': ''}),
        min_length=4,
        required=True)
    rep_password = forms.CharField(widget=forms.PasswordInput(
        attrs=
        {'class': "form-control",
         'placeholder': "Повторите пароль",
         'required': ''}),
        min_length=4,
        required=True)

    keyWord = forms.CharField(widget=forms.TextInput(
        attrs=
        {'class': "form-control",
         'placeholder': "Ключ для регистрации",
         'required': '',
         'autofocus': ''}),
        max_length=12,
        min_length=3,
        required=True,
        validators=[alphanumeric])

    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'id': "first_name",
               'type': "text"}),
        min_length=1,
        max_length=12,
        required=False
    )

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'id': "last_name",
               'type': "text"}),
        min_length=1,
        max_length=12,
        required=False
    )

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': "form-control",
               'id': "email",
               'type': "text"}),
        required=False
    )

    about_text = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control",
               'rows': "4",
               'id': 'aboutField',
               }),
        required=False
    )

    homepage = forms.CharField(widget=forms.URLInput(
        attrs={'class': "form-control",
               'id': "homepage"}),
        required=False
    )

    instagram = forms.CharField(widget=forms.URLInput(
        attrs={'class': "form-control",
               'id': "instagram",
               'type': "text"}),
        required=False,
        max_length=100
    )

    fb = forms.CharField(widget=forms.URLInput(
        attrs={'class': "form-control",
               'id': "fb",
               'type': "text"}),
        required=False,
        max_length=100
    )

    vk = forms.CharField(widget=forms.URLInput(
        attrs={'class': "form-control",
               'id': "vk",
               'type': "text"}),
        required=False,
        max_length=100
    )

    telegram = forms.CharField(widget=forms.URLInput(
        attrs={'class': "form-control",
               'id': "telegram",
               'type': "text"}),
        required=False,
        max_length=100
    )
    tel = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'id': "tel",
               'type': "text"}),
        required=False,
        max_length=100
    )

    youtube = forms.CharField(widget=forms.URLInput(
        attrs={'class': "form-control",
               'id': "youtube",
               'type': "text"}),
        required=False,
        max_length=100
    )

    date = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control",
               'id': "date",
               "placeholder": "14/12/1995"}),
        required=False,
        input_formats=["%d/%m/%Y"]
    )

    avatar = forms.FileInput(attrs={'required': False, 'class': 'form-control', 'enctype': 'multipart/form-data'}),

    class Meta:
        model = ScUser
        fields = ('first_name', 'last_name', 'email', 'date',
                  'about_text', 'tel', 'avatar',
                  'homepage', 'instagram', 'fb', 'vk', 'telegram', 'youtube')

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ProfileForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['avatar'].required = False


class SubmissionForm(forms.ModelForm):
    link_type = -1

    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': "Заголовок поста"}),
        required=True, min_length=1, max_length=250)

    url = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': "(Необязательно) http:///www.example.com"}),
        required=False)

    ctp = forms.ModelMultipleChoiceField(required=False, queryset=CreativeType.objects.all())
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "form-control",
            'rows': "3",
            'id': 'postField',
            'placeholder': "(Необязательно) текст"}),
        max_length=5000,
        required=False)

    regard = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': "form-control",
            "placeholder": "1000"}),
        required=False)

    stoDate = forms.DateField(widget=forms.DateInput(
        attrs={
            'class': "form-control",
            "placeholder": "20/01/2018"}),
        required=False,
        input_formats=["%d/%m/%Y"]
    )

    image = forms.FileInput(attrs={'required': False, 'class': 'form-control', 'enctype': 'multipart/form-data'}),

    def clean_url(self):
        url = self.cleaned_data['url']
        # soundcloud
        match = re.search(r'src="https:\/\/w.soundcloud.com\/[\'"]?([^\'" >]+)"', url)
        if match:
            url = match.group(0)[5:-1]
            self.link_type = Submission.LINK_TYPE_SOUNDCLOUND
        else:
            # youtube
            match = re.search(r'<[\'"]?([^\'" >]+)youtube([^\'" >]+)>', url)
            if match:
                url = match.group(0).replace("watch?v=", "embed/")[1:-1]
                self.link_type = Submission.LINK_TYPE_YOUTUBE
            else:
                match = re.search(r'[\'"]?([^\'" >]+).([^\'" >]+)', url)
                if match:
                    self.link_type = Submission.LINK_TYPE_NOT_PROCESSED
                    url = match.group(0)
                else:
                    if url != '':
                        raise ValidationError("Не удалось расшифровать ссылку")
        return url

    class Meta:
        model = Submission
        fields = ('title', 'url', 'text', 'ctp', 'regard', 'stoDate', 'image')

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(SubmissionForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['image'].required = False


class ImageForm(forms.Form):
    image = forms.ImageField()
