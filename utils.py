import shelve
from telebot import types
from random import shuffle
from SQLighter import SQLighter
from config import shelve_name, database_name
import random


def count_rows():
    db = SQLighter(database_name)
    rnum = db.count_rows()
    with shelve.open(shelve_name) as conn:
        conn["rowsnum"] = rnum

def get_count_rows():
    with shelve.open(shelve_name) as conn:
        return conn["rowsnum"]

def set_user_game(chat_id, estimated_answer, song):
    with shelve.open(shelve_name) as conn:
        conn[str(chat_id)] = [estimated_answer, song]

def finish_user_game(chat_id):
    with shelve.open(shelve_name) as conn:
        del conn[str(chat_id)]


def set_wrong_answers(name):
    ans = [name]
    db = SQLighter(database_name)
    while len(ans) < 6:
        temp = db.select_single(random.randint(1, get_count_rows()))
        if temp[1] not in ans:
            ans.append(temp[1])
    return ans

def get_answer_for_user(chat_id):
    with shelve.open(shelve_name) as conn:
        try:
            return conn[str(chat_id)]
        except KeyError:
            return None


def generate_markup(arr):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    shuffle(arr)
    for ans in arr:
        markup.add(ans)
    return markup