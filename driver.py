import os
import sys

import pandas as pd

import nlp_helpers as nlp
import scraper_twitter as ts
import visualizer as viz

if __name__ == '__main__':
    topic = input("What topic would you like to search for? ")
    days = int(input("How many days of tweets would you like to search for? "))
    number_of_tweets = int(input("How many tweets would you like to search for? "))

    # tweets_df = twitter_scraper.scrape_tweets(topic, days_to_search=3, number_of_tweets_per_day=10)
    tweets_df = ts.scrape_tweets(topic, days_to_search=days, number_of_tweets_per_day=number_of_tweets)
    tweets_df = nlp.analyze_tweets(tweets_df)

    # # Normalize topic string before saving
    topic = topic.replace(" ", "_")
    tweets_df.to_csv("outputs/" + topic + ".csv")

    # re-index the dataframe to Timestamp
    tweets_df.set_index('Timestamp', inplace=True)
    tweets_df.index = pd.to_datetime(tweets_df.index)

    viz.graph_twitter_data(tweets_df)
