import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def plot_card_total_number(df, columns, colors):      
    col = list(columns) 
    fig, axes = plt.subplots(1, 4, figsize=(24, 4))
    axes = axes.flatten()
    
    for ind, col in enumerate(col):
        axes[ind].text(0.5, 0.6,  col, 
                ha='center', va='center',
                fontfamily='monospace', fontsize=40, fontweight='bold',
                color=colors[0], backgroundcolor=colors[1])
        axes[ind].text(0.5, 0.3,+ df[col].nunique(), 
                ha='center', va='center',
                fontfamily='monospace', fontsize=48, fontweight='bold',
                color=colors[2], backgroundcolor='white')
        axes[ind].set_axis_off()
    return fig

def plot_card_Spain(df): 
    spanish = df[df['Native Country'] == 'Spain']['Native Country']  
    bcn =df[df['Based in'] == 'Barcelona'] ['Based in']
    df = pd.concat([spanish, bcn], axis=1)
    df.columns = ['Spanish students', 'Bcn based students']
    col = df.columns

    fig, axes = plt.subplots(1, 2, figsize=(24, 4))
    axes = axes.flatten()
    
    for ind, col in enumerate(col):
        axes[ind].text(0.5, 0.6,  col, 
                ha='center', va='center',
                fontfamily='monospace', fontsize=40, fontweight='bold',
                color=colors[0], backgroundcolor=colors[1])
        
        axes[ind].text(0.5, 0.3,+df[col].count(), 
                ha='center', va='center',
                fontfamily='monospace', fontsize=48, fontweight='bold',
                color='#FFCD2C', backgroundcolor='white')
        axes[ind].set_axis_off()
    return fig  

def select_color(options):
    colors = ['#3E5AFF', '#FFCAD3', '#FF642E', '#FFCD2C', '#C89AEF',' #202020']
    colors_ = []
    if options == df.Course_general.unique()[0]:  
        return colors[0]
    elif options == df.Course_general.unique()[1]:  
        return colors[1]
    elif str(options) ==df.Course_general.unique()[2]:
        return colors[2]
    elif str(options) == df.Course_general.unique()[3]: 
        return colors[3] 
    
def show_text(perc, options, color):
    fig, axes = plt.subplots(1, 1, figsize=(24, 4))
    axes.text(0.3, 0.6,  'Success ratio',ha='center', va='center',
                fontfamily='monospace', fontsize=50, fontweight='bold',
                color='#CEEFE8', backgroundcolor='#202020')
    axes.text(0.3, 0.3,+float(perc[perc['Course'] == options]['Percentage_job'].values),
          ha='center', va='center',
          fontfamily='monospace', fontsize=60, fontweight='bold',
          color='#CEEFE8', backgroundcolor=color)
    axes.set_axis_off()
    return fig
