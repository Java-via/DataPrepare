# _*_ coding: utf-8 _*_

import pymysql

DB_HOST = "localhost"
DB_USER = "appuser"
DB_PASSWD = "456"
DB_DB = "test_db"
DB_CHARTSET = "utf8"


def conn_db():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd= DB_PASSWD, db=DB_DB, charset=DB_CHARTSET)
    cur = conn.cursor()
    return conn, cur
