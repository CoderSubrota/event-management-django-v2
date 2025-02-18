
from django.conf.urls.static import static
from events.views import OptimizedEventListView
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.conf import settings
from users.views import ProfileView
urlpatterns = [
    path('', OptimizedEventListView.as_view() , name='home'),
    path('admin/',admin.site.urls),
    path('accounts/profile/', ProfileView.as_view()),
    path('events/', include('events.urls')),
    path('users/',include('users.urls')),
]+ debug_toolbar_urls()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

