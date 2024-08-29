from django.urls import path
from views import CustomLoginView, CustomLogoutView, SignUpView

app_name='account'                     # 'account/'로 시작하는 URL 패턴

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]