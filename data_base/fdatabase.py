import sqlite3 as sq

def create_db():
    '''Вспомогательная функция для создания таблиц БД '''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getData(self):
        try:
            self.__cur.execute(f"SELECT * FROM menu")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print("Ошибка получения данных из БД" + str(e))
        return []

if __name__ == '__main__':
    from app import app, connect_db
    db = connect_db()
    db = FDataBase(db)
    create_db()
