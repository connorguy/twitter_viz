import glob
import optparse
import os
import sys

import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
import scraper_twitter as st
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS


def read_data(filename) -> DataFrame:
    """
    Reads a file and returns a cleaned up dataframe indexed by time
    :param filename:
    :return:
    """
    try:
        df = pd.read_csv(options.file, index_col='Timestamp', parse_dates=True)
    except:
        print('Unable to read file: ' + options.file)
        sys.exit(1)
    return df


def graph_twitter_data(df: DataFrame):
    '''
    Graphs sentiment data on a daily basis
    :param df:
    '''
    # Note: if you run this with data for a single day it will not plot correctly. Change sampling type to 'H'
    df[['Sentiment_Score_Positive', 'Sentiment_Score_Neutral', 'Sentiment_Score_Negative']].resample('D').mean().plot()

    print(df.describe())
    print(df.head())

    plt.show()


def generate_wordcloud(df: DataFrame):
    '''
    Generates a wordcloud of the most common words in the data
    :param df:
    '''
    # df['Embedded_text'] = df['Embedded_text'].astype(str)
    text = ''.join(str(df['Embedded_text'].values))
    stopwords = set(STOPWORDS)
    stopwords.add('n')
    wordcloud = WordCloud(stopwords=stopwords, background_color="white", width=500, height=500).generate(
        text)
    plt.figure(figsize=(20, 20))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    st.init_output()

    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', dest='file', help='File to visualize')

    (options, args) = parser.parse_args()
    if options.file is None:
        parser.print_help()
        sys.exit(1)

    df = read_data(options.file)

    # graph_twitter_data(df)
    generate_wordcloud(df)
