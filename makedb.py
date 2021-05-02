import telebot
import time
import os
import config
import sqlite3

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['test'])
def find_file_ids(message):
    conn = sqlite3.connect(config.database_name)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS music(
        rowsnum INT,
        right_ans TEXT,
        song TEXT,
        file_id TEXT);
        """)
    conn.commit()
    cnt = cur.execute("select COUNT(*) from music").fetchone()[0]
    for file in os.listdir('music/'):
        if file[-3:] == 'mp3':
            name = file[0:-4]
            parts = name.split(" - ")
            cnt = cnt + 1
            f = open('music/'+file, 'rb')
            msg = bot.send_voice(message.chat.id, f, None, timeout=10)
            bot.send_message(message.chat.id, msg.voice.file_id, reply_to_message_id=msg.message_id)
            row = [cnt, parts[-1], name, msg.voice.file_id]
            print(row)
            cur.execute("INSERT INTO music VALUES(?, ?, ?, ?);", row)
            conn.commit()
            time.sleep(3)
    cur.close()
