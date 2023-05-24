#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Twinsen Bot
# A Mastodon bot which posts random lines from the Little Big Adventure games.

import urllib
import xml.etree.ElementTree as ET
from mastodon import Mastodon
import re


# The URL where we retrieve random quotes from
QUOTE_URL = 'https://www.magicball.net/gamequotes/xml?minlength=15&maxlength=495'

# Quotes which have already been posted will be logged here
SEEN_FILE = './seen-quotes-mstd.db'

# Number of times to try to get a unseen quote
MAX_TRIES=100

# Tags to use for the game quotes
GAME_TAGS = {'lba1': '#LBA', 'lba2' : '#LBA2'}

def retrieve_quote():
    """Retrieve a quote from the given url"""
    data = urllib.request.urlopen(QUOTE_URL).read()
    quote = ET.fromstring(data)
    return quote

def is_unseen(id):
    """Checks if the provided quote id was already used"""
    return not id in seenlist

def format_quote(quote):
    """Format the quote to a twitter message"""
    quoteText = re.sub(r'\s+', ' ', quote.findtext('text').strip());
    if (quoteText == None):
        return None
    return quoteText + '\n' + GAME_TAGS[quote.find('game').get('id')]

seen_file = open(SEEN_FILE, 'a+')
seenlist = seen_file.readlines()

# Find an unused quote to work with
useQuote=None
attempt=0

while useQuote == None:
    attempt+=1
    for quote in retrieve_quote().findall('quote'):
        if (is_unseen(quote.get('id'))):
            useQuote=quote
        elif (attempt >= MAX_TRIES):
            useQuote=quote
        else:
            print("Already saw quote: "+quote.get('id'))

if (useQuote == None):
    print("No new quote found")
    exit()


postMsg=format_quote(quote)

print('Posting quote: '+quote.get('id'))

# Posting the quote
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space/'
)
mastodon.status_post(postMsg, visibility="public")

seen_file.write(quote.get('id')+'\n');
seen_file.close();
