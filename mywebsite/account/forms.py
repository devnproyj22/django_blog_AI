from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

# 부적절한 단어 리스트
PROFANITY_LIST = [
    'satan', 'murder', 'bomb', 'moron', 'drug', 
    '사탄', '살인', '폭탄', '저능아', '마약',
]

class CustomUserCreationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        for bad_word in PROFANITY_LIST:
            if bad_word.lower() in username.lower():
                raise forms.ValidationError(_('아이디: 입력 불가능한 값입니다.'))
        return username
        
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        for bad_word in PROFANITY_LIST:
            if bad_word.lower() in nickname.lower():
                raise forms.ValidationError(_('닉네임: 입력 불가능한 값입니다.'))
        return nickname
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if 'password' in password.lower():
            raise forms.ValidationError(_('비밀번호: 입력 불가능한 값입니다.'))
        return password
        
    def clean_area_of_interest(self):
        area_of_interest = self.cleaned_data.get('area_of_interest')
        for bad_word in PROFANITY_LIST:
            if bad_word.lower() in area_of_interest.lower():
                raise forms.ValidationError(_('관심분야: 입력 불가능한 값입니다.'))
        return area_of_interest
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'nickname', 'profile_picture', 'age_range', 'area_of_interest')
        
        
class CustomAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        for bad_word in PROFANITY_LIST:
            if bad_word.lower() in username.lower():
                raise forms.ValidationError(_('아이디: 입력 불가능한 값입니다.'))
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if 'password' in password.lower():
            raise forms.ValidationError(_('비밀번호: 입력 불가능한 값입니다.'))
        return password
        
class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        new_password = self.cleaned_data.get('new_password1')
        for bad_word in PROFANITY_LIST:
            if bad_word.lower() in new_password.lower():
                raise forms.ValidationError(_('비밀번호: 입력 불가능한 값입니다.'))
        return new_password