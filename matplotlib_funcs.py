import matplotlib

matplotlib.rcParams['axes.formatter.useoffset'] = False
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math
import pdb
from matplotlib import cm
import random
import matplotlib.colors as mcolors
import collections
from matplotlib.ticker import ScalarFormatter

import seaborn as sns





# data = [{'Category Name': '', 'loss': , 'gain':},
#         {'Category Name': '', 'loss': , 'gain':},
#         {'Category Name': '', 'loss': , 'gain':},
#         {'Category Name': '', 'loss': , 'gain':},
#         {'Category Name': '', 'loss': , 'gain':},]

def multiline_chart(rows, dtypes_values, x_name, y_names):
  color_schemes = ['dodgerblue', 'lightcoral',
                   'limegreen', 'darkorchid',
                   'orange', 'turquoise']


  x_vals = [row[x_name] for row in rows if x_name != '' and x_name != None]
  plots = []

  agg_dic_list = []
  i = 0
  for y_name in y_names:
    y_vals = [row[y_name] for row in rows ]
    agg_dict = {}

    for xcategory in x_vals:
      agg_dict[xcategory] = 0

      for row in rows:
        x_name_value = row[x_name]


        if x_name_value == xcategory:

          if row[y_name] != None and not math.isnan(row[y_name]):
            agg_dict[xcategory] += row[y_name]


    y_vals = list(agg_dict.values())
    x_names = list(agg_dict.keys())



    agg_dic_list.append(agg_dict)


    p = plt.plot(x_names, y_vals,  color=color_schemes[i], label=y_name, linewidth=4)
    plots.append(p)
    i += 1

  ax = plt.gca()
  ax.get_yaxis().get_major_formatter().set_scientific(False)



  plt.legend()
  plt.grid(b=True, which='both', axis='both', linestyle='-', linewidth=0.2)
  plt.xlabel(x_name)
  plt.ylabel(''.join([y + ", " for y in y_names]))
  plt.tight_layout()
  plt.savefig('./media/generated_plot.png')
  # plt.show()

  plt.close()
  print('/////////////////////')

# ..........................
def single_line_chart(rows, x_name, y_values, dtypes_values=None):
  y_name = y_values[0]
  x_vals = []
  y_vals = []

  for row in rows:
    if (row[x_name] != None and not math.isnan(row[x_name])) or (row[y_name] != None and not math.isnan(row[y_name])):
      x_vals.append(row[x_name])
      y_vals.append(row[y_name])

  fig, ax = plt.subplots()
  line = ax.plot(x_vals, y_vals, linewidth=2,
                   label=y_name) # label is for the line the line
  ax.set_xlabel(x_name)
  ax.set_ylabel(y_name)
  ax.grid(b=True,  which='both', axis='both', linestyle='-',  linewidth=0.2)
  ax.legend(loc='lower right')

  
  if dtypes_values[x_name] in ['int', 'float']:
    ax.get_xaxis().get_major_formatter().set_scientific(False)

  if dtypes_values[y_name] in ['int', 'float']:
   ax.get_yaxis().get_major_formatter().set_scientific(False)

  # plt.show()
  plt.tight_layout()
  plt.savefig('./media/generated_plot.png')
  plt.close()

# ............................

def single_scatter_plot(rows, x_name, y_values, dtypes_values=None, trend_line=True):
  y_name = y_values[0]
  x_vals = []
  y_vals = []

  for row in rows:
    if (row[x_name]!=None and not math.isnan(row[x_name])) or (row[y_name]!=None and not math.isnan(row[y_name])):
      x_vals.append(row[x_name])
      y_vals.append(row[y_name])



  plt.scatter(x_vals, y_vals, color = 'hotpink')

  plt.title('scatterplot')
  plt.xlabel(x_name)
  plt.ylabel(y_name)



  # if (trend_line):
  # z = np.polyfit(x_vals, y_vals, 1)
  # p = np.poly1d(z)
  # plt.plot(x_vals, p(x_vals), "r--")

  sns.regplot(x = x_vals, y=y_vals, line_kws={"color": "red"})
  plt.tight_layout()
  ax = plt.gca()
  ax.get_xaxis().get_major_formatter().set_scientific(False)
  ax.get_yaxis().get_major_formatter().set_scientific(False)
  # plt.show()
  plt.savefig('./media/generated_plot.png')
  plt.close()

# ...............................

def histogram(rows, x_name, y_values, dtypes_values=None):
  mu, sigma = 100, 15
  y_name = y_values[0]
  label = ''
  y_vals=[]
  if x_name:
    y_vals = [row[x_name] for row in rows if row[x_name]]
    label = x_name
  elif y_name:
    y_vals = [row[y_name] for row in rows if row[y_name]]
    label = y_name

  plt.hist(y_vals, density=False, bins=50)  # density=True would make probability, density=False would make counts

  plt.xlabel(label)
  plt.ylabel(f'Count of {label}')
  # plt.title(r'Title')
  plt.grid(True)
  # plt.axis([40, 160, 0, 0.03])
  plt.tight_layout()
  ax = plt.gca()
  ax.get_xaxis().get_major_formatter().set_scientific(False)
  ax.get_yaxis().get_major_formatter().set_scientific(False)
  # plt.show()
  plt.savefig('./media/generated_plot.png')
  plt.close()

# .................

def pie_chart(rows, x_name, y_values, dtypes_values=None):
  # Pie chart, where the slices will be ordered and plotted counter-clockwise:
  x_v1 =  [str(row[x_name]) for row in rows if row[x_name] not in['', None]]
  x_val_set = set(x_v1)
  x_vals = list(x_val_set)

  y_name = y_values[0]
  agg_dict = {}

  for xcategory in x_vals:
    agg_dict[xcategory] = 0

    for row in rows:

      x_name_value = str(row[x_name])

      if x_name_value == xcategory:
        if row[y_name]!=None and not math.isnan(row[y_name]):
          agg_dict[xcategory] += row[y_name]


  y_vals = list(agg_dict.values())
  x_names = list(agg_dict.keys())

  labels = x_names
  total_y_vals = sum(y_vals)

  sizes = [(y/total_y_vals)*100 for y in y_vals]

  number_of_colors = len(labels)
  colors = random.choices(list(mcolors.CSS4_COLORS.values()),k = number_of_colors)

  explode =[]
  for yv in sizes:
    if yv <=3:
      explode.append(0.3)
    elif yv <=8:
      explode.append(0.2)
    elif yv <= 15:
      explode.append(0.1)
    else:
      explode.append(0)

  plt.figure(figsize=(12, 10))

  # fig1, ax1 = plt.subplots()
  wedges, plt_labels, other = plt.pie(sizes, labels=labels,  explode=explode, autopct='%1.0f%%', rotatelabels=True,
           startangle=360, textprops={'fontsize': 14, 'fontweight': 'bold', 'color':'black'})
  # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  ll_labels = [f'{l}, {s: 0.1f}%' for l, s in zip(labels, sizes)]

  # plt.legend(labels=ll_labels, bbox_to_anchor=(1,0) , loc="lower right", bbox_transform=plt.gcf().transFigure)

  plt.tight_layout()


  # plt.show()
  plt.savefig('./media/generated_plot.png', bbox_inches="tight")
  plt.close()

# ..............................

def bar_chart(rows, x_name, y_values, dtypes_values=None):
    

  x_v1 = [str(row[x_name]) for row in rows if row[x_name] not in ['', None]]
  x_val_set = set(x_v1)
  x_vals = list(x_val_set)
  
  y_name = y_values[0]
  agg_dict = {}

  x_cats_lens = [len(x) for x in x_vals]
  max_len_xcat = max(x_cats_lens)

  for xcategory in x_vals:
    agg_dict[xcategory] = 0

    for row in rows:

      x_name_value = str(row[x_name])

      if x_name_value == xcategory:
        
        if row[y_name]!=None and not math.isnan(row[y_name]):
          agg_dict[xcategory] += row[y_name]

  if (max_len_xcat >= 5):
    agg_dict = {k: v for k, v in sorted(agg_dict.items(), key=lambda item: item[1], reverse=False)} #asc
  else:
    agg_dict = {k: v for k, v in sorted(agg_dict.items(), key=lambda item: item[1], reverse=True)} #desc

  y_vals = list(agg_dict.values())
  x_names = list(agg_dict.keys())

  print('\n\n', agg_dict)

  bars = x_names
  x_pos = np.arange(len(bars))
  heights = y_vals

  if(max_len_xcat >= 5):
    plt.barh(bars, y_vals )
    # Create names on the x-axis
    plt.xlabel(y_name, fontsize=14)
    plt.ylabel(x_name, fontsize=14)

    plt.grid(axis='x')
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_scientific(False)


  else:
    plt.bar(x_pos, heights)
    plt.xticks(x_pos, bars)
    if len(x_vals) > 5:
      plt.xticks(rotation=70, fontsize=12)
    plt.yticks(fontsize=12)

    plt.xlabel(x_name, fontsize=14)
    plt.ylabel(y_name, fontsize=14)
    plt.grid(axis='y')
    ax = plt.gca()
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    
  # Show graph

  plt.tight_layout()
  # plt.show()
  plt.savefig('./media/generated_plot.png')
  plt.close()
  return

# ............................


if __name__ == "__main__":
  rows = [
    {'date': 2006, 'close': 40, 'loss': 70, 'profit': 71},
    {'date': 2008, 'close': 45, 'loss': 33, 'profit': 31},
    {'date': 2010, 'close': 20, 'loss': 22, 'profit': 5},
    {'date': 2012, 'close': 51, 'loss': 29, 'profit': 30},
    {'date': 2014, 'close': 53, 'loss': 39, 'profit': 8},
    {'date': 2015, 'close': 57, 'loss': 49, 'profit': 10},
    {'date': 2017, 'close': 33, 'loss': 51, 'profit': 40},
    {'date': 2006, 'close': 40, 'loss': 70, 'profit': 71},
    {'date': 2008, 'close': 32, 'loss': 33, 'profit': 31},
    {'date': 2010, 'close': 20, 'loss': 22, 'profit': 5},
    {'date': 2012, 'close': 57, 'loss': 29, 'profit': 30},
    {'date': 2014, 'close': 63, 'loss': 39, 'profit': 8},
    {'date': 2015, 'close': 20, 'loss': 49, 'profit': 10},
    {'date': 2017, 'close': 66, 'loss': 51, 'profit': 40}
  ]
  x_name= 'date'
  y_names = ['close', 'profit']
  multiline_chart(rows, None, 'date', y_names)

