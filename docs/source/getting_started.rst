.. _getting_started:


***************
Getting started
***************

Twirly (TWItter Rogue Library in pYthon)

Introduction
============

Yet another Python library for Twitter?, you may ask. Well, if you are looking to a way to tweet/retweet/search, which does not require OAUTH authentication, this is the right place.

Read some tweets
================

.. code-block :: python

   from twirly import Twitter

   driver = Twitter("username","login")
   
   tweets=driver.search_tweets("wine",10)
   for tweet in tweets:
	print driver.get_tweet_info(tweet["author"],tweet["id"])
   
This fragment of code will search for the first 10 tweets including the word "wine" and will print each of them to the console. That's it! See :ref:`Code examples <code_examples>` to have a look on more interesting tasks.

Authentication and API
======================

APP authentication? No way! The approach of this Python library is to give you the utmost freedom without any OAUTH authentication. Indeed, as Twirly does not rely on official Twitter API, every functionality is implemented by direct interaction with HTML elements.

