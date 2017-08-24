import pymysql.cursors
from flask_website.config import db_host, db_user, db_password, db_schema, db_port, db_charset

# Connect to the database
connection = pymysql.connect(host=db_host,
                             port=db_port,
                             user=db_user,
                             password=db_password,
                             db=db_schema,
                             charset=db_charset,
                             cursorclass=pymysql.cursors.DictCursor)


def add_xiaoice(weibo_username, weibo_password):
    with connection.cursor() as cursor:
        sql = 'INSERT INTO xiaoice (weibo_username, weibo_password) VALUES (%s, %s)'
        cursor.execute(sql, (weibo_username, weibo_password))
    connection.commit()


def get_xiaoice_list():
    with connection.cursor() as cursor:
        sql = 'SELECT id, weibo_username FROM xiaoice'
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            id = row['id']
            weibo_username = row['weibo_username']
            print("id=%s,weibo_username=%s" % (id, weibo_username))
    connection.commit()


def insert_xiaoice_log(xiaoice_id, msg, log_level, log_time):
    with connection.cursor() as cursor:
        sql = 'INSERT INTO xiaoice_log (xiaoice_id, msg, log_level, log_time) VALUES (%s, %s, %s, %s)'
        cursor.execute(sql, (xiaoice_id, msg, log_level, log_time))
    connection.commit()


def delete_xiaoice(id):
    with connection.cursor() as cursor:
        sql = 'DELETE FROM xiaoice WHERE id = %s'
        cursor.execute(sql, id);
    connection.commit()
