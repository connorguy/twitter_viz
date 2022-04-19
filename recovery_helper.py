import glob
import os
import sys

import pandas as pd
from pandas import DataFrame

import scraper_twitter as st
import nlp_helpers as nlp

# make a directory called outputs if it doesn't exist
execution_path = sys.path[0]
if not os.path.exists(execution_path + 'outputs'):
    os.makedirs(execution_path + 'outputs')
path = execution_path + '/outputs'
os.chdir(path)


# function to read all csvs from outputs directory and return a dataframe
def read_all_csvs_to_df() -> DataFrame:
    all_files = glob.glob("*.csv")
    all_files = sorted(all_files, key=os.path.getmtime, reverse=True)
    print(all_files)

    if len(all_files) == 0:
        print("No csvs found in directory")
        exit(-1)
    df_tweets = pd.concat((pd.read_csv(f) for f in all_files))

    # re-add the index column
    df_tweets.reset_index(drop=True, inplace=True)
    print("Dataframe size: " + str(len(df_tweets)))

    # change a column type to string
    df_tweets['Comments'] = df_tweets['Comments'].astype(str)
    df_tweets['Retweets'] = df_tweets['Retweets'].astype(str)
    df_tweets['Likes'] = df_tweets['Likes'].astype(str)

    # Clean up tweet text
    df_tweets['Embedded_text'] = df_tweets.apply(lambda row: st.remove_last_lines(row), axis=1)
    return df_tweets


# get boolean value from user
def get_bool_from_user(question: str) -> bool:
    while True:
        try:
            user_input = input(question)
            if user_input.lower() == 'y' or user_input.lower() == 'yes':
                return True
            elif user_input.lower() == 'n' or user_input.lower() == 'no':
                return False
            else:
                print("Please enter 'y' or 'n'")
        except ValueError:
            print("Please enter 'y' or 'n'")


# get user input for a string
def get_string_from_user(question: str) -> str:
    while True:
        try:
            user_input = input(question)
            if len(user_input) > 0:
                return user_input
            else:
                print("Please enter a string")
        except ValueError:
            print("Please enter a string")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
shouldRunNlp = get_bool_from_user("Do you want to run NLP? (y/n) ")
topic = get_string_from_user("Please enter a title: ")

df = read_all_csvs_to_df()

if shouldRunNlp:
    print("Running NLP, hang tight...")
    df = nlp.analyze_tweets(df)

df.to_csv(topic + ".csv")
