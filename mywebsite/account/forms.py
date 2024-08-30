from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

# 필드별 부적절한 단어 리스트
USERNAME_INAPPROPRIATE_WORDS = [
    'satan', 'murder', 'bomb', 'moron', 'drug', 
]
NICKNAME_INAPPROPRIATE_WORDS = [
    '관리자', '운영자', '시발', '병신', '섹스', '야동', '18금',
    'admin', 'moderator', 'fuck', 'bitch', 'sex', 'pron', 'nsfw',
]
PASSWORD_INAPPROPRIATE_WORDS = [
    'password', '123456', 'qwerty', 'letmein', 'admin', 'welcome',
]
INTEREST_INAPPROPRIATE_WORDS = [ 
    '음란물', '도박', '마약', '불법', '테러', '자살', '폭력',
    'pornography', 'gambling', 'drugs', 'illegal', 'terrorism', 'suicide', 'violence',
]

class CustomUserCreationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if username:  # None이 아님을 확인
            for bad_word in USERNAME_INAPPROPRIATE_WORDS:
                if bad_word.lower() in username.lower():
                    raise forms.ValidationError(_('아이디: 입력 불가능한 값입니다.'))
        return username
        
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname', '')
        if nickname:  # None이 아님을 확인
            for bad_word in NICKNAME_INAPPROPRIATE_WORDS:
                if bad_word.lower() in nickname.lower():
                    raise forms.ValidationError(_('닉네임: 입력 불가능한 값입니다.'))
        return nickname
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        if password:  # None이 아님을 확인
            for bad_word in PASSWORD_INAPPROPRIATE_WORDS:
                if bad_word.lower() in password.lower():
                    raise forms.ValidationError(_('비밀번호: 입력 불가능한 값입니다.'))
        return password
        
    def clean_area_of_interest(self):
        area_of_interest = self.cleaned_data.get('area_of_interest', '')
        if area_of_interest:  # None이 아님을 확인
            for bad_word in INTEREST_INAPPROPRIATE_WORDS:
                if bad_word.lower() in area_of_interest.lower():
                    raise forms.ValidationError(_('관심분야: 입력 불가능한 값입니다.'))
        return area_of_interest
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'nickname', 'profile_picture', 'age_range', 'area_of_interest')
        
        
class CustomAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if username:  # None이 아님을 확인
            for bad_word in USERNAME_INAPPROPRIATE_WORDS:
                if bad_word.lower() in username.lower():
                    raise forms.ValidationError(_('아이디: 입력 불가능한 값입니다.'))
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if password:  # None이 아님을 확인
            for bad_word in PASSWORD_INAPPROPRIATE_WORDS:
                if bad_word.lower() in password.lower():
                    raise forms.ValidationError(_('비밀번호: 입력 불가능한 값입니다.'))
        return password
        
class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        new_password = self.cleaned_data.get('new_password1', '')
        if new_password:  # None이 아님을 확인
            for bad_word in PASSWORD_INAPPROPRIATE_WORDS:
                if bad_word.lower() in new_password.lower():
                    raise forms.ValidationError(_('비밀번호: 입력 불가능한 값입니다.'))
        return new_password
