# _*_ coding: utf-8 _*_

from z_db_config import *

# add ios's app to android


def united_andios():
    conn, cur = conn_db()
    # sql_select_andr = """SELECT pkgname, softgame, classify, platform FROM t_pkg_classify;"""
    sql_insert_ios = """INSERT INTO t_pkg_classify (pkgname, softgame, classify, platform, name_list)
                        (SELECT bundleid, softgame, classify, platform, name FROM t_ios_classify
                        WHERE classify IS NOT NULL);"""
    cur.execute(sql_insert_ios)
    conn.commit()
