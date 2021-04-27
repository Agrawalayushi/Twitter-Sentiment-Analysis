from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
plt.style.use('fivethirtyeight')

def dataframe(posts):
	df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
	df['Date'] = ([tweet.created_at for tweet in posts])
	df['Retweets'] = ([tweet.retweet_count for tweet in posts])
	df['Likes'] = ([tweet.favorite_count for tweet in posts])
	return df

def timeseries(df):
	time_likes = pd.Series(data=df['Likes'].values, index= df['Date'])
	time_likes.plot(figsize=(16,4), label = "Likes", legend = True )
	time_retweets = pd.Series(data=df['Retweets'].values, index= df['Date'])
	time_retweets.plot(figsize=(16,4), label = "Retweets", legend = True )
	plt.show()
	st.pyplot()

# Cleaning the tweets in the dataframe
def cleanTxt(text):
  text = re.sub(r'@[A-Za-z0-9]+' , '' , text) # removes @ Symbols
  text = re.sub(r'#' , '' , text) # removes # Symbols
  text = re.sub(r'RT[\s]+' , '' , text) # removes RT (retweet)
  text = re.sub(r'https?:\/\/\S+' , '' , text) # removes the hyperlink=
  return text


# Creating a function to get the subjectivity
def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

# Creating a function to get the Polarity
def getPolarity(text):
  return TextBlob(text).sentiment.polarity


# Function to compute Negative , Netural and positive analysis
def getAnalysis(score):
  if score < 0 :
    return 'Negative'
  elif score == 0 :
    return 'Netural'
  else :
    return 'Positive'

def scatterplot(df):
	# Plot the Polarity and Subjectivity
	plt.figure(figsize=(5,5))
	for i in range(0,df.shape[0]):
	    plt.scatter(df["Polarity"][i], df["Subjectivity"][i], color='Blue') 

	plt.title('Sentiment Analysis') 
	plt.xlabel('Polarity') 
	plt.ylabel('Subjectivity') 
	plt.show()
	st.pyplot(dpi = 1000)

def ptweets(df):
	ptweets = df[df.Analysis == 'Positive']
	ptweets = ptweets['Tweets']
	ptweet = round((ptweets.shape[0] / df.shape[0]) * 100 , 1)
	return ptweet

def ntweets(df):
	ntweets = df[df.Analysis == 'Negative']
	ntweets = ntweets['Tweets']
	ntweet = round((ntweets.shape[0] / df.shape[0]) * 100 , 1)
	return ntweet

def analysisplot(df):
	#plot and visualize the count
	plt.title('Sentiment Analysis')
	plt.xlabel('Sentiment')
	plt.ylabel('Counts')
	df['Analysis'].value_counts().plot(kind = 'bar')
	plt.show()
	st.pyplot(dpi = 1000)

def temp(df):
	temp = df.groupby('Analysis').count()['Tweets'].reset_index().sort_values(by='Tweets',ascending=False)
	st.write(temp.style.background_gradient(cmap='Purples'))


def funnelchart(df):
	temp = df.groupby('Analysis').count()['Tweets'].reset_index().sort_values(by='Tweets',ascending=False)
	fig = go.Figure(go.Funnelarea(text =temp.Analysis,values = temp.Tweets,title = {"position": "top center", "text": "Funnel-Chart of Sentiment Distribution"}))
	fig.update_layout(title = " Funnel Plot " , autosize = False , width = 800 , height = 800 , margin=dict(l=40, r=40, b=40, t=40))
	st.plotly_chart(fig)