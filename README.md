TwinsenBot
==========

Twitter bot posting lines from the LBA games. The quotes are retrieved from the Magicball Network: http://www.magicball.net/gamequotes

The bot in action: https://twitter.com/twinsen_txt

This bot is inspired by the WAD BOT by JP LeBreton: https://bitbucket.org/JPLeBreton/wadbot


Getting the OAuth tokens
------------------------

In order to get the user's OAuth token, you need to run the following in an interactive python session.

    >>> api_key='__something__'
    >>> api_secret='__something__'
    >>> import tweepy
    >>>
    >>> auth = tweepy.OAuthHandler(api_key, api_secret)
    >>> print auth.get_authorization_url()
    https://api.twitter.com/oauth/authorize?oauth_token=__something__

Visit this page and authenticate with the twitter user you want to use, and get the PIN to use in the next command.

    >>> print auth.get_access_token(__the_pin_here__)
    oauth_token_secret=__something__&oauth_token=__something__
    >>>

Or, simply create the twitter application with the target account so you can create OAuth tokens directly from the application management page.
