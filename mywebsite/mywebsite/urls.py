from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

urlpatterns = [
	path('admin/', admin.site.urls),
    path('', include('main.urls')),  # '/'
    path('account/', include('account.urls')),
    path('blog/', include('blog.urls')),  
]

# 개발 환경에서 media 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'blog.views.custom_404'