#!/usr/bin/python
# Chirpy v. 0.1.0 
#
# About: A Python library for Twitter, which does not need any OAUTH authentication. Diving in Twitter has never been so easy.
# Warning: for security reasons, do not use this tool with your personal Twitter account
# Author: picus
#
# Acknowledgements: codezero & Ant-Man for starting code and the idea
#
# Requirements:
# - Python 2.7
# - Python Requests Module
#  
# License: GNU GENERAL PUBLIC LICENSE Version 3
#


import requests
from lxml.html import fromstring
from urllib import quote
import time 

class Twitter():
    def __init__(self, username, password):
	"""
	:param str username: username
	:param str password: password	
	"""
        self.username = username
        self.password = password
        self.is_logged = False
        try:
            self.bot = requests.Session()
        except:
            self.bot = None
	    raise Exception("Error: session not created.")
    
    #Actions

    def login(self):
	"""Login to Twitter with the username and password set in __init__."""
        if self.bot:
            url = 'https://mobile.twitter.com/session'
            response = self.bot.get(url)
            html = fromstring(response.content)    
            payload = dict(html.forms[0].fields)
            #email and password
            payload.update({
                'username': self.username,
                'password': self.password,
            })
   
            c = self.bot.post(url, data=payload)
            if "https://mobile.twitter.com/login/error" in c.url:
        	raise LoginException()
	    else:
                self.is_logged = True


    def logout(self):
	"""Logout from Twitter"""
   	if self.is_logged:
		url='https://mobile.twitter.com/account'
		response = self.bot.get(url)
        	html = fromstring(response.content)
                payload = dict(html.xpath('//form[@class="logout-form"]')[0].fields)
            	c = self.bot.post(url, data=payload)
		if "https://mobile.twitter.com/login" in c.url:
			self.is_logged=False
			  

    def is_logged(self):
	"""Check if the user is logged or not.
	
	:return: a boolean
	"""
	return self.is_logged

    def follow(self,username):
	"""Follow the user with the specified username.

	:param str username: specifies the screen_name of the user
	:return: a boolean stating if the operation has succeeded
	"""
	url="https://mobile.twitter.com/"+username+"/follow"
        response = self.bot.get(url) 
	html=fromstring(response.content)
	payload=dict(html.forms[0].fields)
	output=self.bot.post(url,data=payload)
	if "following#"+username in output.url:
		return True
	else: 
		return False

	
    def unfollow(self,username):
	"""Unfollow the user with the specified username.

	:param str username: specifies the screen_name of the user	
	:return: a boolean stating if the operation has succeeded
	"""
	url="https://mobile.twitter.com/"+username+"/unfollow"
	response = self.bot.get(url) 
	html=fromstring(response.content)
	payload=dict(html.forms[0].fields)
	output=self.bot.post(url,data=payload)
	if "https://mobile.twitter.com/"+username in output.url:
		return True
	else: 
		return False


    def tweet(self, message):
	"""Send a tweet with the specified message.
	
	:param str message: specifies the content of the tweet
	"""
        if self.bot and self.is_logged:
            url = 'https://mobile.twitter.com/compose/tweet'
            response = self.bot.get(url)
            html = fromstring(response.content)
            payload = dict(html.forms[0].fields)
            payload.update({
                'tweet[text]': message
            })
            self.bot.post("https://mobile.twitter.com/compose/tweet", data =payload)


    def tweet_reply(self,username,tweet_id,message):
	"""Send a reply to the specified tweet.

   	:param str username: specifies the screen_name of the user
	:param str tweet_id: specifies the id of the tweet to reply
	:param str message: specifies the content of the reply
	"""
	url="https://mobile.twitter.com/"+username+"/reply/"+tweet_id
	response = self.bot.get(url) 
	html=fromstring(response.content)
	payload = dict(html.forms[0].fields)
        payload.update({'tweet[text]': payload["tweet[text]"]+message})
        self.bot.post("https://mobile.twitter.com/compose/tweet", data =payload)


    def tweet_retweet(self,tweet_id):
	"""Retweet the specified tweet.

	:param str tweet_id: specified the id of the tweet to retweet
	:return: a boolean stating if the operation has succeeded
	"""
	url="https://mobile.twitter.com/statuses/"+tweet_id+"/retweet"
	response = self.bot.get(url) 
	html=fromstring(response.content)
	payload=dict(html.forms[0].fields)
	output=self.bot.post(url,data=payload)
	if "https://mobile.twitter.com/#tweet_"+tweet_id in output.url:
		return True
	else:
		return False


    def tweet_like(self,username,tweet_id):
	"""Like the specified tweet.

	:param str username: specifies the screen_name of the user
	:param str tweet_id: specified the id of the tweet to like
	"""
	url="https://mobile.twitter.com/"+username+"/status/"+tweet_id
	response = self.bot.get(url) 
	html=fromstring(response.content)	
	like_url=html.xpath('//a[@class="favorite"]/@href')[0]
	self.bot.get("https://mobile.twitter.com/"+like_url)
	

    def block_user(self,username):
	"""Block the specified user.

	:param str username: specifies the screen_name of the user to block
	"""
	url="https://mobile.twitter.com/"+username+"/actions"
	response = self.bot.get(url) 
	html=fromstring(response.content)
	payload=dict(html.forms[2].fields)
	output=self.bot.post("https://mobile.twitter.com/"+username+"/block",data=payload)

	
    def report_spam_user(self,username):
	"""Report the username for spam.
	
	:param str username: specifies the screen_name of the user to report for spam	
	"""
	url="https://mobile.twitter.com/"+username+"/actions"
	response = self.bot.get(url) 
	html=fromstring(response.content)
	payload=dict(html.forms[3].fields)
	output=self.bot.post("https://mobile.twitter.com/"+username+"/spam",data=payload)
	

    #Search functionalities

    def get_user_info(self,username):
    	"""Return a set of information about the user specified in input. This method is run anonymously (without any Session active).

	:param str user: specifies the screen_name of the user
	:return: a dictionary including keys "username","tweets","following","followers","location","bio","url" as details of the user
	"""
	userInfo={}
	url = 'https://mobile.twitter.com/'+username
	response = requests.get(url)#self.bot.get(url)
	html=fromstring(response.content)
	userInfo["username"]=username	    
	#get stats
	values=html.xpath('//div[@class="statnum"]/text()')
	if(values):	
		userInfo["tweets"]=values[0]
		userInfo["following"]=values[1]
		userInfo["followers"]=values[2]
	else:
		userInfo["tweets"]=''
		userInfo["following"]=''
		userInfo["followers"]=''
	#get location
	location=html.xpath('//div[@class="location"]/text()')
	if(location):
		userInfo["location"]=location[0]
	else:
		userInfo["location"]=''		
 	#bio
	bio=html.xpath('//div[@class="bio"]/div/text()')
	if(bio):
		userInfo["bio"]=bio[0].strip(" \n")
	else:
		userInfo["bio"]=''
	url=html.xpath('//div[@class="url"]/div/a/text()')
	if(url):
		userInfo["url"]=url[0]
	else:
		userInfo["url"]=''
        return userInfo	

    def get_followers(self,username,max_num):
	"""Return a list of followers of the specified user. This method is run anonymously (without any Session active).

	:param str username: specifies the screen_name of the user
	:param int max_num: specifies the number of following users to get
	:return: a list of screen_name of following users
	"""
	return self.__get_user_list('followers',username,max_num)

    def get_following(self,username,max_num):
	"""Return a list of users followed by the specified user. This method is run anonymously (without any Session active).

	:param str username: specifies the screen_name of the user
	:param int max_num: specifies the number of following users to get
	:return: a list of screen_name of following users
	"""
	return self.__get_user_list('following',username,max_num)

    def __get_user_list(self,search_type,username,max_num):
	
	user_list=[]
	url = 'https://mobile.twitter.com/'+username+'/'+search_type
	while(len(user_list)<max_num and url!=''):
		response = requests.get(url)#self.bot.get(url)
		html=fromstring(response.content)
		 
		user_list.extend(html.xpath('//td[contains(@class,"info") and contains(@class,"fifty") and contains(@class,"screenname")]/a/@name')) 			
		more_button=html.xpath('//div[@class="w-button-more"]/a/@href')
		if(more_button):
			url="http://mobile.twitter.com/"+str(more_button[0])
		else:
			url=''
        #resize if needed
        if(len(user_list)>max_num):
		user_list=user_list[0:max_num]
	return user_list



    def search_users(self,searchterm,max_num):
	"""Search for users according to the search term. This method is run anonymously (without any Session active).
		
	:param str searchterm: specifies the search term
	:param int max_num: specifies the number of users to get
	:return: a list of screen_name of users	
	"""
	user_list=[]
	url='https://mobile.twitter.com/search/users?q='+searchterm
	while(len(user_list)<max_num and url!=''):
		response = requests.get(url)#self.bot.get(url) 
	        html=fromstring(response.content)
		user_list=html.xpath('//div[@class="user-list"]')
		user_items=[]
		if(user_list):
			user_items=html.xpath('//div[@class="user-list"]')[0].findall('.//table')	
		for user in user_items:
			user=user.xpath('.//tr/td[2]/a/@name')[0]
			user_list.append(user)
			if(len(user_list)==max_num):
				break
		more_button=html.xpath('//div[@class="w-button-more"]/a/@href')
		if(more_button):
			url="https://mobile.twitter.com"+str(more_button[0])
		else:
			url=''

	return user_list
	

    def get_tweets(self,screen_name,max_num):
	"""Return at most max_num tweets from the username timeline. This method is run anonymously (without any Session active).

	:param str username: specifies the screen_name of the user
	:param int max_num: specifies the number of tweets to get 
	:return: a list of dictionaries including keys "id" of the tweet and "author"
	"""
	tweets=[]
	url = 'https://mobile.twitter.com/'+username
	while(len(tweets)<max_num and url!=''):
		response = requests.get(url)#self.bot.get(url) 
	        html=fromstring(response.content)
		timeline=html.xpath('//div[@class="timeline"]')
		tweet_items=[]
		if(timeline):
			tweet_items=timeline[0].findall('.//table')
		for item in tweet_items[1:]:
			tbody=item.getchildren()[0]
			tweet={}
			tweet["id"]=item.xpath('.//div[@class="tweet-text"]/@data-id')[0]			
			
			#check if retweeted
			author=item.xpath('.//div[@class="username"]/text()')[1].strip(" \n")
			if(author!=username):
				tweet["author"]=author
			else:
				tweet["author"]=username
			tweets.append(tweet)
			if(len(tweets)==max_num):
				break
		more_button=html.xpath('//div[@class="w-button-more"]/a/@href')
		if(more_button):
			url="https://mobile.twitter.com"+str(more_button[0])
		else:
			url=''

	return tweets

    def get_tweet_info(self,username,tweet_id):
	"""Return details about the specified tweet. This method is run anonymously (without any Session active).
	
	:param str username: the author of the tweet
	:param str tweet_id: the id of the tweet
	:return: a dictionary including the keys "id","username","date","time","text","hashtags","retweet","likes" as details of the tweet
	"""
    	url = 'https://mobile.twitter.com/'+username+"/status/"+tweet_id
	response = requests.get(url)#self.bot.get(url) 
	html=fromstring(response.content)	
	tweet={} 
	tweet["id"]=tweet_id
	tweet["username"]=username
	datetime=html.xpath('//td[@class="tweet-content"]/div[@class="metadata"]/a/text()')[0]
	tweet["date"]=datetime.split("-")[1].strip()
	tweet["time"]=datetime.split("-")[0].strip()
        tweet["text"]=html.xpath('//div[@class="tweet-text"]')[0].text_content().strip(" \n")
	tweet["hashtags"]=html.xpath('//a[@data-query-source="hashtag_click"]/text()')
	   
	stats=html.xpath('//td[@class="stat"]/span')
	for stat in stats:
		value=stat.xpath('.//span[@class="statnum"]/text()')[0]
	        label=stat.xpath('.//span[@class="statlabel"]/text()')[0]
		if(label.lower()=="retweet"):
			tweet["retweet"]=value
		else:
			tweet["likes"]=value

     	return tweet

    def search_tweets(self,searchterm,max_num):
	"""Search for tweets according to the search terms. This method is run anonymously (without any Session active).

	:param str searchterm: specifies the search term
	:param int max_num: specifies the number of tweets to get
	:return: a list of dictionaries including keys "id" of the tweet and "author"
	"""
	tweets=[]		
	url="https://mobile.twitter.com/search?q="+quote(searchterm)		
	while(len(tweets)<max_num and url!=''):
	   	response = requests.get(url)#self.bot.get(url) 
	        html=fromstring(response.content)
		if(html.xpath('//div[@class="noresults"]')):
			break
		tweet_items=html.xpath('//div[@class="timeline"]')[0].findall('./table')
		for item in tweet_items:
			tweet={}
			tweet["id"]=item.xpath('.//div[@class="tweet-text"]/@data-id')[0]			
			tweet["author"]=item.xpath('.//div[@class="username"]/text()')[1].strip(" \n")
				
			tweets.append(tweet)
			if(len(tweets)==max_num):
				break
		more_button=html.xpath('//div[@class="w-button-more"]/a/@href')
		if(more_button):
			url="https://mobile.twitter.com"+str(more_button[0])
		else:
			url=''

	return tweets


class LoginException(Exception):
	def __init__( self):
		Exception.__init__(self, 'Twitter Login failed.')
