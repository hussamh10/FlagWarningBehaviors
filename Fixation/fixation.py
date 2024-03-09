import os
os.environ['SQLITE_TMPDIR'] = '/home/data/hussam/TMP'

import nltk

import multiprocessing as mp
import pickle as pkl
import sqlite3 as db
import pandas as pd
import numpy as np
from lab317.utils import get_months

import os
import gc
import re

months = get_months('2015_01', '2020_08')
keywords = open('keywords.txt', 'r').read().split(', ')
tokenizer = nltk.RegexpTokenizer(r'\w+')

def count(text):
    tokens = tokenizer.tokenize(text)
    return len(tokens)

def fixation(text):
    tokens = tokenizer.tokenize(text.lower())
    found = [i for i in tokens if i in keywords]
    return len(found)

def process_posts(month):
    con = db.connect('../../reddit-all-data/pickle/posts.db')
    sql = "ATTACH DATABASE ? AS output"
    tbl =(f"../storage/raw/traits/fixation/posts/{month}.db",)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    
    con.create_function("FIXATION", 1, fixation)
    con.create_function("TCOUNT", 1, count)

    SQL = f"""
    CREATE TABLE output.`{month}` AS
    SELECT author, FIXATION(GROUP_CONCAT(title || ' ' || selftext)) as fixation, TCOUNT(GROUP_CONCAT(title || ' ' || selftext)) as total
    FROM `{month}` 
    GROUP BY author
    """
    
    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
    con.close()

def process_comments(month):
    out = f"../storage/raw/traits/fixation/comments/{month}.db"
    if os.path.exists(out):
        print(month)
        return
    table = month.replace('_', '-')
    con = db.connect('../../reddit-all-data/comments/comments-new-new.db')
    sql = "ATTACH DATABASE ? AS output"
    tbl =(f"../storage/raw/traits/fixation/comments/{month}.db",)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    
    con.create_function("FIXATION", 1, fixation)
    con.create_function("TCOUNT", 1, count)

    SQL = f"""
    CREATE TABLE output.`{month}` AS
    SELECT author, FIXATION(body) as fixation, TCOUNT(body) as total
    FROM `{table}` 
    """
    
    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
    con.close()
    
    
pool = mp.Pool(processes=len(months))
pool.map(process_comments, months)
pool.close()
