# Description : This is a sentiment analysis program that parses the tweets fetched from Twitter using Python
# Group - Ayushi
#		- Harika
# 		- Gaurav
# 		- Kartik



# Importing All Libraries
import streamlit as st
from auth import auth
from Dataframe import *
import numpy as np
from PIL import Image
from wordclouder import plot_wordcloud
st.set_option('deprecation.showPyplotGlobalUse', False)

st.write("""
	# Twitter Sentiment Analysis✨
	""")

# Authenticate Twiter

api = auth()

username = st.text_input("Username ", "BillGates")
no_of_tweets = st.slider('No Of Tweets', 0, 250, 25)
# no_of_tweets = st.text_input("No Of Tweets ", 100)

if st.button('Submit'):
	# Extract 100 tweets from the Twitter User - Harika
	posts = api.user_timeline(screen_name = username, count = no_of_tweets , lang = "en" , tweet_mode="extended")
	st.write(""" ## Show the 5 recent tweets of - """  + username)

	# Creating dataframe of the posts fetched
	df = dataframe(posts)
	st.dataframe(df.head() , width=2048, height=768)

	#Showing Time series of the User tweets over the year
	st.write(""" # Plotting the Time series of the User Tweets""")
	timeseries(df)
	
	# Cleaning the tweets
	st.write(""" # Cleaning the Tweets""")
	df['Tweets'] = df['Tweets'].apply(cleanTxt)
	for tweet in df['Tweets'][0:5]:
		st.write(tweet)

	# Getting Subjectivity and polarity
	st.write(""" # Getting the Subjectivity and the Polarity""")
	df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
	df['Polarity'] = df['Tweets'].apply(getPolarity)
	st.dataframe(df.head() , width=2048, height=768)

	# Creating wordcloud
	allWords = ' '.join( [twts for twts in df['Tweets']] )
	pos_mask = np.array(Image.open('twitter_mask.png'))
	plot_wordcloud(allWords,mask=pos_mask,color='white',max_font_size=50,title_size=10,title="WordCloud of all Tweets")


	# Getting Analysis using the polarity and subjectivity - Ayushi
	st.write(""" # Analysis of the Tweets""")
	df['Analysis'] = df['Polarity'].apply(getAnalysis)
	st.dataframe(df.head() , width=2048, height=768)


	# Scatter plot of the Analysis 
	st.write(""" # Scatterplot of the Tweets by - """ + username)
	scatterplot(df)

	# ptweets and ntweets
	st.write(""" # Postivite and Negtaive Tweets by - """ + username)
	st.write(""" ### Postivite Tweets = """ + str(ptweets(df)))
	st.write(""" ### Negative Tweets = """ + str(ntweets(df)))

	# Temperature plot
	temp(df)

	# Setiment analysis bar plot
	st.write(""" # Sentiment Analysis Bar Plot""")
	analysisplot(df)


	# Funnel chart
	st.write(""" # Sentiment Analysis Funnel Plot""")
	funnelchart(df)



# interactive Shell
st.write("""
	# Interactive Tweet Analysis ✨
""")

temp = st.text_input("Enter a Tweet")
if st.button("Analyse !!!"):
	temp = cleanTxt(temp)
	st.write(""" ### Cleaned Tweet =  """ + temp)
	polarity = getPolarity(temp)
	st.write(""" ### Polarity of the  Tweet =  """ + str(polarity))
	subjectivity = getSubjectivity(temp)
	st.write(""" ### Subjectivity of the  Tweet =  """ + str(subjectivity))
	temp = getAnalysis(polarity)
	st.write(""" ### Analysis of the  Tweet =  """ + temp)

st.markdown("<h1 style='text-align: center; color: white;'>✨ Thankyou ✨</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>✨ Made by Group  ✨</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'> Ayushi Agarwal - 17070122012 </h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'> Harika Challa - 17070122017</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'> Gaurav Joshi - 17070122021</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'> Kartik Bhushan - 17070122028</h4>", unsafe_allow_html=True)


# The End #