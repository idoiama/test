import pandas as pd
from nltk.stem import WordNetLemmatizer
import string
import re
import numpy as np
from PIL import Image
import streamlit as st
from plotly.subplots import make_subplots
import plotly.subplots as sp
# Suppress warnings 
import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="AllWomen database", 
                   page_icon=":computer:",
                   layout='centered')
                   
st.header("Welcome to the ***AllWomen*** database!  :computer: :star:")
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
title_image = Image.open("logo.jpg")
#st.image(title_image)
st.markdown("A Data Geek's take on the question ***'Do I have the right background to bla bla bla?'***")

st.header("Overall information from our students")
"""
Bla bla bla information from our students bla bla bla"""


def clean_text(text):
    '''Make text lowercase, remove text in square brackets,
    remove links,remove punctuation
    and remove words containing numbers.'''
    
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text) #words --> 
    return text

# text preprocessing function
def text_preprocessing(text):
    """
    Cleaning and parsing the text.
    
    """
    from nltk.corpus import stopwords
    from nltk.stem.wordnet import WordNetLemmatizer

    # Lower case and remove punctuations
    nopunc = clean_text(text)
    
    # Tokenize the text
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    tokenized_text = tokenizer.tokenize(nopunc)
    
    #Lemmatize the text
    lemmatizer = WordNetLemmatizer()
    lem_words = [lemmatizer.lemmatize(w,'v') for w in tokenized_text]

    # Remove stopwords  
    remove_stopwords = [w for w in lem_words if w not in stopwords.words('english')]    
    combined_text = ' '.join(remove_stopwords)
    return combined_text

def pretty(s: str) -> str:
    try:
        return dict(js="JavaScript")[s]
    except KeyError:
        return s.capitalize()
#Data loading and first checks
df = pd.read_csv('data_streamlit.csv', index_col = 0)

#---------------------------------------------------------------#
# OVERALL OVERVIEW THROUGH COURSES AND SETUP DATA
#---------------------------------------------------------------#
editions = df.groupby('Course_general')['Edition'].nunique().reset_index()
editions = editions.sort_values(by = ['Edition'], ascending = False)


# ## List of colors in function of each of the courses
colors = ['#3E5AFF', '#FFCAD3', '#FF642E', '#FFCD2C', '#C89AEF',' #202020']
color_discrete_map = {df.Course_general.unique()[0]: colors[2], 
                      df.Course_general.unique()[1]: colors[1], 
                      df.Course_general.unique()[2]: colors[2],
                      df.Course_general.unique()[3]: colors[0],
                      df.Course_general.unique()[4]: colors[3],
                      df.Course_general.unique()[5]: colors[4]
                     }

# Excluding the new courses (UX writing and Web development)
df2 = df[(df['Course_general'] != 'Web Development') & (df['Course_general'] != 'Content Design & UX Writing')]
num_students2 = round(df2['Course_general'].value_counts(normalize=True)*100,2).reset_index()
num_students2.columns = ['Course', 'count']
#grouped2 = df.groupby(['Based in'])['Edition'].count().reset_index()
#grouped2 = grouped2.sort_values(by= ['Edition'], ascending=False)

st.subheader('Distribution of students:')
# Creamos el primer gráfico (fig1)
fig = px.bar(num_students2, x='Course', y = 'count',text='count',
            color = 'Course',color_discrete_map=color_discrete_map,
            title="Percentage students per course")
fig.update_traces(texttemplate='%{text:.2s} %', textposition='inside')
fig.update_layout(title=("blabla"))
st.plotly_chart(fig)


################ SELECT ###########
all_courses = df2.Course_general.unique().tolist()
langs = st.multiselect(
    "Which course/s do you want to explore?", options=all_courses, default=all_courses, format_func=pretty
    
)

col1, col2 = st.beta_columns([3,2])
plot_df = df2[df2.Course_general.isin(langs)]
num_students2 = round(plot_df['Course_general'].value_counts(normalize=True)*100,2).reset_index()
num_students2.columns = ['Course', 'count']
grouped2 = plot_df.groupby(['Based in'])['Edition'].count().reset_index()
grouped2 = grouped2.sort_values(by= ['Edition'], ascending=False)
grouped = plot_df.groupby(['Native Country'])['Edition'].count().reset_index().sort_values(by=['Edition'], ascending=False)

with col1:
    st.subheader('Where our students are based in')
    # Creamos el primer gráfico (fig1)
    fig1 = px.bar(grouped2[1:10], x= 'Based in', y= 'Edition',text= 'Edition',
                color_discrete_map=color_discrete_map,
                 title="Location of students per country, excluding Bcn")
    st.plotly_chart(fig1)

# Creamos el segundo gráfico (fig2)
with col2:
    st.subheader('Where our students come from')
    fig2 =  px.choropleth(grouped[1:], locations="Native Country",locationmode = 'country names',
                        color="Edition")                 
    st.plotly_chart(fig2)


# Drop the students from the current editions
df = df[(df['Edition'] != 'Mar-Sep 2021')&(df['Edition'] != 'Feb-Apr 2021')&
       (df['Edition'] != 'Mar-Sep 2021')& (df['Edition'] != 'May-Jul 2021') &
        (df['Edition'] != 'Apr-Jul 2021') &(df['Edition'] != 'May-Nov 2021')]
