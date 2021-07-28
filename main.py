import pandas as pd
import numpy as np
#from PIL import Image
import streamlit as st
#from plotly.subplots import make_subplots
#import plotly.subplots as sp
# Suppress warnings 
import warnings
warnings.filterwarnings('ignore')
import streamlit as st
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

st.set_page_config(page_title="AllWomen database", 
                   page_icon=":computer:",
                   layout='wide')
                   
st.title("Welcome to the ***AllWomen*** database!  :computer: :star:")
"""
[Allwomen] (https://www.allwomen.tech/)
1. Overcome the fear of tech, maths and science.
Find a job in one of the fastest growing sectors.
Boost or shift your career
We believe that any background is the right background to become a woman in tech. That’s why we design our programs for you to go from 0 to 100, and we offer mentoring and assistance from beginning to end. 
Because your past shouldn’t be an obstacle in your future career!
"""


#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- SETTING UP THE APP
#--------------------------------- ---------------------------------  ---------------------------------
#title_image = Image.open("logo.jpg")
#st.image(title_image)
st.markdown("A Data Geek's take on the question ***'Do I have the right background to bla bla bla?'***")

st.header("**Overall information from our students**")
"""
Bla bla bla information from our students bla bla bla"""

# plot cards in grid
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
    axes.text(0.5, 0.6,  'Success ratio',ha='center', va='center',
                fontfamily='monospace', fontsize=50, fontweight='bold',
                color='#CEEFE8', backgroundcolor='#202020')
    axes.text(0.5, 0.3,+float(perc[perc['Course'] == options]['Percentage_job'].values),
          ha='center', va='center',
          fontfamily='monospace', fontsize=60, fontweight='bold',
          color='#CEEFE8', backgroundcolor=color)
    axes.set_axis_off()
    return fig


 
#Data loading and first checks
df = pd.read_csv('all_students_StreamlitCLEAN2.csv', index_col = 0)
df = df[(df['Course_general'] != 'Web Development') & (df['Course_general'] != 'Content Design & UX Writing')]

# Background
background = pd.read_csv('courses_bck_percentage.csv')
background = background[(background['Background'] != 'unknown')]

# Job success:
perc_r = pd.read_csv('percentage_job.csv', index_col = 0)

#---------------------------------------------------------------#
# OVERALL OVERVIEW THROUGH COURSES AND SETUP DATA
#---------------------------------------------------------------#
editions = df.groupby('Course_general')['Edition'].nunique().reset_index()
editions = editions.sort_values(by = ['Edition'], ascending = False)

# List of colors in function of each of the courses
colors = ['#3E5AFF', '#FFCAD3', '#FF642E', '#FFCD2C', '#C89AEF',' #202020']
color_courses = {df.Course_general.unique()[0]: colors[0], #Product
                      df.Course_general.unique()[1]: colors[1], #UX
                      df.Course_general.unique()[2]: colors[2], #DS
                      df.Course_general.unique()[3]: colors[3]} #DA}

col1, col2 = st.beta_columns(2)
with col1:
    columns1 = ['Student_ID', 'Native Country', 'Based in', 'Edition' ]
    colors_ = ['#C89AEF', '#3E5AFF', '#FF642E']
    ff = plot_card_total_number(df, columns1,colors_)
    st.pyplot(ff)
    columns2 = ['Course', 'Background', 'year', 'Job Position' ]
    colors_ = ['#202020', '#FFCD2C', '#C89AEF']
    ff2 = plot_card_total_number(df, columns2,colors_)
    st.pyplot(ff2)  
    ff3 = plot_card_Spain(df)
    st.pyplot(ff3)

num_students2 = round(df['Course_general'].value_counts(normalize=True)*100,2).reset_index()
num_students2.columns = ['Course', 'count']

with col2:
    st.subheader('Distribution of students_')
    # Creamos el primer gráfico (fig1)
    fig = px.bar(num_students2, x='Course', y = 'count',text='count',
                color = 'Course',color_discrete_map=color_courses)
    fig.update_traces(texttemplate='%{text:.2s} %', textposition='inside')
    st.plotly_chart(fig)

# Background
st.header('Background of our students')

all_courses = df.Course_general.unique().tolist()
st.header('**Select the course/s you want to explore**')
langs = st.multiselect(' ',options=all_courses, default=all_courses)

################ SELECT  BY COURSE ###########
col1, col2 = st.beta_columns(2)
plot_df = df[df.Course_general.isin(langs)]

#num_students = round(plot_df['Course_general'].value_counts(normalize=True)*100,2).reset_index()
#num_students.columns = ['Course', 'count']
based_grouped = plot_df.groupby(['Based in'])['Edition'].count().reset_index()
based_grouped = based_grouped.sort_values(by= ['Edition'], ascending=False)
country_grouped = plot_df.groupby(['Native Country'])['Edition'].count().reset_index().sort_values(by=['Edition'], ascending=False)
perc = perc_r.iloc[:4,:]
color_2 = {perc.Course.unique()[0]: colors[2], #Prod
                      perc.Course.unique()[1]: colors[0], #UX
                      perc.Course.unique()[2]: colors[4], #Web
                      perc.Course.unique()[3]: colors[1]} #DS}
colors_map = [ '#C89AEF','#FFCAD3','#FFCD2C','#FF642E'] 

with col1:
    st.subheader('From where our students are based in (top 10 locations, excluding Bcn)')
    fig1 = px.bar(based_grouped[1:11], x= 'Based in', y= 'Edition',
    text= 'Edition')
    st.plotly_chart(fig1)
    
with col2:
    st.subheader('From where our students come from')
    fig2 =  px.choropleth(country_grouped[1:], locations="Native Country",locationmode = 'country names',
                        color="Edition",color_continuous_scale= colors_map)                 
    st.plotly_chart(fig2)

col1, col2 = st.beta_columns(2)
with col1:
    st.subheader('Background of our students')

    fig = px.bar(background, x="Background", y='percentage', color= 'Courses',
                labels = {'Background':'Academic background',
                 'percentage': '% of students'},
                 color_discrete_map = color_courses)
    st.plotly_chart(fig)
with col2:
    st.subheader('Students that found a job linked to the studied Course')
    fig = px.bar(perc_r[:-1], x='Course', y = 'Percentage_job',
    text='Percentage_job',
            color = 'Course',color_discrete_map = color_courses,
            labels = {'Course': 'Course','Percentage_job': '% of students'}
            )

    fig.update_traces(texttemplate='%{text:.2s} %', textposition='inside')
    st.plotly_chart(fig)


#---------------------------------------------------------------#
# IN DEEP OVERVIEW OF THE COURSES
#---------------------------------------------------------------#
st.title('Dive into the courses!')
# Drop the students from the current editions
df = df[(df['Edition'] != 'Mar-Sep 2021')&(df['Edition'] != 'Feb-Apr 2021')&
       (df['Edition'] != 'Mar-Sep 2021')& (df['Edition'] != 'May-Jul 2021') &
        (df['Edition'] != 'Apr-Jul 2021') &(df['Edition'] != 'May-Nov 2021')]

#---------------------------------------------------------------#
# BACKGROUND OF THE COURSES
#---------------------------------------------------------------#

all_courses = df.Course_general.unique().tolist()

options = st.selectbox(
 'Which course are you interested in?', all_courses)
#st.write('You selected:', options)
#st.subheader('Background in function of the course')
ds = df[df.Course_general == options]

ds.Background.unique()
# Background arrangement
overall_ds = ds['Background'].value_counts(normalize=True).reset_index()
overall_ds.columns = ['Background', 'percentage']
overall_ds['Course'] = str(str(options))
overall_ds['percentage'] = round(overall_ds['percentage']*100,2)

col1, col2 = st.beta_columns(2)
row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3 = st.beta_columns(
    (.1, 1.6, .1, 1.6, .1)
    )
with col1:
    st.subheader(f"Background for {options} Course")
    fig = px.bar(overall_ds[:15], x= 'Background', y= 'percentage', text='percentage',
                     color_discrete_sequence=[select_color(options)])
    fig.update_traces(texttemplate='%{text:.3s} %', textposition='outside')
    st.plotly_chart(fig)

# Success ratio arrangement in function of the years
#success_students = ds[ds['success'] == 1].groupby('year')['Job Position'].count().reset_index().rename(columns={'index': 'year', 'Job Position': 'total_number'})
#success_students['total_students'] = ds.groupby('year')['Course_general'].count().reset_index()['Course_general']
#success_students.columns = ['year', 'success','total_students']
#success_students['ratio'] = round(success_students['success']/ success_students['total_students']*100,2)

#---------------------------------------------------------------#
# JOBS OF THE COURSES
#---------------------------------------------------------------#  
with col2:
    st.subheader(f"Success ratio over years for {options} Course")
    fig3 = show_text(perc_r, options,select_color(options))
    st.pyplot(fig3)
    st.header(f"Top Job positions  for {options} Course")
    # Create and generate a word cloud image:
    wordcloud = WordCloud(max_words= 10, 
    background_color="white", 
                   collocations= True, 
                   max_font_size= 500).generate("".join(ds['Job Position']))
        
    # Display the generated image:
    plt.imshow(wordcloud)
    st.image(wordcloud.to_array())
    
