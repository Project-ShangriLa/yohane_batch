import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='anime_admin_development',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:

    with connection.cursor() as cursor:
        sql = "SELECT id, name FROM anime_character where bases_id = 372"
        cursor.execute(sql)

        results = cursor.fetchall()
        for r in results:
            print(r['name'])
finally:
    connection.close()
