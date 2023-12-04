from prefect import flow, task
from time import sleep
from models.utils import Utils
import pandas as pd

util = Utils()


@task
def read_search_terms():
    search_terms_df = pd.read_csv(util.search_terms_csv)
    #search_terms = ["keyword 1", "keyword 2", "keyword 3"]
    search_terms = list(search_terms_df['search_term'])
    return search_terms


@task(tags=["10_at_a_time"])
def fetch_tweets(search_term: str):
    return util.fetch_tweets(search_term=search_term)


def get_tweets(search_terms: list):
    tweets = []
    for search_term in search_terms:
        tweets.append(fetch_tweets.submit(search_term))

    return [tweet.result() for tweet in tweets]


@task(tags=["1000_at_a_time"])
def analyze_sentiment_from_text(search_term: str, tweet: str):
    return util.analyze_sentiment_from_text(search_term=search_term, text=tweet)


def perform_sentiment_analysis(list_of_tweet_dicts: list):
    senti_analysis = list()
    for tweets_data in list_of_tweet_dicts:
        search_term = tweets_data["search_term"]
        tweets = tweets_data["tweets"]

        for tweet in tweets:
            senti_analysis.append(
                analyze_sentiment_from_text.submit(search_term, tweet)
            )

    return [senti.result() for senti in senti_analysis]

@task
def generate_sentimentanalysis_csv(sentiment_analysis_result: list):
    util.generate_sentiment_analysis_csv(sentiment_analysis_result=sentiment_analysis_result)


@flow(log_prints=True)
def twitter_sentiment_analysis_flow():
    search_terms_list = read_search_terms()
    list_of_tweet_dicts = get_tweets(search_terms=search_terms_list)
    sentiment_analysis_result = perform_sentiment_analysis(
        list_of_tweet_dicts=list_of_tweet_dicts, 
    )
    generate_sentimentanalysis_csv(sentiment_analysis_result)


if __name__ == "__main__":
    twitter_sentiment_analysis_flow()
