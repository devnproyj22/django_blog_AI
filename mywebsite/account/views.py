from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'account/signup.html'
    
    def form_valid(self, form):
        '''회원가입 성공 시 처리'''
        response = super().form_valid(form)
        messages.success(self.request, '회원가입 성공!')
        return response

    def form_invalid(self, form):
        '''회원가입 실패 시 처리'''
        messages.error(self.request, '회원가입 실패!')
        return super().form_invalid(form)
    
    def get_success_url(self):
        '''회원가입 성공 후 리다이렉트할 URL (폼 성공적으로 제출 후)'''
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('account:login')

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True    # 이미 로그인된 사용자를 리다이렉트

    def get_success_url(self):
        '''로그인 후 리다이렉트할 URL을 결정'''
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('main:home') 
    
class CustomLogoutView(LoginRequiredMixin, LogoutView):
    def get_next_page(self):
        '''로그아웃 후 리다이렉트할 URL을 결정'''
        next_page = self.request.GET.get('next')
        if next_page:
            return next_page
        return reverse_lazy('main:home')
        
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('account:login')
    
class CustomUserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'account/account_delete.html'
    success_url = reverse_lazy('main:home')
    
    def get_object(self, queryset=None):
        return self.request.user