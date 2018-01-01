import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from sc.models import Submission, CreativeType
from users.models import ScUser


class UserForm(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z_]*$',
                                  'Это поле может содержать только буквы, '
                                  'числа и символ _.')
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

    username = forms.CharField(widget=forms.TextInput(
        attrs=
        {'class': "form-control",
         'placeholder': "Логин",
         'required': '',
         'autofocus': ''}),
        max_length=12,
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

    display_picture = forms.BooleanField(required=False)

    about_text = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control",
               'id': "about_me",
               'rows': "4",
               }),
        max_length=500,
        required=False
    )

    homepage = forms.CharField(widget=forms.URLInput(
        attrs={'class': "form-control",
               'id': "homepage"}),
        required=False
    )

    instagram = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'id': "instagram",
               'type': "text"}),
        required=False,
        max_length=39
    )

    twitter = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'id': "twitter",
               'type': "text"}),
        required=False,
        max_length=39
    )

    fb = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'id': "fb",
               'type': "text"}),
        required=False,
        max_length=39
    )

    vk = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'id': "vk",
               'type': "text"}),
        required=False,
        max_length=39
    )

    telegram = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'id': "telegram",
               'type': "text"}),
        required=False,
        max_length=39
    )

    youtube = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'id': "youtube",
               'type': "text"}),
        required=False,
        max_length=39
    )

    date = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control",
               'id': "date",
               "placeholder": "1995-12-14"}),
        required=False
    )



    class Meta:
        model = ScUser
        fields = ('first_name', 'last_name', 'email','date',
                  'display_picture', 'about_text',
                  'homepage', 'instagram', 'twitter','fb','vk','telegram','youtube')


class SubmissionForm(forms.ModelForm):
    link_type = -1

    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': "Submission title"}),
        required=True, min_length=1, max_length=250)

    url = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': "(Optional) http:///www.example.com"}),
        required=False)

    ctp = forms.ModelMultipleChoiceField(required=False,queryset=CreativeType.objects.all())
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "form-control",
            'rows': "3",
            'placeholder': "Optional text"}),
        max_length=5000,
        required=False)


    def clean_url(self):
        url = self.cleaned_data['url']
        print(url)
        # flickr
        match = re.search(r'<img src="[\'"]?([^\'" >]+)staticflickr([^\'" >]+)"',url)
        if match:
            url = match.group(0)[10:-1]
            self.link_type = Submission.LINK_TYPE_FLICKR
            print("matches")
        else:
            # soundcloud
            match = re.search(r'src="https:\/\/w.soundcloud.com\/[\'"]?([^\'" >]+)"', url)
            if match:
                url = match.group(0)[5:-1]
                self.link_type = Submission.LINK_TYPE_SOUNDCLOUND
            else:
                # youtube
                match = re.search(r'[\'"]?([^\'" >]+)youtube([^\'" >]+)', url)
                if match:
                    url = match.group(0).replace("watch?v=","embed/")
                    self.link_type = Submission.LINK_TYPE_YOUTUBE
                else:
                    match = re.search(r'[\'"]?([^\'" >]+).([^\'" >]+)', url)
                    if match:
                        self.link_type = Submission.LINK_TYPE_NOT_PROCESSED
                        url = match.group(0)
                    else:
                        pass
                        #raise ValidationError("Не удалось расшифровать ссылку")
        return url

    class Meta:
        model = Submission
        fields = ('title', 'url', 'text','ctp')
