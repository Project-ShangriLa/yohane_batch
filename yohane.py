import time
import pixiv
import sys
import json
import pymysql.cursors
from datetime import date
from datetime import datetime
import requests
import re
from optparse import OptionParser

#python3 yohane.py -i 372
#python3 yohane.py -i 372 -d
#python3 yohane.py -i 372 -d -s 5
parser = OptionParser()

parser.add_option(
    '-d', '--day',
    action = 'store_true',
    dest = 'day_switch',
    help = 'day mode on'
)

parser.add_option(
    '-i', '--id',
    action = 'store',
    type = 'str',
    dest = 'bases_id',
)

parser.add_option(
    '-s', '--sleep_second',
    action = 'store',
    type = 'int',
    dest = 'sleep_sec',
)

parser.set_defaults(
    bases_id = 0,
    day_switch = False,
    sleep_sec = 30
)

options, args = parser.parse_args()

day_switch = options.day_switch
bases_id = options.bases_id
sleep_sec = options.sleep_sec

def status_table_init(master_ids):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='anime_admin_development',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "delete FROM pixiv_character_tag_status WHERE bases_id IN (" + ",".join(master_ids) + ")"
            cursor.execute(sql)

        connection.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        connection.close()

def regist_pixiv_datta(id, character_id, get_date, key, total, note, json, history_table):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='anime_admin_development',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `pixiv_character_tag_status` (`bases_id`, `character_id`, `get_date`, `search_word`, `total`,`note`, `json`, `created_at`, `updated_at`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, character_id, get_date, key, total, note, json, datetime.now(), datetime.now()))

            sql = "INSERT INTO " + history_table + " (`bases_id`,`character_id`, `get_date`, `search_word`, `total`,`note`, `json`, `created_at`, `updated_at`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, character_id, get_date, key, total, note, json, datetime.now(), datetime.now()))

            connection.commit()

    finally:
        connection.close()


SLEEP_TIME_SEC = sleep_sec
history_table = "pixiv_character_tag_hourly"
get_date = datetime.now()
param = sys.argv


status_table_init([bases_id])

if (day_switch):
    history_table = "pixiv_character_tag_daily"
    get_date = date.today()


character_list = []

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='anime_admin_development',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = "SELECT id, bases_id, name FROM anime_character where bases_id = " + bases_id
    cursor.execute(sql)

    results = cursor.fetchall()
    for r in results:
        character_list.append(r)

for character in character_list:

    search_keyword = character['name']

    json_result = pixiv.api.search_works(search_keyword, page=1, mode='tag')
    total = json_result.pagination.total

    print(search_keyword)
    print(total)

    regist_pixiv_datta(character['bases_id'], character['id'], get_date, search_keyword, total, '', '', history_table)

    print("sleep!")
    time.sleep(SLEEP_TIME_SEC)
