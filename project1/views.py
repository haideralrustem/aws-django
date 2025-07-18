
from django.shortcuts import redirect, render
import pandas as pd
from .forms import UploadedDataFormHandler, GenericValueForm, GenericMultichoiceForm
from django.http import JsonResponse
from django.core import serializers
import re


# import django.contrib.sessions

# me
import my_functions

from django.conf import settings
import pdb
import json

import os

from datetime import datetime, time, timedelta
import time
import string
import csv
import main_urls
# import sys
# sys.path.append("..")
# import my_functions

# persistent vars
persistent_data_state = {}

prev_file_name = {'prev_file': ''}
select_options =['Decimal number', 'Whole number', 'Text', 'Date', 'Time', 'Time period']

# AJAX Reqs
def accept_uploaded_data(request):

    print('\n\n\n accept_uploaded_data@  views.py has been hit \n\n\n')
    if request.method == 'POST' and ( request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        
        u_form = UploadedDataFormHandler(request.POST)
        # save the data and after fetch the object in instance
        if u_form.is_valid():
            accept_value = u_form.cleaned_data['accept_value']   

            
            # pass session variables ??? <<<<<<<
            if accept_value == 'true':
                
                rows = persistent_data_state['rows'] 
                headers = persistent_data_state['headers'] 
                original_dtypes_values = persistent_data_state['original_dtypes_values'] 
                str_rows = persistent_data_state['str_rows'] 
                modded_rows = persistent_data_state['modded_rows'] 
                new_dtypes_values = persistent_data_state['new_dtypes_values'] 

                data_state = {
                'headers': headers, 'original_dtypes_values': original_dtypes_values,
                'str_rows': str_rows,
                'new_dtypes_values': new_dtypes_values
                }
                

                return JsonResponse({                                    
                'msg': 'accept_value posted successfully', 
                                    'accept_value': accept_value,
                                    }, status=200)

            return JsonResponse({
                                 'msg': 'form was valid but but accept_value was false',
                                 'accept_value': accept_value,
                                 }, status=400)
        
        else:
            return JsonResponse({'msg':'Form was not valid'}, status=400)

    return JsonResponse({'status':'Fail', 'msg':'Not a valid request'}, status=400)

# .................................


def auto_detect_data(request):
    global persistent_data_state
    if request.method == 'POST' and ( request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        detect_table_format = GenericValueForm(request.POST)

        if detect_table_format.is_valid() and len(persistent_data_state) > 2:
            text_key = detect_table_format.cleaned_data['text_key']
            text_value = detect_table_format.cleaned_data['text_value']

            # retrieve the original data
            if persistent_data_state and 'rows' in persistent_data_state:
                rows = persistent_data_state['rows']
                headers = persistent_data_state['headers']
                strip_headers = persistent_data_state['strip_headers']
                original_dtypes_values = persistent_data_state['original_dtypes_values']
                str_rows = persistent_data_state['str_rows']
            else:
                sor = request.session['serialized_original_rows']
                rows = my_functions.deserialize_data(sor)
                
                original_dtypes_values = request.session['original_dtypes_values'] 
                headers = request.session['headers'] 
                strip_headers = request.session['strip_headers']
                cmr =request.session['serialized_modded_rows']
                current_modded_rows = my_functions.deserialize_data(cmr)
                current_dtypes_values = request.session['new_dtypes_values']


            if text_value == 'auto-format':
                # auto format
                # modded_rows, new_dtypes_values = my_functions.post_process_dtypes(
                #                                                 original_dtypes_values, 
                #                                                 headers, rows)

                modded_rows = persistent_data_state['original_modded_rows']
                original_modded_dtypes_values =persistent_data_state[
                                                'original_modded_dtypes_values']

                str_modded_rows = my_functions.stringfy_data(original_modded_dtypes_values, headers, modded_rows)
            
                new_dtypes_values_readable = my_functions.convert_to_readable_dtype_value(original_modded_dtypes_values)
                
               
                persistent_data_state['modded_rows'] = modded_rows
                persistent_data_state['new_dtypes_values'] = original_modded_dtypes_values
                persistent_data_state['new_dtypes_values_readable'] = new_dtypes_values_readable
                
                return JsonResponse({                                    
                        'msg': 'auto_detect_data posted successfully', 
                                            'text_key': text_key,
                                            'text_value': text_value,
                                            'headers': headers,
                                            'strip_headers': strip_headers,
                                            'str_modded_rows': str_modded_rows,
                                            'original_modded_dtypes_values': original_modded_dtypes_values,
                                            'original_dtypes_values_readable_length': len(new_dtypes_values_readable),
                                            'new_dtypes_values_readable': new_dtypes_values_readable,
                                            'select_options': select_options #dropdown options
                                            }, status=200) 
            else:
                return JsonResponse({'msg': 'error auto_detect_data value was not "auto-format"', 
                                }, status=400)

        else:
                return JsonResponse({'msg': 'error auto_detect_data form was not valid or no file uploaded', 
                                    }, status=400)
# .........................

# select_chart_type_form
def change_col_dtype(request):
    global persistent_data_state
    print('\n\n\n change_col_dtype @  views.py has been hit \n\n\n')
    if request.method == 'POST' and ( request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        
        u_form = GenericValueForm(request.POST)
        
        if u_form.is_valid():
            print('\n\n u_form \n\n', u_form.cleaned_data)
            text_key = u_form.cleaned_data['text_key']
            text_value = u_form.cleaned_data['text_value']

            # retrieve the original data
            if persistent_data_state and 'rows' in persistent_data_state:
                
                rows = persistent_data_state['rows']
                
                headers = persistent_data_state['headers']
                original_dtypes_values = persistent_data_state['original_dtypes_values']
                str_rows = persistent_data_state['str_rows']

                # current rows (which could be modded) and dtypes
                current_modded_rows = persistent_data_state['modded_rows']
                current_dtypes_values = persistent_data_state['new_dtypes_values']

                current_dtypes_values_readable = persistent_data_state['new_dtypes_values_readable'] 
            
            else:
                sor = request.session['serialized_original_rows']
                rows = my_functions.deserialize_data(sor)
                
                original_dtypes_values = request.session['original_dtypes_values'] 
                headers = request.session['headers'] 

                cmr =request.session['serialized_modded_rows']
                current_modded_rows = my_functions.deserialize_data(cmr)
                current_dtypes_values = request.session['new_dtypes_values']
               


            target_dtype = my_functions.reverse_readable_dtype_value(text_value)
            colname = text_key
            index_of_colname = headers.index(colname) # needed to target table cells

            target_change_cols = { colname : target_dtype }
            
            modded_rows, ndtypes = my_functions.manual_change_data_type(
                                                dtypes_values=current_dtypes_values, 
                                                target_change_cols=target_change_cols, 
                                                headers=headers, 
                                                rows=rows)
            timedelta_str = None
            # str_rows is just for the view
            if 'datetime.timedelta' in target_dtype:
                timedelta_str = target_dtype.split(' ')[1]
                                
            
            str_modded_rows = my_functions.stringfy_data(ndtypes, 
                                                        headers, 
                                                        modded_rows, 
                                                        timedelta_str=timedelta_str)

            persistent_data_state['modded_rows'] = modded_rows
            persistent_data_state['new_dtypes_values'] = ndtypes

            return JsonResponse({                                    
                    'msg': 'change dtype posted successfully', 
                                        'selected_header': text_key,
                                        'selected_value': text_value,
                                        'selected_header_index': index_of_colname,
                                        'str_modded_rows': str_modded_rows
                                        }, status=200) 
        else:
            return JsonResponse({'msg': 'error form was not valid', 
                                }, status=400)
# .....................................



def select_chart_type(request):
    global persistent_data_state
    
    if request.method == 'POST' and ( request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        
        
        # select_chart_type_form
        select_chart_type_form = GenericValueForm(request.POST)

        u_form = select_chart_type_form
        
        if u_form.is_valid():
            print('\n\n select_chart_type_form \n\n', u_form.cleaned_data)
            text_key = u_form.cleaned_data['text_key']
            text_value = u_form.cleaned_data['text_value']
            chart_type = text_value

            # retrieve the original data
            print(persistent_data_state.keys())
            if persistent_data_state and 'rows' in persistent_data_state:
                rows = persistent_data_state['rows']
                headers = persistent_data_state['headers']
                original_dtypes_values = persistent_data_state['original_dtypes_values']
                str_rows = persistent_data_state['str_rows']
            

                # current rows (which could be modded) and dtypes
                current_modded_rows = persistent_data_state['modded_rows']
                current_dtypes_values = persistent_data_state['new_dtypes_values']

                current_dtypes_values_readable = persistent_data_state['new_dtypes_values_readable'] 
                
                # put in sessions
                serialized_rows = my_functions.serialize_data(rows)
                serialized_modded_rows = my_functions.serialize_data(current_modded_rows)

                
                request.session['serialized_original_rows'] = serialized_rows
                request.session['serialized_modded_rows'] = serialized_modded_rows
                request.session['original_dtypes_values'] = original_dtypes_values
                request.session['new_dtypes_values'] = current_dtypes_values
                request.session['headers'] = headers
                request.session['chart_type'] = chart_type
            
            else:
                
                sor = request.session['serialized_original_rows']
                rows = my_functions.deserialize_data(sor)
                
                original_dtypes_values = request.session['original_dtypes_values'] 
                headers = request.session['headers'] 

                cmr =request.session['serialized_modded_rows']
                current_modded_rows = my_functions.deserialize_data(cmr)
                current_dtypes_values = request.session['new_dtypes_values']

            
            allowed_x_names, allowed_y_names, allowed_x_types, allowed_y_types = my_functions.determine_allowed_xy(
                                                chart_type, current_modded_rows, 
                                                headers, current_dtypes_values)

        
            return JsonResponse({                                    
                    'msg': 'select CHART type posted successfully', 
                                        'text_key': text_key,
                                        'chart_type': chart_type,
                                        'allowed_x_columns': json.dumps(allowed_x_names),
                                        'allowed_y_columns': json.dumps(allowed_y_names),
                                        'allowed_x_types': json.dumps(allowed_x_types),
                                        'allowed_y_types': json.dumps(allowed_y_types)
                                        }, status=200) 
        else:
            return JsonResponse({'msg': 'error form was not valid', 
                                }, status=400)


# .............................................



def generate_plot(request):
    global persistent_data_state


    
    if request.method == 'POST' and ( request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        
        # select_chart_type_form
        select_axis_form = GenericValueForm(request.POST)

        u_form = select_axis_form
        
        if u_form.is_valid():
            print('\n\n select_axis_form \n\n', u_form.cleaned_data)
            text_key = u_form.cleaned_data['text_key']
            text_value = u_form.cleaned_data['text_value']

            x_name = text_key
            y_name = text_value

            # retrieve the original data
            if persistent_data_state and 'rows' in persistent_data_state:
                rows = persistent_data_state['rows']
                headers = persistent_data_state['headers']
                original_dtypes_values = persistent_data_state['original_dtypes_values']
                str_rows = persistent_data_state['str_rows']

                # current rows (which could be modded) and dtypes
                current_modded_rows = persistent_data_state['modded_rows']
                current_dtypes_values = persistent_data_state['new_dtypes_values']
                current_dtypes_values_readable = persistent_data_state['new_dtypes_values_readable'] 
                
            else:
                sor = request.session['serialized_original_rows']
                rows = my_functions.deserialize_data(sor)
                
                original_dtypes_values = request.session['original_dtypes_values'] 
                headers = request.session['headers'] 
                cmr =request.session['serialized_modded_rows']
                current_modded_rows = my_functions.deserialize_data(cmr)
                current_dtypes_values = request.session['new_dtypes_values']


            request.session['x_name'] = x_name
            request.session['y_name'] = y_name
            chart_type = request.session['chart_type']
            
            y_names = [y_name]

            
            #  visualization step ......

            if chart_type == 'MULTI-LINE-CHART':
                y_names = json.loads(y_name)
                my_functions.multiline_chart(current_modded_rows,
                                        current_dtypes_values, x_name, y_names)                  
            
            elif chart_type == 'LINE-CHART':
                my_functions.single_line_chart(current_modded_rows, x_name, y_names, 
                                                current_dtypes_values)

            elif chart_type == 'BAR-CHART':
                my_functions.bar_chart(current_modded_rows, x_name, y_names)
                pass
                
            elif chart_type == 'HISTOGRAM':
                my_functions.histogram(current_modded_rows, x_name, y_names, 
                                       current_dtypes_values)
            elif chart_type == 'SCATTERPLOT':
                my_functions.single_scatter_plot(current_modded_rows, x_name, y_names, 
                                       current_dtypes_values, True)

            elif chart_type == 'PIE-CHART':
                my_functions.pie_chart(current_modded_rows, x_name, y_names, 
                                       current_dtypes_values)

             
                                              
            return JsonResponse({                                    
                    'msg': 'select X_NAME and Y_NAME posted successfully', 
                                        'x_name': text_key,
                                        'y_name': text_value,
                                        'url_redirect': '/project1/viz'
                                        # 'allowed_x_columns': json.dumps(allowed_x_names),
                                        # 'allowed_y_columns': json.dumps(allowed_y_names),
                                       
                                        }, status=200) 
        else:
            
            return JsonResponse({'msg': 'error form was not valid', 
                                }, status=400)

# .............................




# Create your views here.

def data_file_upload(request):

    
    global persistent_data_state
    if request.method == 'POST' and not ( request.headers.get('x-requested-with') == 'XMLHttpRequest'):  # file upload 
        

        y_names = []
        file_path = os.path.join(settings.BASE_DIR, '')
        rows=[]
        file_name = 'app1\\static\\csv_files\\data2.csv'
        show_modal = 'false'
        
        if 'uploaded_file' in request.FILES:
            uploaded_file = request.FILES['uploaded_file']
            # reset vars?
            persistent_data_state = {}
            print(' >>>> \t >>>> persistent_data_state has been reset! ')
            request.session['serialized_original_rows'] = None
            request.session['original_dtypes_values'] =None
            request.session['headers'] =None

            request.session['new_dtypes_values'] =None
            request.session['x_name'] = None
            request.session['y_name'] = None
            request.session['serialized_modded_rows'] = None
            request.session['new_dtypes_values'] = None
            request.session['chart_type'] = None

        else:
            return render(request, 'project1/presets_config.html')
        # file_path = os.path.join(settings.BASE_DIR, file_name)


        # pipeline to open csv, save the data to a TabularDataSets model
        
        dataset_name = "dataset_"+ str(time.time())
                       
        headers, rows = my_functions.prepare_data(file_name=uploaded_file, dataset_name=dataset_name)
        original_dtypes_values = my_functions.detect_datatypes(headers, rows)
        original_dtypes_values_readable = my_functions.convert_to_readable_dtype_value(
                                                       original_dtypes_values)
                                            


        
        # str_header_and_rows = 
        strip_headers = [re.sub('\s', '', header) for header in headers]
        strip_header_mapper = {}
        keys = list(original_dtypes_values_readable.keys())
        i = 0
        for k in keys:
            strip_header_mapper[k] = strip_headers[i]
            i+=1
        
        
        modded_rows, new_dtypes_values = my_functions.post_process_dtypes(
                                                            original_dtypes_values, 
                                                            headers, rows)
        
        
        str_rows = my_functions.stringfy_data(original_dtypes_values, headers, rows)
        str_modded_rows = my_functions.stringfy_data(original_dtypes_values, headers, modded_rows)
       
        new_dtypes_values_readable = my_functions.convert_to_readable_dtype_value(new_dtypes_values)
        
               
        # user presented with a choice
        # modded_rows2, new_dtypes_values2 = manual_change_data_type(original_dtypes_values, {'date': 'datetime.timedelta minutes'}
        #                         , headers, rows)       
        
       

        # get only the colummn names
        # column_names = my_functions.unpack_csvrow_values(rows[0].row_variables)
        # for r in rows:
        #     single_row = my_functions.unpack_csvrow_values(row_values=r.row_values)
        #     new_rows.append(single_row)
            
        # json_string_dict = my_functions.convert_rows_to_json(column_names=column_names, 
        #                                         list_of_rows=new_rows)
        
        uploaded_data_form_handler = UploadedDataFormHandler(initial={'accept_value': 'false'})
        
        change_dtype_form = GenericValueForm()
        detect_table_format = GenericValueForm()
        select_chart_type_form =  GenericValueForm()
        select_axis_form =  GenericValueForm()
        

        choices = [ch for ch in original_dtypes_values_readable.keys()]
        change_dtype_form_multi = GenericMultichoiceForm(custom_choices=choices)
        
        context = {'uploaded_file': uploaded_file, 'rows': rows, 
                    'headers': headers, 
                    'strip_headers': strip_headers,
                    'strip_header_mapper': strip_header_mapper,
                    'original_dtypes_values': original_dtypes_values,
                    'original_modded_dtypes_values': new_dtypes_values,
                    'str_rows': str_rows,
                    'str_modded_rows': str_modded_rows,
                    'modded_rows': modded_rows, 'new_dtypes_values': new_dtypes_values,
                    'original_dtypes_values_readable': original_dtypes_values_readable,
                    'original_dtypes_values_readable_length': len(original_dtypes_values_readable),
                    'uploaded_data_form_handler': uploaded_data_form_handler,
                    'detect_table_format': detect_table_format,
                    'change_dtype_form': change_dtype_form,
                    'select_chart_type_form': select_chart_type_form,
                    'change_dtype_form_multi': change_dtype_form_multi,
                    'select_axis_form': select_axis_form,
                    'show_modal': show_modal,
                    'finsihed': '1'
                    
                    }

        persistent_data_state['rows'] = rows
        persistent_data_state['strip_headers'] = strip_headers
        persistent_data_state['headers'] = headers
        persistent_data_state['original_dtypes_values'] = original_dtypes_values
        persistent_data_state['original_modded_dtypes_values'] = new_dtypes_values
        persistent_data_state['str_rows'] = str_rows
        persistent_data_state['modded_rows'] = modded_rows
        persistent_data_state['original_modded_rows'] = modded_rows
        persistent_data_state['new_dtypes_values'] = new_dtypes_values
        persistent_data_state['new_dtypes_values_readable'] = new_dtypes_values_readable


        # put in sessions
        serialized_rows = my_functions.serialize_data(rows)
        serialized_modded_rows = my_functions.serialize_data(modded_rows)

        # you retrieve this from other view
        desrialized_rows = my_functions.deserialize_data(serialized_rows)
        desrialized_modded_rows = my_functions.deserialize_data(serialized_modded_rows)

        request.session['serialized_original_rows'] = serialized_rows
        request.session['original_dtypes_values'] = original_dtypes_values
        request.session['headers'] = headers
        request.session['new_dtypes_values'] = new_dtypes_values
        request.session['serialized_modded_rows'] = serialized_modded_rows
        request.session['strip_headers'] = strip_headers
       
        context['url_context'] = main_urls.url_context

        return render(request, 'project1/presets_config.html', context)

    else:
        change_dtype_form = GenericValueForm()
        

        context = {'uploaded_file': 'no file uploaded yet',
                    'change_dtype_form': change_dtype_form,
                  }
        context['url_context'] = main_urls.url_context
        return render(request, 'project1/presets_config.html', context)


# ........................................


def main_page_viz(request):  
    deliver_modded_rows = []

    file_path = os.path.join(settings.BASE_DIR, '')
    
    # retrieval 
    
    serialized_original_rows = request.session['serialized_original_rows']
    serialized_modded_rows = request.session['serialized_modded_rows']
    original_dtypes_values= request.session['original_dtypes_values']
    current_dtypes_values = request.session['new_dtypes_values']
    headers= request.session['headers']
    chart_type = request.session['chart_type']
    x_name = request.session['x_name']
    y_name = request.session['y_name'] #  deserialize y_name

    # if chart_type == 'MULTI-LINE-CHART':
    #     y_name = json.dumps(y_name)

    current_modded_rows = my_functions.deserialize_data(serialized_modded_rows)

    deliver_modded_rows = current_modded_rows.copy()

    for col, dtype in  current_dtypes_values.items():
            if dtype=='date':
                sorted_modded_rows = my_functions.sort_dates(
                                                col, current_modded_rows, headers, 
                                                current_dtypes_values)
        
                str_date_rows = my_functions.stringify_dates(sorted_modded_rows, 
                                                            current_dtypes_values)
                deliver_modded_rows = str_date_rows
    

    json_recieved_data = json.dumps(deliver_modded_rows)

    # json_recieved_data = my_functions.stringfy_data2(
    #                             current_dtypes_values, 
    #                             headers, 
    #                             deliver_modded_rows)
    json_current_dtypes_values = json.dumps(current_dtypes_values)
   
    context = {
        'data_array': [1, 2, 3, 4 , 5],
       
        'BASE_DIR': settings.BASE_DIR,
        'file_path': file_path,
        'debug_vars': {
            'json_string_dict': ''

        },
        'deliver_modded_rows': deliver_modded_rows,
        'json_recieved_data': json_recieved_data,
        'chart_type': chart_type,
        'x_name': x_name,
        'y_name': y_name ,
        'json_current_dtypes_values': json_current_dtypes_values      
    }

    context['url_context'] = main_urls.url_context

    

    # return render(request, 'project1/main_page.html', context)
    return render(request, 'project1/main_page.html', context)


# ..........................


def intro(request): 
    context = {}

    
    context['url_context'] = main_urls.url_context
    return render(request, 'project1/intro.html', context)


# .......................

def testing_page(request):
    context={}
    context['url_context'] = main_urls.url_context
    return render(request, 'project1/testing_page.html', {})