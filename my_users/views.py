from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import   login_required

from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.forms import User

from .my_forms import MyUserRegisterForm, UserUpdateForm, UserEmailUpdateForm, ProfileUpdateForm
from .models import Profile



# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():  # makes a check at the backend
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username} !')
            return redirect ('app1-home')

    else:
        form = UserCreationForm()

    return render(request, 'my_users/user_registeration.html', {'suppliedform': form})

#......................

def register2(request):
    if request.method == 'POST':
        custom_form = MyUserRegisterForm(request.POST)
        if custom_form.is_valid():  # makes a check at the backend
            username = custom_form.cleaned_data.get('username')
            custom_form.save()
            messages.success(request, f'Account created for {username} !')
            return redirect ('login')

    else:
        custom_form = MyUserRegisterForm()

    return render(request, 'my_users/user_registeration2.html', {'suppliedform': custom_form})

#...................


# @ login_required
# def user_profile(request):
#     success_msg_visible = {'display_status': False}
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         u_email_form = UserEmailUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

#         if u_form.is_valid():
#             u_form.save()
            
#             messages.success(request, f'Your user has been updated!')
#             success_msg_visible['display_status'] = True
#             # return redirect('my_users:profile')
#         else:
#              u_form = UserUpdateForm(instance=request.user)
        
#         if u_email_form.is_valid():
#             u_email_form.save()
            
#             messages.success(request, f'Your email has been updated!')
#             success_msg_visible['display_status'] = True
#             # return redirect('my_users:profile')
#         else:
#             # this will just reset the form 
#             u_email_form = UserEmailUpdateForm(instance=request.user)

#         if p_form.is_valid():
            
#             print('>    >      >', p_form.cleaned_data['image'])
#             model_instance = p_form.save(commit=False)

#             # print('\n\n', model_instance.get_image(),'\n\n')

#             p_form.save()
            
#             if (model_instance.get_image()):
#                 messages.success(request, f'Your account has been updated!')
#                 success_msg_visible['display_status'] = True
#                 # return redirect('my_users:profile')

#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         u_email_form = UserEmailUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)



#     context = {
#         'u_form': u_form,
#         'u_email_form': u_email_form,
#         'p_form': p_form,
#         'success_msg_visible': success_msg_visible
#     }

#     return render(request, 'my_users/user_profile.html', context)

#........................................
# .......................................

def postUserForm(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        u_form = UserUpdateForm(request.POST)
        # save the data and after fetch the object in instance
        if u_form.is_valid():
            instance = u_form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": u_form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)

# ......................

def updateUserForm(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            any_pk_id = request.user.id
            obj = User.objects.get(id=any_pk_id)
            obj.username = request.POST['username']
            obj.save()
            # get updated obj
            obj = User.objects.get(id=request.user.id)
            

            return JsonResponse({'status':'Success', 'msg': 'save successfully', 
                                 'new_username': obj.username})
        except User.DoesNotExist:
            return JsonResponse({'status':'Fail', 'msg': 'Object does not exist'})
    else:
        return JsonResponse({'status':'Fail', 'msg':'Not a valid request'})




def test_updateUserForm(request):

    print('\n\n\n  views.py has been hit \n\n\n')
    print('\n\n\n  views.py has been hit \n\n\n')
    if request.method == 'POST' and request.is_ajax():
        try:
            any_pk_id = request.user.id
            obj = User.objects.get(id=any_pk_id)
            obj.username = request.POST['username']
            obj.save()
            # get updated obj
            obj = User.objects.get(id=request.user.id)
            

            return JsonResponse({'status':'Success', 'msg': 'save successfully', 
                                 'new_username': obj.username})
        except User.DoesNotExist:
            return JsonResponse({'status':'Fail', 'msg': 'Object does not exist'})
    else:
        return JsonResponse({'status':'Fail', 'msg':'Not a valid request'})

# .........................

def getUser(request):
        if request.is_ajax and request.method == "GET":
            username = request.GET.get("requested_username", None)

            try:
                user = User.objects.get(username = username)
                        
            except:
                return JsonResponse({"success":False}, status=400)

            user_info = {
                "username": user.username,
            }
            return JsonResponse({"user_info":user_info}, status=200)
        
        return JsonResponse({"success":False}, status=400)
            
        
    

# ..........................


@ login_required
def user_profile(request):
    success_msg_visible = {'display_status': False}

    u_form = UserUpdateForm(initial={'username': request.user.username})
    users = User.objects.all()

    context = {
        'u_form': u_form,
        'users': users,
        'success_msg_visible': success_msg_visible
    }

    return render(request, 'my_users/user_profile.html', context)




def testing(request, p):

    success_msg_visible = {'display_status': False}
    u_form = UserUpdateForm(initial={'username': request.user.username})
    users = User.objects.all()

    context = {
        'p': 7,
        'u_form': u_form,
        'users': users,
        'success_msg_visible': success_msg_visible
    }

    return render(request, 'my_users/test.html', context)