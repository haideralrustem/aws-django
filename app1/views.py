from django.shortcuts import render
from .models import Info

from django.http import HttpResponse   # me


pulled_data = [
    {
        'section_title': 'head',
        'section_text': 'Haider Al-Rustem',
    },

    {
        'section_title': 'address',
        'section_text': '2630 Bissonnet Street. Houston, TX, 77005',
    },

]


# Create your views here.

def home(request):

    return render(request,
                  'app1/home.html',  # template name
                  )

#........

def about(request):

    context = {
        'pulled_data': pulled_data
    }

    context2 = {
        'pulled_data': Info.objects.all()
    }

    return render(request, template_name='app1/about.html', context=context2)

#...............

