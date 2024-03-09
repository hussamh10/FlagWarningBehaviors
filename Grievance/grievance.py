import os
os.environ['SQLITE_TMPDIR'] = '/home/data/hussam/TMP'

import multiprocessing as mp
import os
import pandas as pd
import sqlite3 as db

from collections import Counter
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

from tqdm import tqdm
from lab317.utils import get_months

months = get_months('2015_01', '2020_08')

ps = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

ref = pd.read_pickle('g7.dict')
all_keys = []

cat = []
for k in ref:
    all_keys += ref[k]
    cat += [k] * len(ref[k])
    
dic = pd.DataFrame(all_keys, columns=['keys'])
dic['cat'] = cat
cats = list(ref.keys())
cats.append('total')

L = 10
keys = set(dic['keys'])

def score(text):
    tokens = tokenizer.tokenize(text)
    tokens = [ps.stem(t[:20]) for t in tokens]
    tokens = Counter(tokens)
    WC = sum(tokens.values())
    total = 0
    K = keys.intersection(set(tokens.keys()))
    for k in K:
        total += tokens[k]
        
    return (total/(WC + L) )* 100


def score_raw(text):
    tokens = tokenizer.tokenize(text)
    tokens = [ps.stem(t[:20]) for t in tokens]
    tokens = Counter(tokens)
    WC = sum(tokens.values())
    total = 0
    K = keys.intersection(set(tokens.keys()))
    for k in K:
        total += tokens[k]
        
    return total

def total(text):
    tokens = tokenizer.tokenize(text)
    return len(tokens)

def process_posts(month):
    if os.path.exists(f"../storage/raw/traits/grievance/posts/{month}.db"):
        return
    
    con = db.connect('../../reddit-all-data/pickle/posts.db')
    sql = "ATTACH DATABASE ? AS output"
    tbl =(f"../storage/raw/traits/grievance/posts/{month}.db",)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    
    con.create_function("GSCORE", 1, score)
    
    SQL = f"""
    CREATE TABLE output.`{month}` AS
    SELECT author, GSCORE(GROUP_CONCAT(title || ' ' || selftext)) as score
    FROM `{month}` 
    GROUP BY author
    """
    
    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
    con.close()
    

def process_comments(month):
    if os.path.exists(f"../storage/raw/traits/grievance/comments/{month}.db"):
        return
    
    con = db.connect('../../reddit-all-data/comments/comments-new-new.db')
    sql = "ATTACH DATABASE ? AS output"
    tbl =(f"../storage/raw/traits/grievance/comments/{month}.db",)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    
    con.create_function("GSCORE", 1, score)

    table = month.replace('_', '-')
    
    SQL = f"""
    CREATE TABLE output.`{month}` AS
    SELECT author, GSCORE(GROUP_CONCAT(body)) as score
    FROM `{table}` 
    GROUP BY author
    """
    
    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
    con.close()

def process_comments_raw(month):
    if os.path.exists(f"../storage/raw/traits/grievance/comments/raw_{month}.db"):
        return
    
    con = db.connect('../../reddit-all-data/comments/comments-new-new.db')
    sql = "ATTACH DATABASE ? AS output"
    tbl =(f"../storage/raw/traits/grievance/comments/raw_{month}.db",)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    
    con.create_function("GSCORE", 1, score_raw)
    con.create_function("LEN", 1, total)

    table = month.replace('_', '-')
    
    SQL = f"""
    CREATE TABLE output.`{month}` AS
    SELECT author, GSCORE(body) as score, LEN(body) as total
    FROM `{table}` 
    """
    
    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
    con.close()
    
def process_comments_group(month):
    if os.path.exists(f"../storage/raw/traits/grievance/comments/{month}.db"):
        return
    
    con = db.connect(f'../storage/raw/traits/grievance/comments/raw_{month}.db')
    sql = "ATTACH DATABASE ? AS output"
    tbl =(f"../storage/raw/traits/grievance/comments/{month}.db",)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    
    
    SQL = f"""
    CREATE TABLE output.`{month}` AS
    SELECT author, sum(score) as score, sum(total) as total
    FROM `{month}` 
    GROUP BY author
    """
    
    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
    con.close()

m = get_months('2019_01', '2020_08')
pool = mp.Pool(processes=len(m))
pool.map(process_comments_group, m)
pool.close()
