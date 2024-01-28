import pymysql as mysql
import os
from dotenv import load_dotenv

load_dotenv()
conn = mysql.connect(
    host='localhost',
    user='root',
    password=os.getenv('DBPASSWORD'),
    db='pswdmanager',
    charset='utf8mb4',
    cursorclass=mysql.cursors.DictCursor
)

def createTable(tableName, columnArray):
    columnString = ""
    for column in columnArray:
        columnString += f", {column} VARCHAR(100)"


    with conn.cursor() as cursor:
        sql = (f"CREATE TABLE {tableName} (id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY{columnString})")
        print(sql)
        cursor.execute(sql)