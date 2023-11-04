import sqlite3
import pandas as pd

DB_NAME = 'pcc-rent.db'
conn = sqlite3.connect(DB_NAME)

c = conn.cursor()
#print(c.execute(input('SQL>')))
c.execute("INSERT INTO pcc_users(name,email,solt,passwd,activate_flag,uuid) VALUES('unko','a@b.c','test','test',0,'4')")
print(c.fetchall())

c.close()