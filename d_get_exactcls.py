# _*_ coding: utf-8 _*_

import logging
from z_db_config import *

logging.basicConfig(level=logging.DEBUG)

# get exact classify for ios apps  --->  t_ios_classify


def get_exactcla():
    conn, cur = conn_db()
    ios_pkg_sql = "SELECT bundleid, pkgname FROM t_ios_classify WHERE pkgname IS NOT NULL AND classify IS NULL;"
    andr_sql = "SELECT pkgname, classify FROM t_pkg_classify;"
    update_sql = "UPDATE t_ios_classify SET classify = %s, is_exact = %s WHERE bundleid = %s;"
    count = 0

    cur.execute(ios_pkg_sql)
    bundle_pkg_dic = {}
    for item in cur.fetchall():
        bundle_pkg_dic[item[0]] = item[1]

    cur.execute(andr_sql)
    pkg_cls_dic = {}
    for item in cur.fetchall():
        pkg_cls_dic[item[0]] = item[1] + "\t" + item[2]

    for key in bundle_pkg_dic:
        pkgname = bundle_pkg_dic[key]
        if pkgname in pkg_cls_dic:
            logging.debug("pkgname in android: %s", pkgname)
            classify = pkg_cls_dic[pkgname].split("\t")[0]
            cur.execute(update_sql, (classify, 1, key))
        else:
            logging.debug("pkgname not in android: %s", pkgname)
        if count % 50 == 0:
            print("update")
            conn.commit()
        count += 1
    conn.commit()

if __name__ == "__main__":
    get_exactcla()
