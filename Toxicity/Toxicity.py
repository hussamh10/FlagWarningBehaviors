import os
os.environ['SQLITE_TMPDIR'] = '/home/data/hussam/TMP'
import gc
import re
from random import shuffle

import numpy as np
import pandas as pd
import pickle as pkl
import sqlite3 as db
import multiprocessing as mp

from tqdm import tqdm
from random import sample
from lab317.utils import get_months
from googleapiclient import discovery

months = get_months('2015_01', '2020_08')
db.enable_callback_tracebacks(True)


SAMPLE = 100
P = 18

def chunkify(lst,n):
    return [lst[i::n].copy() for i in range(n)]

def score(s):
    s = s.split('|')
    shuffle(s)
    s = s[:SAMPLE]
    scores = toxic_score(s)
    return str(scores)

def toxic_score(comments):
    API_KEY = 'AIzaSyBdVLZnvcOYKIKfbnrQ99lathFLRIN3Fns'
    client = discovery.build(
      "commentanalyzer",
      "v1alpha1",
      developerKey=API_KEY,
      discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1"
    )
    
    scores = []
    
    for s in comments:
    
        analyze_request = {
          'comment': { 'text': s },
          'requestedAttributes': {'TOXICITY': {}}
        }
        score = None
        try:
            response = client.comments().analyze(body=analyze_request).execute()
            score = response['attributeScores']['TOXICITY']['spanScores'][0]['score']['value']
            score = round(score, 3)
        except:
            score = None
        

        scores.append(score)
    return scores

def process_comments(month):
    out = f"../storage/raw/traits/toxicity/comments/filterd-{month}.db"
    
    users = 'users.db'
        
    if os.path.exists(out):
        print(month)
        return
    
    table = month.replace('_', '-')
    con = db.connect('../../reddit-all-data/comments/comments-new-new.db')
    sql = "ATTACH DATABASE ? AS output"
    tbl =(out,)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    
    sql = "ATTACH DATABASE ? AS user"
    tbl =('users.db',)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    
    con.create_function("SCORE", 1, score)

    SQL = f"""
            CREATE TABLE output.`{month}` AS
            SELECT t.author, SCORE(GROUP_CONCAT(body, "|")) as toxicity
            FROM `{table}` as t JOIN user.users as u 
            ON t.author = u.author
            GROUP BY u.author"""
    
    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
    con.close()

pool = mp.Pool(processes=P)
pool.map(process_comments, months)
pool.close()
