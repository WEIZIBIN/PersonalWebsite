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


def add_xiaoice(weibo_username):
    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO xiaoice (weibo_username) VALUES (%s, %s)'
            cursor.execute(sql, (weibo_username));
        connection.commit()
    finally:
        connection.close();


def get_xiaoice_list():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT id, weibo_username FROM xiaoice'
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                id = row[1]
                weibo_username = row[2]
                print
                "id=%s,weibo_username=%s" % (id, weibo_username)
        connection.commit()
    finally:
        connection.close();


def insert_xiaoice_log(xiaoice_id, log):
    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO xiaoice_log (xiaoice_id, log) VALUES (%s, %s)'
            cursor.execute(sql, (xiaoice_id, log));
        connection.commit()
    finally:
        connection.close();


def delete_xiaoice(id):
    try:
        with connection.cursor() as cursor:
            delete_xiaoice_sql = 'DELETE FROM xiaoice WHERE id = %s'
            cursor.execute(delete_xiaoice_sql, id);
            delete_xiaoice_log_sql = 'DELETE FROM xiaoice_log WHERE xiaoice_id = %s'
            cursor.execute(delete_xiaoice_log_sql, id);
        connection.commit()
    finally:
        connection.close();
