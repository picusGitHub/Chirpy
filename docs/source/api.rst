.. _api:


***************
API Reference
***************
This page contains documentation for the Tweedly module.


:mod:`tweedly.Twitter`
======================

.. class:: Twitter(username, password)

   The functions provided in this class are listed below.

   :param str username: |username|
   :param str password: |password|

Access methods
--------------

.. method:: login():
   
   Login to Twitter.

.. method:: logout():
   
   Logout from Twitter.

.. method:: is_logged():
   
   Check if the user is logged or not.
	
   :return: a boolean

Action methods
--------------

.. method:: follow(username):
   
   Follow the user with the specified username.

   :param str username: specifies the screen_name of the user
   :return: a boolean stating if the operation has succeeded

.. method:: unfollow(username):
   
   Unfollow the user with the specified username.

   :param str username: specifies the screen_name of the user	
   :return: a boolean stating if the operation has succeeded

.. method:: tweet(message):
   
   Send a tweet with the specified message.
	
   :param str message: specifies the content of the tweet

.. method:: tweet_reply(username,tweet_id,message):
   
    Send a reply to the specified tweet.

   :param str username: specifies the screen_name of the user
   :param str tweet_id: specifies the id of the tweet to reply
   :param str message: specifies the content of the reply

.. method:: tweet_retweet(tweet_id):
   
   Retweet the specified tweet.

   :param str tweet_id: specified the id of the tweet to retweet
   :return: a boolean stating if the operation has succeeded

.. method:: tweet_like(username,tweet_id):
   
   Like the specified tweet.

   :param str username: specifies the screen_name of the user
   :param str tweet_id: specified the id of the tweet to like

.. method:: block_user(username):
   
   Block the specified user.

   :param str username: specifies the screen_name of the user to block
	
.. method:: report_spam_user(username):
   
   Report the username for spam.
	
   :param str username: specifies the screen_name of the user to report for spam	


Search methods
--------------

.. method:: get_user_info(username):
   
   Return a set of information about the user specified in input. This method is run anonymously (without any Session active).

   :param str user: specifies the screen_name of the user
   :return: a dictionary including keys "username","tweets","following","followers","location","bio","url" as details of the user

.. method:: get_followers(username,max_num):
   
   Return a list of followers of the specified user. This method is run anonymously (without any Session active).

   :param str username: specifies the screen_name of the user
   :param int max_num: specifies the number of following users to get
   :return: a list of screen_name of following users

.. method:: get_following(username,max_num):
   
   Return a list of users followed by the specified user. This method is run anonymously (without any Session active).

   :param str username: specifies the screen_name of the user
   :param int max_num: specifies the number of following users to get
   :return: a list of screen_name of following users

.. method:: search_users(searchterm,max_num):
   
   Search for users according to the search term. This method is run anonymously (without any Session active).
		
   :param str searchterm: specifies the search term
   :param int max_num: specifies the number of users to get
   :return: a list of screen_name of users	

.. method:: get_tweets(screen_name,max_num):
   
   Return at most max_num tweets from the username timeline. This method is run anonymously (without any Session active).

   :param str username: specifies the screen_name of the user
   :param int max_num: specifies the number of tweets to get 
   :return: a list of dictionaries including keys "id" of the tweet and "author"


.. method:: get_tweet_info(username,tweet_id)
   
   Return details about the specified tweet. This method is run anonymously (without any Session active).
	
   :param str username: the author of the tweet
   :param str tweet_id: the id of the tweet
   :return: a dictionary including the keys "id","username","date","time","text","hashtags","retweet","likes" as details of the tweet

.. method:: search_tweets(searchterm,max_num)
   
   Search for tweets according to the search terms. This method is run anonymously (without any Session active).

   :param str searchterm: specifies the search term
   :param int max_num: specifies the number of tweets to get
   :return: a list of dictionaries including keys "id" of the tweet and "author"

:mod:`tweedly.LoginException`
=============================

.. class: LoginException(Exception)
   
   The exception raised by a failed login.	
