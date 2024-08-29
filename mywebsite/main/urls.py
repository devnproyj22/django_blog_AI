from django.urls import path
from .views import MainView

app_name='main'                         # 'main/'로 시작하는 URL 패턴
urlpatterns = [
    path('', MainView.as_view(), name='home'), 
]