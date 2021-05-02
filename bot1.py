import telebot
from telebot import types
from config import TOKEN, database_name
import utils
import SQLighter
import random

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['game'])
def game(message):
    db = SQLighter.SQLighter(database_name)
    row = db.select_single(random.randint(1, utils.get_count_rows()))
    utils.set_user_game(message.chat.id, row[1], row[2])
    variants = utils.set_wrong_answers(row[1])
    markup = utils.generate_markup(variants)
    bot.send_voice(message.chat.id, row[3], reply_markup= markup)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add("/game")
    right_ans = utils.get_answer_for_user(message.chat.id)
    if message.text == right_ans[0]:
        utils.finish_user_game(message.chat.id)
        bot.send_message(message.chat.id, "Хорош, бро!!! Держи название трека:\n{}".format(right_ans[1]), reply_markup= markup)
    else:
        utils.finish_user_game(message.chat.id)
        bot.send_message(message.chat.id, "Неправильно:(( Это трек:\n{} \nНичего! попробуй еще раз!".format(right_ans[1]), reply_markup= markup)




if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.infinity_polling()
