from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("このユーザー名はすでに使用されています。")
        return username
    
    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    

class UserChangeForm(ModelForm):#パスワードについて追加
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        username = kwargs.pop('username', None)
        super().__init__(*args, **kwargs)
        if username:
            self.fields['username'].widget.attrs['value'] = username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("このユーザー名はすでに使用されています。")
        return username

    def update(self, user):
        user.username = self.cleaned_data['username']
        user.save()

    def __init__(self, username=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if username:
            self.fields['username'].widget.attrs['value'] = username

    def update(self, user):
        user.username = self.cleaned_data['username']
        user.save()
