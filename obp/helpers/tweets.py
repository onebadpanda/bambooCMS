__author__ = 'One Bad Panda'
import twitter
from obp.helpers.config import Config as settings


api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                  consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                  access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
                  access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)


def get_latest_tweets():
    try:
        return api.GetUserTimeline(count=5)
        #return {'text':'boo'}
    except twitter.TwitterError as e:
        return e.message


def get_latest_mentions():
    try:
        return api.GetMentions(count=5)
        #return {'text':'boo'}

    except twitter.TwitterError as e:
        return e.message