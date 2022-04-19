import boto3
import pandas as pd
from pandas import DataFrame

client = boto3.client('comprehend', region_name='us-east-1')


def get_sentiment_for_tweet(tweet: str) -> dict:
    """
    Returns the sentiment of a tweet
    """
    if len(tweet) < 1:
        return dict()
    response = client.detect_sentiment(Text=tweet, LanguageCode='en')
    sentiment_data = dict()
    sentiment_data['Sentiment'] = response['Sentiment']
    sentiment_data['Sentiment_Score_Positive'] = response['SentimentScore']['Positive']
    sentiment_data['Sentiment_Score_Neutral'] = response['SentimentScore']['Neutral']
    sentiment_data['Sentiment_Score_Negative'] = response['SentimentScore']['Negative']
    return sentiment_data


def analyze_tweets(tweets: DataFrame) -> DataFrame:
    """
    Analyzes the sentiment of each tweet in a dataframe
    """
    s = tweets['Embedded_text'].apply(get_sentiment_for_tweet)
    tweets = tweets.join(pd.DataFrame(s.tolist(), index=s.index))
    return tweets
