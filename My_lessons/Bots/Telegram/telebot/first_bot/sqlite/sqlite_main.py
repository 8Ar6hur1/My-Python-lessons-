import telebot
import sqlite3
import os

TOKEN = telebot.TeleBot('7478465201:AAHmj3KuKW7IXonkz6s-eSRRHHFPYyBmDv8')

name = None
password = None

@TOKEN.message_handler(commands=['start'])
def start(message):

    folder_sql = '/sqlite/sqlite_list'

    if not os.path.exists(folder_sql):
        os.makedirs(folder_sql)

    db_sql = os.path.join(folder_sql, 'info.sql')

    conn = sqlite3.connect(db_sql)
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    
    conn.commit()
    cur.close()
    conn.close()

    TOKEN.send_message(message.chat.id, 'Привіт! Введи Ім\'я, а я тебе зареєструю')
    TOKEN.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()

    TOKEN.send_message(message.chat.id, 'Введи свій пароль')
    TOKEN.register_next_step_handler(message, user_pass)

def user_pass(message):
    global password
    password = message.text.strip()

    conn = sqlite3.connect('info.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, pass) VALUES ("%s","%s")' % (name, password))
    
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список користувачів', callback_data='user_list'))
    TOKEN.send_message(message.chat.id, 'Користувач зареєстрованний', reply_markup=markup)

@TOKEN.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('info.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    users_info = ''
    for el in users:
        users_info += f'Ім\'я: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()

    TOKEN.send_message(call.message.chat.id, users_info)

TOKEN.polling(non_stop=True)