import os
import sys

from pandas import DataFrame
from datetime import date, timedelta
from Scweet.scweet import scrape
from time import sleep
import pandas as pd

env_path = os.environ.get('SCWEET_ENV')  # path to .env file for Scweet see library docs


def init_output():
    # make a directory called outputs if it doesn't exist, this is the default location for the outputs
    execution_path = sys.path[0]
    output_path = execution_path + 'outputs'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    path = execution_path + '/outputs'
    os.chdir(path)


def scrape_tweets(topic: str, days_to_search: int, number_of_tweets_per_day: int) -> DataFrame:
    """
    Scrapes tweets from a topic for a certain number of days
    :param topic:
    :param days_to_search:
    :param number_of_tweets_per_day:
    :return: DataFrame of tweets
    """
    list_of_dataframes = []
    for i in range(0, days_to_search):
        starting_date = date.today() - timedelta(days=i)
        end_date = starting_date + timedelta(days=1)
        print(f'Scraping tweets from {starting_date} to {end_date}')
        df = scrape(words=topic, since=starting_date.__str__(), until=end_date.__str__(), from_account=None, interval=1,
                    headless=False, display_type="Top", save_images=False,
                    resume=False, filter_replies=True, proximity=False, limit=number_of_tweets_per_day, minlikes=100)
        list_of_dataframes.append(df)
        if i < days_to_search - 1:
            # found that not sleeping causes the program to crash
            sleep(3)

    if len(list_of_dataframes) > 0:
        df = pd.concat(list_of_dataframes)
        # reset indexes, this is important when we run nlp on the dataframe
        df.reset_index(drop=True, inplace=True)
        # the df that gets returned from scrape has the tweet stats duplicated for each tweet, so clean it up
        df['Embedded_text'] = df.apply(lambda row: remove_last_lines(row), axis=1)

        return df
    else:
        return pd.DataFrame()


# Embedded text has like, comment, retweet, and like counts, we only want the embedded text
def remove_last_lines(row_of_df: DataFrame) -> str:
    num_lines_to_remove = 0
    if len(row_of_df['Comments']) > 0:
        num_lines_to_remove += 1
    if len(row_of_df['Retweets']) > 0:
        num_lines_to_remove += 1
    if len(row_of_df['Likes']) > 0:
        num_lines_to_remove += 1
    return '\n'.join(row_of_df['Embedded_text'].split('\n')[:-num_lines_to_remove])
