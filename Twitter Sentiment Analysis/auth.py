import tweepy
import pandas as pd

def auth():
	log = pd.read_csv('twitter.csv')
	consumerKey = log['key'][0]
	consumerSecret = log['key'][1]
	accessToken = log['key'][2]
	accessTokenSecret = log['key'][3]

	authenticate = tweepy.OAuthHandler(consumer_key= consumerKey, consumer_secret= consumerSecret)

	# Set the Access token and Access Token Secret 
	authenticate.set_access_token(accessToken, accessTokenSecret)

	# Create the API object while passing the authentication information
	api = tweepy.API(auth_handler = authenticate, wait_on_rate_limit= True)

	return api