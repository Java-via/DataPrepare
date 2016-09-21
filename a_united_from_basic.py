# _*_ coding: utf-8 _*_

from z_db_config import *


def united_ios():
    # prepare tables
    # first add softgame for ios   --->  t_apps_basic_new: softgame
    conn, cur = conn_db()
    sql_set_softgame = """UPDATE t_apps_basic_new t1,
                                (SELECT a_id, CASE WHEN LOCATE("70",a_source)>0 THEN 'game' ELSE 'soft' END softgame
                                  FROM t_apps_basic_new WHERE a_source LIKE "iphone%" AND a_softgame IS NULL ) t0
                          SET t1.a_softgame = t0.softgame WHERE t1.a_id = t0.a_id; """
    cur.execute(sql_set_softgame)
    conn.commit()

    # then add ios data to united   --->  t_apps_basic_bunited
    sql_insert_united = """INSERT INTO t_apps_basic_united (
                              a_id, a_pkgname, a_pkgname_list, a_name, a_name_list,
                              a_url, a_picurl, a_publisher, a_description, a_description_list,
                              a_classify, a_source_list, a_softgame, a_getdate)
                              SELECT a_id AS id,
                              a_pkgname AS pkgname,
                              a_pkgname AS pkgname_list,
                              a_name AS a_name,
                              GROUP_CONCAT(DISTINCT a_name SEPARATOR ",") AS a_name_list,
                              GROUP_CONCAT(DISTINCT a_url SEPARATOR ",") AS a_url,
                              a_picurl AS a_picurl,
                              GROUP_CONCAT(DISTINCT a_publisher SEPARATOR ",") AS a_publisher,
                              a_description AS a_description,
                              a_description AS a_description_list,
                              GROUP_CONCAT(DISTINCT a_classify SEPARATOR ",") AS a_classify,
                              GROUP_CONCAT(DISTINCT a_source SEPARATOR ",") AS a_source,
                              GROUP_CONCAT(DISTINCT a_softgame SEPARATOR ",") AS a_softgame,
                              "2000-09-01"
                              FROM t_apps_basic_new
                              WHERE a_source LIKE "iphone%"
                              GROUP BY pkgname ORDER BY a_id;"""
    cur.execute(sql_insert_united)
    conn.commit()

    # then create tables of ios_classify   --->  t_ios_classify
    sql_update_ioscls = """INSERT INTO t_ios_classify (bundleid, name, url, is_exact)
                          (SELECT a_pkgname, a_name, a_url, 0 FROM t_apps_basic_united);"""
    cur.execute(sql_update_ioscls)
    conn.commit()


if __name__ == "__main__":
    united_ios()
