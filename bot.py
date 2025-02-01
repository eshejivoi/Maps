import telebot
from telebot.apihelper import send_message
from config import *
from logic import *
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:  /show_city [город], /remember_city [город], /show_my_cities ")
    # Допиши команды бота

@bot.message_handler(commands=['visual_map'])
def visual(message):
    None



@bot.message_handler(commands=['show_city'])
def handle_show_city(message, update):
    city_name = message.text.split()[-1]
    # Реализуй отрисовку города по запросу
    user_id = message.chat.id
    keyboard = [
    [InlineKeyboardButton("Карта мира (шар)", callback_data='globe')],
    [InlineKeyboardButton("Плоская карта мира", callback_data='flat')]]
    manager.create_grapf(f'{user_id}.png',[city_name])
    query = update.callback_query
    query.answer()

    if query.data == 'globe':
        with open(f'D:/projectproject/maps/{user_id}.png', 'rb') as map:
            bot.send_photo(user_id, map)
    elif query.data == 'flat':
        with open(f'D:/projectproject/maps/{user_id}.png', 'rb') as map:
            bot.send_photo(user_id, map)


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    # Реализуй отрисовку всех городов
    if cities:
        manager.create_grapf(f'{message.chat.id}_cities.png', cities)
        with open(f'{message.chat.id}_sities.png', 'rb') as map:
            bot.send_photo(message.chat.id, map)
    else:
        bot.send_message(message.chat.id, "У вас пока что нет сохраненных проектов")



if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
