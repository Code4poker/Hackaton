import sqlite3


# добавить информацию в базу данных
def add(user_id, nickname, answer, question):
    connect = sqlite3.connect('users_answer_table')
    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INT, name TEXT, answer TEXT, question TEXT)''')
    connect.commit()
    # добавление значений в список
    user_information = [user_id, nickname, answer, question]
    cursor.execute("INSERT INTO users VALUES(?,?,?,?);", user_information)
    connect.commit()


# удаление человека из базы данных
def delete_client(user_id, nickname, answer, question):
    connect = sqlite3.connect('users_answer_table')
    cursor = connect.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {user_id} AND name = {nickname}"  # возможно не верно написано
                   f" AND answer = {answer} AND question = {question}")
    connect.commit()


# удалить всю базу данных
def delete_db():
    connect = sqlite3.connect('users_answer_table')
    cursor = connect.cursor()
    cursor.execute("DROP TABLE users")
    connect.commit()


# вывод значений из базы данных
def search():
    connect = sqlite3.connect('users_answer_table')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users")
    all_results = cursor.fetchall()
    print(all_results)
