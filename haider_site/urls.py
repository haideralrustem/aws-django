"""haider_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


# import for deployments
from django.conf.urls import url
from django.views.static import serve



from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app1.urls')),

    path('register/', include('my_users.urls', namespace='register')),
    path('', include('my_users.urls', namespace='user_profile')),
    path('project1', include('project1.urls', namespace='project1')),

    path('project2', include('project2.urls', namespace='project2')),

    path('login/', auth_views.LoginView.as_view(template_name='my_users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='my_users/logout.html'), name='logout'),


url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

