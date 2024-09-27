import sqlite3

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('db.db', check_same_thread=False)
        self.c = self.conn.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS forum(
            id INTEGER PRIMARY KEY,
            heading TEXT,
            subtitle,
            comments
        )""")

        # self.c.execute('DELETE FROM forum')
        # self.c.execute('INSERT INTO forum(id, heading, subtitle, comments) VALUES(0, ?, ?, ?)', ('Новости и нововведения.', 'Версия: 0.0.1\nДобавлено:\n●Список форумов.\n●Возможность оставить комментарии.\n●Создание поста.\n●Кнопка для выхода назад в меню.\n\nЧё думаете по этому поводу?)', '[]'))

        self.conn.commit()