import sqlite3

class UserModel(): 

    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password
    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        print(cursor)
        select_user = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(select_user,(username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user
    @classmethod
    def find_by_id(cls,_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_by_id = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(select_by_id,(_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user