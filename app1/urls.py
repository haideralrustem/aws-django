from django.urls import path
from . import views


# haider
# Ilovemytmnt5
app_name = 'app1'  # me

urlpatterns = [
    path('', views.home, name='app1-home'),
    path('home', views.home, name='app1-home-page'),
    
    path('about/', views.about, name='app1-about'),

]
