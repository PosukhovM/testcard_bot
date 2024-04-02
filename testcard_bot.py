# подключение библиотек
# В google colab добавить: !pip install pyTelegramBotAPI
# В google colab добавить: !pip install Faker
# для установки необходимо в файл requirements.text добавить строки
# 'PyTelegramBotApi'
# 'faker'

from telebot import TeleBot, types
from faker import Faker
from datetime import datetime, timedelta


bot = TeleBot(token='СЮДА_СВОЙ_ТОКЕН_ТЕЛЕГРАМ_БОТА', parse_mode='html') # создание бота

faker = Faker('ru_RU') # утилита для генерации номеров кредитных карт

# объект клавиаутры
card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
card_type_keybaord.row(
    types.KeyboardButton(text='VISA'),
    types.KeyboardButton(text='MIR'),
)
# второй ряд кнопок
card_type_keybaord.row(
    types.KeyboardButton(text='Maestro'),
    types.KeyboardButton(text='Mastercard'),
)


# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    bot.send_sticker(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        sticker="CAACAgIAAxkBAAJMz2YJygi2RTL0BAimdmbsPEh1Fq3bAAIlRAACgSVhSDQ66yhpcG0sNAQ" # id стикера
    )
    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Привет! \nЯ умею генерировать тестовые банковской карты\n\n⬇️Выбери платёжную систему:⬇️', # текст сообщения
        reply_markup=card_type_keybaord,
    )
    
# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # проверяем текст сообщения на совпадение с текстом какой либо из кнопок
    # в зависимости от типа карты присваем занчение переменной 'card_type'
    if message.text.lower() in ['visa', 'виса', 'виза', 'visа', 'вisa','вiса', 'dbpf', 'dbcf', 'мшыф']:
        card_type = 'visa'
    elif message.text.lower() in ['mastercard', 'мастеркард', 'мастеркарт', 'мастерка', 'мастер', 'ьфыеуксфкв', 'vfcnthrfhl']:
        card_type = 'mastercard'
    elif message.text.lower() in ['maestro', 'маэстро', 'маестро', 'маестр', 'vftcnhj', 'ьфуыекщ']:
        card_type = 'maestro'
    elif message.text.lower() in ['mir', 'мир', 'мiр', 'vbh', 'ьшк']:
        card_type = 'mir'        
    else:
        # если текст не совпал ни с одной из кнопок
        # выводим ошибку
        bot.send_message(
            chat_id=message.chat.id,
            text='Не понимаю тебя 🤔\n\n⬇️Попробуй выбрать один из вариантов:⬇️',
            reply_markup=card_type_keybaord,
        )
        return

    @bot.message_handler(content_types=["sticker"])

    def message_handler_sticker(message: types.Sticker):
      bot.send_sticker(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        sticker="CAACAgIAAxkBAAJMzGYJxk8AASIstHVGX88HIEtyfcAlUgAChB4AAlL-8UvkaSsuqDjzkTQE" # id стикера
      )
      bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Стикеры — круто, мемы — ещё круче, но я всего лишь бот, который создаёт тестовые карты\n\n⬇️Попробуй выбрать один из вариантов:⬇️', # текст сообщения
        reply_markup=card_type_keybaord
      )


    # получаем номер тестовой карты выбранного типа
    # card_type может принимать одно из зачений ['maestro', 'mastercard', 'visa13', 'visa16', 'visa19',
    # 'amex', 'discover', 'diners', 'jcb15', 'jcb16']
    start_date = datetime.now() + timedelta(days=365*2)  # Текущая дата + 2 год
    card_secret = faker.credit_card_security_code(card_type)
    card_number = faker.credit_card_number(card_type)
    card_date = faker.credit_card_expire(start=start_date, end='+12y', date_format='%m/%y')
    # и выводим пользователю
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Тестовая карта {card_type.upper()}:\n\nНомер карты:  <code>{card_number}</code>\nДата:  <code>{card_date}</code>\nCVC/CVV:  <code>{card_secret}</code>'
    )


# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()