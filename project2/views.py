from django.shortcuts import render

from django.conf import settings

from .forms import *

from django.http import JsonResponse
from django.core import serializers
import pdb
import json

import os

from datetime import datetime, time, timedelta
import time
import string
import csv

import text_classification as tc




# AJAX

def analyze_text(request):

    word_count = 0
    frequency_graph_data = []
    likely_topic = ''
    word_cloud_url = ''
    complexity_score = ''

    if request.method == 'POST' and request.is_ajax():
        
        u_form = UploadedDataFormHandler(request.POST)
        # save the data and after fetch the object in instance
        if u_form.is_valid():
            text_value = u_form.cleaned_data['text_value']   
            if len(text_value) <= 0:
                 return JsonResponse({                                    
                                'msg': 'text_value length is zero', 
                                'text_value': text_value,
                                'word_count': 0,
                                'frequency_graph_data': None,
                                'complexity_score': None,
                                'likely_topic': None,
                                'word_cloud_url': None
                                }, status=400)
            
            text_value = text_value + ' '

            # text analysis pipeline goes here:
            freq_dict, word_count = tc.word_frequency(text_value)
            frequency_graph_data = tc.convert_to_data_array(freq_dict)
            

            score = tc.FleschReadabilityEase(text_value)
            percentage = tc.convert_Flesch_percentage(score)
            complexity_score = percentage

            likely_topic =  tc.predict_likely_topic(text_value)
            
            word_cloud_url = tc.generate_word_cloud(text_value)
            
            # json_recieved_data = json.dumps(deliver_modded_rows)

            return JsonResponse({                                    
            'msg': 'text_value posted successfully', 
                                'text_value': text_value,
                                'word_count': word_count,
                                'frequency_graph_data': frequency_graph_data,
                                'complexity_score': complexity_score,
                                'likely_topic': likely_topic,
                                'word_cloud_url': word_cloud_url
                                }, status=200)

                    
        else:
            return JsonResponse({'msg':'Form was not valid'}, status=400)

    return JsonResponse({'status':'Fail', 'msg':'Not a valid request'}, status=400)



# Create your views here.

def intro(request):
    context = {'BASE_DIR': settings.BASE_DIR}

    return render(request, 'project2/intro.html', context)

# ............................

def text_analyzer_main(request):
    context = {}

    u_form = UploadedDataFormHandler()
    context['u_form'] = u_form
    # json_recieved_data = json.dumps(deliver_modded_rows)

    return render(request, 'project2/text_analyzer_main.html', context)