import pandas as pd
import os
from nltk.sentiment import SentimentIntensityAnalyzer
import csv


class Utils:
    def __init__(self):
        self.files_path = "files/input"
        self.results_files_path = "files/results"
        twitter_df = pd.read_csv(
            os.path.join(self.files_path, "twitter_updated_dataset.csv")
        )
        self.twitter_df = twitter_df[["tweet"]]
        self.sia = SentimentIntensityAnalyzer()
        self.search_terms_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQWOFdqyg6YXj5ckFfmjj-ZJrvesEpY0FK7W9KuLRceXdIeDNEgskI3Zx0kh8ogCV4F99VAT-horLlC/pub?output=csv"

    def fetch_tweets(self, search_term):
        search_term_tweets_df = self.twitter_df.sample(n=100)
        search_term_tweets_list = list(search_term_tweets_df["tweet"])
        tweets_data = {"search_term": search_term, "tweets": search_term_tweets_list}
        return tweets_data

    def analyze_sentiment_from_text(self, search_term, text):
        sentiment = self.sia.polarity_scores(text=text)
        compound_score = sentiment["compound"]
        resulting_sentiment = ""

        if compound_score >= 0.05:
            resulting_sentiment = "Positive"
        elif sentiment["compound"] <= -0.05:
            resulting_sentiment = "Negative"
        else:
            resulting_sentiment = "Neutral"

        sentiment_analysis_data = {
            "search_term": search_term,
            "text": text,
            "resulting_sentiment": resulting_sentiment
        }
        print(sentiment_analysis_data)
        return sentiment_analysis_data
    
    def generate_sentiment_analysis_csv(self, sentiment_analysis_result):
        df = pd.DataFrame(sentiment_analysis_result)
        df.to_csv(os.path.join(self.results_files_path,'result_final.csv'), index=False)
