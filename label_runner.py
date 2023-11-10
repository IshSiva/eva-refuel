import pandas as pd
import evadb
import sqlite3
import pandas as pd


cursor = evadb.connect().cursor()
print("Connected to EvaDB")

#Drop function if it already exists
cursor.query("DROP FUNCTION IF EXISTS AutoLabeller;").execute()

#create a new function
create_function_query = f"""CREATE FUNCTION IF NOT EXISTS AutoLabeller
            IMPL  './functions/auto_labeller.py';
            """

cursor.query(create_function_query).execute()
print("Created Function")

#create table in sqlite and connect to evadb
sql_db = """CREATE DATABASE IF NOT EXISTS sqlite_data WITH ENGINE = 'sqlite', PARAMETERS = {
     "database": "evadb.db"
};"""

cursor.query(sql_db).execute()

#load data into sqlite
df = pd.read_csv("data/test.csv")

database_file = 'evadb.db'
conn = sqlite3.connect(database_file)
table_name = 'TOXICITY'
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.commit()
conn.close()
print("Loaded data")

chat_query_1 = f""" SELECT AutoLabeller(example, label) FROM sqlite_data.TOXICITY;
"""
result = cursor.query(chat_query_1).execute()
print(result)

