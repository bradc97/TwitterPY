Twitter-PY
=========

This is a twitter wrapper that **doesn't** use the offical API




List of current functions
--------------
* Login
* Tweet
* Retweet
* Favorite
* Delete Tweet
* Direct Message
* Get Followers/Following(Returns a list of accounts)
* Change Profile Settings (Location, Username Etc)


Login Example
--------------

```sh
    twitter = TwitterClient.TwitterClient()

    if twitter.login('account', 'passowrd'):
    	print('Signed into %s' %  Twitter.Account)
    else:
        print('Sign in failed')
```
Tweeting Example
---------------

```sh

    twitter = TwitterClient.TwitterClient()

    twitter.login('account', 'passowrd')
    
    Messages = ['First Tweet','Second Tweet','Third??']
    
    for Message in Messages:
        twitter.tweet(Message)
        
```

License
----

MIT

