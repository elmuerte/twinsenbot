# TwinsenBot

Twitter/Mastodon bot posting lines from the LBA games.

The bot in action: 
- https://twitter.com/twinsen_txt
- https://botsin.space/@twinsen

This bot is inspired by the WAD BOT by JP LeBreton: https://bitbucket.org/JPLeBreton/wadbot

# Twitter version

## Getting the OAuth tokens

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

# Mastodon version

Put the application access token in a file name `token.secret`.

# Quotes DB

The quote database was created from the game using one of the available HQR unpackers to
produce the `.lbt` files. With the LBA Text Views from LBADeCOMP these files were dumped
to individual text files. 

The `extract-quotes.py` script parses these files to the `quotes.db`. The script is called
with each file to process as an argument. It assumes the filenames have the following
format: `<game>/<id> <area>.txt` for example: `lba1/08 Citadel Island.txt`.

So the script was executed as: `./extract-quotes.py lba1/* lba2/*`
