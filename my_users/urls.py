from django.urls import path
from django.conf.urls  import url
from . import views

app_name = 'my_users'  # me

urlpatterns = [
    path('', views.register, name='my_users-register'),
   

    path('register2', views.register2, name='my_users-register2'),
    path('profile', views.user_profile, name='profile'),

    url('testing/(?P<p>\d+)', views.testing, name="testing"),

    url('post/ajax/update_userform', 
        views.test_updateUserForm, name="test_post_update_userform"),
    
    path('post/ajax/userform', views.postUserForm, name='post_userform'),
    
    path('post/ajax/update_userform', views.updateUserForm, name='post_update_userform'),

    path('get/ajax/user', views.getUser, name='get_user')

]