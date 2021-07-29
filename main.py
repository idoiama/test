import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from functions_ import *


## PAGE STYLING
st.set_page_config(page_title="AllWomen database", 
                   page_icon=":computer:",
                   layout='wide')
                   
st.title("Welcome to the ***AllWomen*** database!  :computer: :star:")
"""
[Allwomen] (https://www.allwomen.tech/)
Bla bla bla information from our students bla bla bla
Bla bla bla information from our students bla bla bla
We believe that any background is the right background to become a woman in tech. That’s why we design our programs for you to go from 0 to 100, and we offer mentoring and assistance from beginning to end. 
Because your past shouldn’t be an obstacle in your future career!
"""

#-------------------------------------------------------------------------------------------------------
#--------------------------------- SETTING UP THE APP
#--------------------------------- ---------------------------------------------------------------------
#title_image = Image.open("logo.jpg")
#st.image(title_image)
st.markdown("A Data Geek's take on the question ***'Do I have the right background to bla bla bla?'***")

st.header("**Overall information from our students**")
"""
Bla bla bla information from our students bla bla bla"""

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
#editions = df.groupby('Course_general')['Edition'].nunique().reset_index()
#editions = editions.sort_values(by = ['Edition'], ascending = False)
    
# List of colors in function of each of the courses
colors = ['#3E5AFF', '#FFCAD3', '#FF642E', '#FFCD2C', '#C89AEF',' #202020']
color_courses = {df.Course_general.unique()[0]: colors[0], #Product
                      df.Course_general.unique()[1]: colors[1], #UX
                      df.Course_general.unique()[2]: colors[2], #DS
                      df.Course_general.unique()[3]: colors[3]} #DA}

num_students = round(df['Course_general'].value_counts(normalize=True)*100,2).reset_index()
num_students.columns = ['Course', 'count']

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

with col2:
    st.subheader('Distribution of our students in all courses')
    fig = px.bar(num_students, x='Course', y = 'count',text='count',
                color = 'Course',color_discrete_map=color_courses)
    fig.update_traces(texttemplate='%{text:.2s} %', textposition='inside')
    st.plotly_chart(fig)

# Background
st.header("**Let's have an overall look at our student database!**")

all_courses = df.Course_general.unique().tolist()
st.subheader('**Select the course/s you want to explore**')
langs = st.multiselect(' ',options=all_courses, default=all_courses)

################ FILTER BY COURSE ###########
plot_df = df[df.Course_general.isin(langs)]

based_grouped = plot_df.groupby(['Based in'])['Edition'].count().reset_index()
based_grouped = based_grouped.sort_values(by= ['Edition'], ascending=False)
country_grouped = plot_df.groupby(['Native Country'])['Edition'].count().reset_index().sort_values(by=['Edition'], ascending=False)
perc = perc_r.iloc[:5,:]

#Re-arrangement of the colors per course (percentage)
color_perc = {perc.Course.unique()[0]: colors[2], #DS-FT
                      perc.Course.unique()[1]: colors[0], #Prod
                      perc.Course.unique()[2]: '#f59371', #DS-PT
                      perc.Course.unique()[3]: colors[1], #UX/UI
                      perc.Course.unique()[4]: colors[3]} #DA
colors_map = [ '#C89AEF','#FFCAD3','#FFCD2C','#FF642E'] 

col1, col2 = st.beta_columns(2)
with col1:
    st.subheader('From where our students are located in  (excluding Bcn)')
    fig1 = px.bar(based_grouped[1:11], x= 'Based in', y= 'Edition',
    text= 'Edition')
    st.plotly_chart(fig1)
    
with col2:
    st.subheader('From where our students come from (excluding Spain)')
    fig2 =  px.choropleth(country_grouped[1:], locations="Native Country",locationmode = 'country names',
                        color="Edition",color_continuous_scale= colors_map)                 
    st.plotly_chart(fig2)
    
col1, col2 = st.beta_columns(2)
with col1:
    st.subheader('Academic background distribution per courses')
    st.markdown('The total number of female students in each background was considered and represented their percentage per course.')
    fig = px.bar(background, x="Background", y='percentage', color= 'Courses',
                labels = {'Background':'Academic background',
                 'percentage': '% of students'},
                 color_discrete_map = color_courses)
    st.plotly_chart(fig)
with col2:
    st.subheader('Ratio of the students that found a job linked to the Course')
    fig = px.bar(perc_r[:-1], x='Course', y = 'Percentage_job',
    text='Percentage_job',
            color = 'Course',color_discrete_map = color_perc,
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

course = df[df.Course_general == options]

# Background arrangement
overall = round(course['Background'].value_counts(normalize=True)*100,2).reset_index()
overall.columns = ['Background', 'percentage']
overall = overall[(overall['Background'] != 'unknown') & (overall['Background'] != 'education')]


col1, col2 = st.beta_columns(2)

with col1:
    st.subheader(f"[{options}] - Their backgrounds")
    fig = px.bar(overall[:15], x= 'Background', y= 'percentage', text='percentage',
                     color_discrete_sequence=[select_color(options,df)])
    fig.update_traces(texttemplate='%{text:.3s} %', textposition='outside')
    st.plotly_chart(fig)

#---------------------------------------------------------------#
# JOBS SUCCESS OF THE COURSES
#---------------------------------------------------------------#  
with col2:
    fig3 = show_text(perc_r, options,select_color(options,df))
    st.pyplot(fig3)
    st.subheader(f"Top words according to their job positions")
    st.markdown("The higher the size, the more frequent the word is")
    # Create and generate a word cloud image:
    wordcloud = WordCloud(max_words= 50, 
    background_color="white", 
                   collocations= False,color_func=lambda *args, **kwargs: select_color(options,df), 
                   max_font_size= 500).generate(" ".join(course['clean_job']))
        
    #plt.imshow(wordcloud)
    st.image(wordcloud.to_array())
  
