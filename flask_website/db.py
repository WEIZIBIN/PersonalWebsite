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
