from django.shortcuts import render
from .models import Info

from django.http import HttpResponse   # me
import main_urls



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
    context = {}
    
    context['url_context'] = main_urls.url_context

    return render(request,
                  'app1/home.html',  # template name
                  context
                  )

#........

def about(request):

    context = {}
    context['url_context'] = main_urls.url_context
        
    return render(request, template_name='app1/about.html', context=context)

#...............

