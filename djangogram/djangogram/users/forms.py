from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms as django_forms
from django.core.exceptions import ValidationError

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])

# 로그인에 사용할 html 태그
class SignUpForm(django_forms.ModelForm):
    class Meta():
        model = User
        fields = ['email', 'name', 'username', 'password']
        
        # 라벨병 변경
        labels = {
            'email': '이메일 주소',
            'name': '성명',
            'username': '사용자 이름',
            'password': '비밀번호'
        }
        
        # 태그 각각 변경
        widgets = {
            'email': django_forms.TextInput(attrs={'placeholder': '이메일 주소'}),
            'name': django_forms.TextInput(attrs={'placeholder': '성명'}),
            'username': django_forms.TextInput(attrs={'placeholder': '사용자 이름'}),
            'password': django_forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
        }
    
    # 패스워드 저장시 정상적으로 저장할수 있게 작성
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user