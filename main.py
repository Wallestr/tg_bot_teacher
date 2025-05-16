import telebot
from telebot import types

API_TOKEN = '7621086514:AAFV1-iE6HQwnMKwlXMQAToRxtkt1KXdavY'
bot = telebot.TeleBot(API_TOKEN)

users_id = []


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем клавиатуру с кнопками
    button_help = types.KeyboardButton("Помощь")
    button_add_user = types.KeyboardButton("Добавить получателя")
    button_send_message = types.KeyboardButton("Отправить сообщение")
    button_look_user_id = types.KeyboardButton("Посмотреть получателей")
    button_delete_user_id = types.KeyboardButton("Удалить ID получателя")
    markup.add(button_help, button_add_user, button_send_message, button_look_user_id, button_delete_user_id)

    bot.send_message(message.chat.id,
                     "Привет! Этот бот предоставляет удобные возможности для автоматизации рассылки сообщений. "
                     "Выберите одну из функций:",
                     reply_markup=markup)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: message.chat.id)
def handle_message(message):
    if message.text == "Помощь":
        bot.send_message(message.chat.id, "Я могу помочь вам с следующими командами:\n"
                                          "/start - Начать общение со мной\n"
                                          "/help - Получить список доступных команд")
    elif message.text == "Добавить получателя":
        mess = bot.send_message(message.chat.id, "Введите ID получателя")
        bot.register_next_step_handler(mess, add_recipient)
    elif message.text == "Отправить сообщение":
        mess = bot.send_message(message.chat.id, "Введите сообщение")
        bot.register_next_step_handler(mess, send_message)
    elif message.text == "Посмотреть получателей":
        mess = bot.send_message(message.chat.id, f"Все айди получателей: {users_id}")
    elif message.text == "Удалить юзер получателя":
        mess = bot.send_message(message.chat.id, "Введите id пользователя")
        bot.register_next_step_handler(mess, send_message)
    else:
        bot.send_message(message.chat.id, f"Вы сказали: {message.text}")


# Обработчик текстовых сообщений
@bot.message_handler(content_types=["text"])
def add_recipient(message):
    text = message.text
    users_id.append(text)
    bot.send_message(message.chat.id, f'Получатель {text} успешно добавлен')


def send_message(message):
    text = message.text
    for user_id in users_id:
        try:
            bot.send_message(user_id, f'Вам пришло сообщение: {text}')
        except Exception:
            bot.send_message(message.chat.id, f'Не получилось отправить сообщение такому юзеру: {user_id}')
    bot.send_message(message.chat.id, f"Сообщение '{text}' отправлено получателям.")


def delete_user_id(message):
    text = int(message.text)
    if text in users_id:
        users_id.remove(text)
        bot.send_message(message.chat.id, f"Получатель {text} успешно удалён.")
    else:
        bot.send_message(message.chat.id, f"Получатель с ID {text} не найден в списке.")




# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)