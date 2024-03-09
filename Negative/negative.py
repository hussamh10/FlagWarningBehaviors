from lab317.utils import get_months
from lab317.utils import chunkify
from random import sample
from tqdm import tqdm

import multiprocessing as mp
import pickle as pkl
import sqlite3 as db
import pandas as pd
import numpy as np

import os
import gc
import re


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
obj = SentimentIntensityAnalyzer()
def sentiment(text):
    return obj.polarity_scores(text)['compound']

def sentiment_post(text1, text2):
    text = text1 + ' ' + text2
    return obj.polarity_scores(text)['compound']


def process_posts(month):
    con = db.connect('../../reddit-all-data/pickle/posts.db')
    sql = "ATTACH DATABASE ? AS output"
    tbl =(f"../storage/raw/traits/negative/posts/{month}.db",)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    con.create_function("VADER", 2, sentiment_post)


    SQL = f"""
        CREATE TABLE output.`{month}` AS
        SELECT VADER(title, selftext) as sentiment_score, subreddit, author, id
        FROM `{month}` 
    """

    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
    con.close()

def process_comments(month):
    table = month.replace('_', '-')
    con = db.connect('../../reddit-all-data/comments/comments-new-new.db')
    sql = "ATTACH DATABASE ? AS output"
    tbl =(f"../storage/raw/traits/negative/comments/{month}.db",)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    con.create_function("VADER", 1, sentiment)


    SQL = f"""
        CREATE TABLE output.`{month}` AS
        SELECT VADER(body) as sentiment_score, subreddit, author, id
        FROM `{table}` 
    """

    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
    con.close()
    
months = get_months('2015_01', '2020_08')

pool = mp.Pool(processes=len(months))
pool.map(process_posts, months)
pool.close()
