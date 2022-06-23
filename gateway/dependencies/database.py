from statistics import multimode
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection
    
    def login(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM user WHERE username = '{}' AND password = '{}'".format(username, password)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        #check if user exist
        if result is None:
            return False,result
        return True,result

    def register(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        #check if user exist
        sql = "SELECT * FROM user WHERE username = '{}'".format(username)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            return False
        sql = "INSERT INTO user (username, password) VALUES ('{}', '{}')".format(username, password)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return True

    def get_user_id(self, username):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT id FROM user WHERE username = '{}'".format(username)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result['id']

    def download_file(self, file_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM file WHERE id = '{}'".format(file_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return True,result['location'],result['name']

    #add news
    def add_news(self, user_id, title, content, date,file_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO news (user_id, title, content, `date`,file_id) VALUES ('{}', '{}', '{}', '{}',{})".format(user_id, title, content, date,file_id)
        print(sql)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        
        #check if file upload success
        if cursor.lastrowid is None:
            return False
        return True

    def get_file_id(self, filename,filepath):
        cursor = self.connection.cursor(dictionary=True)
        print("test get_file_id_bawah")
        sql = "SELECT id FROM file WHERE name = '{}' AND location = '{}'".format(filename,filepath)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        print(result)
        return result['id']

    def add_news_file(self, title,content,file_id):
        cursor = self.connection.cursor(dictionary=True)
        #update news file_id that has title and content
        sql = "UPDATE news SET file_id = '{}' WHERE title = '{}' AND content = '{}'".format(file_id, title, content)
        cursor.execute(sql)
        self.connection.commit()

    def check_news_exist(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM news WHERE id = '{}'".format(id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return False
        return True

    def check_news_belong_to_user(self, id, user_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM news WHERE id = '{}' AND user_id = '{}'".format(id, user_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return False
        return True

    def edit_news(self, id, title, content,date):
        setsql=""
        if title is not 0:
            setsql = setsql + "title = '{}'".format(title)
        if content is not 0:
            if setsql is not "":
                setsql = setsql + ", "
            setsql = setsql + "content = '{}'".format(content)
        cursor = self.connection.cursor(dictionary=True)
        sql = "UPDATE news SET {}, `date` = '{}' WHERE id = '{}'".format(setsql, date, id)
        print(sql)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        if cursor.lastrowid is None:
            return False
        return True

    def delete_news(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "DELETE FROM news WHERE id = '{}'".format(id)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        if cursor.lastrowid is None:
            return False
        return True

    def get_news(self):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM news"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_news_by_id(self, news_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM news WHERE id = '{}'".format(news_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    def __del__(self):
        self.connection.close()


class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='departmentnews',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
