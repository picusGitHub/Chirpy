.. _code_examples:


***************
Code examples
***************

Introduction
============

Here you will find some examples of usage of this class. Before executing the scripts below don't forget to import Tweedly and initialize it providing username and password of your account!

.. code-block :: python

   import tweedly

   driver = Twitter('my_username','my_password')

Login and logout
================

.. code-block :: python

   driver.login()

   driver.logout()


Search for tweets in a user's timeline
======================================

.. code-block :: python

	# Get the last 100 tweets
	tweets=driver.get_tweets('username',100)

	# Print id and username of the author
	for tweet in tweets:
		print tweet("id="+tweet['id'])
		print tweet("author="+tweet['username'])

Search for all details of a given tweet from a given user
=========================================================

.. code-block :: python

	tweet=driver.get_tweet_info('username','123456789')

	# Print details
	print tweet['id']
	print tweet['username']
	print tweet['time']
	print tweet['date']
	print tweet['text']
	print tweet['hashtags']
	print tweet['rewteet']
	print tweet['likes']


Get info about a user
=====================

.. code-block :: python

	user=driver.get_user_info('username')

	# Print details
	print user['tweets']
	print user['followers']
	print user['following']
	print user['location']
	print user['bio']
	print user['url']


Get usernames of followers/following of a user
==============================================

.. code-block :: python

	# Get 10 followers
	followers=driver.get_followers('username',10)

	# Get 10 following
	following=driver.get_following('username,10)


Search usernames by term and print their details
================================================

.. code-block :: python

	#Get the first 10 users (as sorted by twitter search)
	users=driver.search_users('search term',10)
	for user in users:
		print driver.get_user_info(user)


Search for tweets by hashtag
============================

.. code-block :: python

	# Get the first 30 tweets with hashtag #wine (as sorted by Twitter search)
	tweets=driver.search_tweets('#wine',30)


Search for users
================

.. code-block :: python

	# Get the first 20 users (as sorted by Twitter search)
	users=driver.search_users('search term',20)
   
Tweet a message
===============

.. code-block :: python

	driver.tweet('Hi everybody')

Reply to a tweet
================

.. code-block :: python

	# Replies to the tweet id '1234567890' written by user 'username'
	driver.tweet_reply('username','1234567890','This is a reply!')

Follow a user
=============

.. code-block :: python

	driver.follow('user_to_follow')

Unfollow a user
===============

.. code-block :: python

	driver.unfollow('user_to_unfollow')

Block a user
============

.. code-block :: python

	driver.block_user('username')

Report a user for spam
======================

.. code-block :: python

	driver.report_spam_user('username')

