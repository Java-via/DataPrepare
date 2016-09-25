# _*_ coding: utf-8 _*_

import logging
from z_db_config import *

logging.basicConfig(level=logging.DEBUG)


def get_classify():
    # if use t_apps_basic_new use next method named get_andr_classify
    # get android apps that accord with standard classify  t_apps_basic_united  --->  t_pkg_classify
    conn, cur = conn_db()
    s_sql = """SELECT a_pkgname_list, a_name_list, a_classify, a_softgame FROM t_apps_basic_united
                WHERE a_source_list NOT LIKE "iphone%" AND a_softgame_list NOT LIKE "\n";"""
    sql = """INSERT INTO t_pkg_classify (pkgname, name_list, classify, softgame) VALUES (%s, %s, %s, %s);"""
    logging.debug("Select begin")
    cur.execute(s_sql)
    logging.debug("Select done")
    apps = [(item[0], item[1], item[2], item[3]) for item in cur.fetchall()]
    for app in apps:
        classify_all = ""
        pkglist = app[0].split()
        classify_list = app[2].split()
        for classify in classify_list:
            logging.debug("Classify is %s", str(classify))
            if ":" not in str(classify):
                continue
            else:
                classify_all = classify_all + " " + classify
        if len(classify_all) > 0:
            logging.debug("Classify is need: %s", str(classify_all))
            for pkg in pkglist:
                logging.debug("Pkgname is %s, classify is %s", pkg, classify_all)
                try:
                    cur.execute(sql, (pkg, app[1], ",".join(set(classify_all.split())), app[3]))
                    conn.commit()
                except Exception as excep:
                    logging.error("Insert Error: %s", excep)


def get_andr_classify():
    # get android apps that accord with standard classify  t_apps_basic_new  --->  t_pkg_classify
    conn, cur = conn_db()
    sql = """INSERT INTO t_pkg_classify (pkgname, softgame, name_list, classify, platform)
                    SELECT t0.a_pkgname AS pkgname, GROUP_CONCAT(DISTINCT t0.a_softgame SEPARATOR ",") AS softgame,
                    GROUP_CONCAT(DISTINCT t0.a_name SEPARATOR ",") AS name,
                    GROUP_CONCAT(DISTINCT a_classify SEPARATOR ",") AS classify,
                    "android" AS platform FROM
                    (SELECT a_pkgname, a_softgame, a_name, a_classify
                      FROM t_apps_basic_new
                      WHERE a_getdate = "2016-09-25" AND a_source NOT LIKE "iphone%" AND INSTR(a_classify,":")>0) t0
                    GROUP BY a_pkgname;"""
    cur.execute(sql)
    conn.commit()


if __name__ == "__main__":
    get_andr_classify()
