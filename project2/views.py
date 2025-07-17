from django.shortcuts import render

from django.conf import settings
import requests

from .forms import *

from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import pdb
import json

import os

from datetime import datetime, time, timedelta
import time
import string
import csv

from dotenv import load_dotenv


from openai import OpenAI

import text_classification as tc

import main_urls


load_dotenv()
api_key = os.getenv("API_KEY")


print(f"\n\n Api key is {api_key} \n\n")

# AJAX

def analyze_text_old(request):

    print('FGH\n\n\n')

    word_count = 0
    frequency_graph_data = []
    likely_topic = ''
    word_cloud_url = ''
    complexity_score =  0
    text_value = ''
    freq_dict = ''
    word_count = None
    frequency_graph_data = None
    score = None
    percentage =None

    API_KEY = 'bbabf90560c20350a1237f4b52f4189b'
    text = "Zara is great, lots of stylish and affordable clothes, shoes, and accessories."
    model = 'IAB_2.0_en'
    url = "https://api.meaningcloud.com/deepcategorization-1.0"

    payload={
                    'key': API_KEY,
                    'txt': text_value,
                    'model': model,  # like IAB_2.0_en
                }

    # response = requests.post(url, data=payload)
    # response = {'status': {'code': '0', 'msg': 'OK', 'credits': '1', 'remaining_credits': 19988}, 
    #             'category_list': [{'code': 'Style&Fashion', 'label': 
    #             'Style and Fashion', 'abs_relevance': '2', 'relevance': '100'}]}
    # print('Status code:', response.status_code)
    # print(response.json())
    
    # pdb.set_trace()

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

            payload={
                    'key': API_KEY,
                    'txt': text_value,
                    'model': model,  # like IAB_2.0_en
                }

            response = requests.post(url, data=payload)
            likely_topic, sucess = tc.validate_response(response)
            fail_reason = 'no fail reason detected when classifying text'
            if sucess == False:
                fail_reason = 'likely topic failed. Reason-> ' + likely_topic
                likely_topic = 'none detected'

            # text analysis pipeline goes here:
            freq_dict, word_count = tc.word_frequency(text_value)
            frequency_graph_data = tc.convert_to_data_array(freq_dict)
            

            score = tc.FleschReadabilityEase(text_value)
            percentage = tc.convert_Flesch_percentage(score)
            complexity_score = percentage

            # likely_topic =  tc.predict_likely_topic(text_value)
            #likely_topic = response.json()['category_list'][0]['label']

            
            
            word_cloud_url = tc.generate_word_cloud(text_value)
            
            # json_recieved_data = json.dumps(deliver_modded_rows)

            return JsonResponse({                                    
            'msg': 'text_value posted successfully', 
                                'text_value': text_value,
                                'word_count': word_count,
                                'frequency_graph_data': frequency_graph_data,
                                'complexity_score': complexity_score,
                                'likely_topic': likely_topic,
                                'word_cloud_url': word_cloud_url,
                                'fail_reason': fail_reason
                                }, status=200)

                    
        else:
            return JsonResponse({'msg':'Form was not valid'}, status=400)

    return JsonResponse({'status':'Fail', 'msg':'Not a valid request'}, status=400)

#________________________________________________________________




@csrf_exempt
def analyze_text(request):

    print('FGH\n\n\n')

    word_count = 0
    frequency_graph_data = []
    likely_topic = ''
    word_cloud_url = ''
    complexity_score =  0
    text_value = ''
    freq_dict = ''
    word_count = None
    frequency_graph_data = None
    score = None
    percentage =None

    API_KEY = api_key
    text_value = "First, it was 7,000. Now it’s 9,000 more. But what's interesting is they are pouring $80 billion into GPUs that never need a coffee break."
    
    client = OpenAI(api_key=API_KEY)
    

    print("\nBefore Request received .....")

    
    if request.method == "POST":

        data = json.loads(request.body)

        
        text_value = data.get("text", "")
        print(f"\nText is\n", text_value)

        if not text_value or len(text_value) <= 0:
            return JsonResponse({"error": "No text provided.", 
                                "msg": "No text provided.",
                                'text_value': text_value,
                                'word_count': 0,
                                'frequency_graph_data': None,
                                'complexity_score': None,
                                'likely_topic': None,
                                'word_cloud_url': None}, status=400)


        # Prompt: Allow multiple topics and subtopics
        system_prompt = (
            "You are a text classification assistant. "
            "Given a piece of text, identify and return all relevant topics and subtopics. "
            "Choose from: sports, entertainment, history, science, technology, politics, health, education, finance, travel, and other. "
            "Return a JSON array like [\"sports: basketball\", \"science: physics\"]"
        )

        try:
            
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_value}
                ],
                temperature=0.3,
                max_tokens=100,
            )

            print("\n", response.choices[0], "\n")
            
            output = response.choices[0].message.content.strip()


            # use this to test static output instead of hitting the API repeatedly and consume quotas
            # output = "[\"Topic A\", \"Topic B\"]"

            print(f"\noutput :\n", output, "\n\n")
            # Try parsing JSON-like output
            try:
                topics = json.loads(output)
                print(f"\ntopics: {topics}\n")
            except json.JSONDecodeError:
                topics = [output]  # fallback: return raw string if not proper JSON




            # text analysis pipeline goes here:
            freq_dict, word_count = tc.word_frequency(text_value)
            frequency_graph_data = tc.convert_to_data_array(freq_dict)
            

            score = tc.FleschReadabilityEase(text_value)
            percentage = tc.convert_Flesch_percentage(score)
            complexity_score = percentage

            # likely_topic =  tc.predict_likely_topic(text_value)
            #likely_topic = response.json()['category_list'][0]['label']

            
            
            word_cloud_url = tc.generate_word_cloud(text_value)

            topics_string = ", ".join(topics)

            
            return JsonResponse({"topics_array": topics, "topics_string": topics_string, 
                                'msg': 'text_value posted successfully', 
                                'text_value': text_value,
                                'word_count': word_count,
                                'frequency_graph_data': frequency_graph_data,
                                'complexity_score': complexity_score,
                                'likely_topic': topics_string,
                                'word_cloud_url': word_cloud_url,
                                'fail_reason': '' 
                                })
        
        except Exception as e:
            return JsonResponse({"error": str(e), 'msg':'An Error Occurred while processing your request.' }, status=500)


   
    return JsonResponse({"error": "Only POST allowed.", 'msg':'Not a valid request'}, status=405)



#-----------------------------------------------------------------------------

# Create your views here.

def intro(request):
    context = {'BASE_DIR': settings.BASE_DIR}
    context['url_context'] = main_urls.url_context
    return render(request, 'project2/intro.html', context)

# ............................

def text_analyzer_main(request):
    context = {}

    u_form = UploadedDataFormHandler()
    context['u_form'] = u_form
    context['url_context'] = main_urls.url_context
    # json_recieved_data = json.dumps(deliver_modded_rows)

    return render(request, 'project2/text_analyzer_main.html', context)
