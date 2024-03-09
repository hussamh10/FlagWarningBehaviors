from liwc_core import liwc

import multiprocessing as mp
import pickle as pkl
import sqlite3 as db
import pandas as pd
import numpy as np
from lab317.utils import get_months

import os
import gc
import re


from liwc_core import liwc

LIWC = liwc('LIWC2015_English_OK.dic')

def liwc_score(text):
    if type(text) == str:
        values = LIWC.liwcify(text)
        values = list(values.values())
        return str(values).replace(' ', '')
    return str(list(LIWC.liwcify('').values())).replace(' ','')

def process_posts(month):
    con = db.connect('../../reddit-all-data/pickle/posts.db')
    sql = "ATTACH DATABASE ? AS output"
    tbl =(f"../storage/raw/traits/liwc/posts/{month}.db",)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    con.create_function("LIWC", 1, liwc_score)

    SQL = f"""
    CREATE TABLE output.`{month}` AS
    SELECT id, author, LIWC(title || ' ' || selftext) as liwc_score
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
    tbl =(f"../storage/raw/traits/liwc/comments/{month}.db",)
    cur = con.cursor()
    cur.execute(sql,tbl)
    con.commit()
    con.create_function("LIWC", 1, liwc_score)


    SQL = f"""
        CREATE TABLE output.`{month}` AS
        SELECT id, author, LIWC(body) as liwc_score
        FROM `{table}` 
    """

    cur = con.cursor()
    cur.execute(SQL)
    con.commit()
    con.close()

months = get_months('2015_01', '2020_08')

pool = mp.Pool(processes=len(months))
pool.map(process_comments, months)
#pool.map(process_posts, months)
pool.close()
