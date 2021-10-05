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


context = {
    'project1_url': 'http://ec2-3-20-48-103.us-east-2.compute.amazonaws.com/project1/intro',
    'project2_url' : 'http://ec2-3-20-48-103.us-east-2.compute.amazonaws.com/project2',
    'food_suggester_url': 'https://haiderapps.herokuapp.com/',
    'home_url': 'https://haiderapps.herokuapp.com/project1/food_suggester',

}


# Create your views here.

def home(request):

    

    return render(request,
                  'app1/home.html',  # template name
                  context
                  )

#........

def about(request):

    context = {
        'pulled_data': pulled_data
    }

    context2 = {
        'pulled_data': Info.objects.all()
    }

    return render(request, template_name='app1/about.html', context=context)

#...............

