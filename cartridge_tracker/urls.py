from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views  # Добавляем этот импорт

urlpatterns = [
    # Редирект с корня сайта на /cartridges/
    path('', RedirectView.as_view(url='/cartridges/', permanent=True)),

    path('admin/', admin.site.urls),
    path('cartridges/', include('cartridges.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='cartridges/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]