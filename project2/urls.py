from django.urls import path
from . import views


app_name = 'project2'  # me



urlpatterns = [
    
    path('', views.intro, name='intro'),
    path('/text_analyzer_main', views.text_analyzer_main, name='text_analyzer_main'),
       

    # # ajax requests
    path('/ajax/post/analyze_text', views.analyze_text, name="analyze_text"),
    # #auto_detect_data
    # path('/ajax/post/auto_detect_data', views.auto_detect_data, name="auto_detect_data"),
    
    # path('/ajax/post/change_col_dtype', views.change_col_dtype, name="change_col_dtype"),
    # # 
    # path('/ajax/post/select_chart_type', views.select_chart_type, name="select_chart_type"),
    
    # path('/ajax/post/generate_plot', views.generate_plot, name="generate_plot"),
  
]