import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import aiohttp


#logging.basicConfig(
 #   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
#)

logger = logging.getLogger(__name__)


async def start(update, context):
    global info, markup
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"""Привет {user.mention_html()}! Я Почта_Бот. Я готов помогать тебе со многими важными задачами
Но для начала, давай зарегестрируемся
Твоё имя я уже взял. Какая у тебя фамилия?""", reply_markup=markup)
    info += 1


async def registration(update, context):
    global info
    """123"""
    if info == 1:
        await update.message.reply_html(
            rf"""Такс {update.message.text}, я понял кто ты.
    Ноо... Сколько тебе лет?""")
    if info == 2:
        await update.message.reply_html(
            rf"""Такс тебе {update.message.text} лет, я понял, какой ты взрослый.
    Напиши что-гинудь о себе""")
    if info == 3:
        await update.message.reply_html(
            rf"""Какой ты интересный,запишу
на этом регистрация завершена, если ты ввёл все верно смелее пиши /reg""")
    if info > 3:
        await update.message.reply_html("Ты уже вошел в аккаунт, но можешь выйти в настройках")
    info += 1


async def complete_registration(update, context):
    """Отправляет сообщение когда получена команда /start"""
    await update.message.reply_html(
        rf"""Пользователь успешно создан""")
    # СДЕЛАТЬ ЗАПИСЬ В БАЗУ ДАННЫХ ПОЛЬХОВАТЕЛЯ name, surname, age, info_user


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("""Привет, я Почти_Бот. Во мне включены(пока нет) 2 очень выжные функции.
    Во первых, я твоя личная почта, не такая продвинутая как @gmail, @mail и другие, но всё же
    Я могу(пока не могу) отправлять за тебя письма другим людям на любую почту, оповещать тебя о новых сообщениях и рассылках
    Во вторых, я также могу(не могу) быть для тебя ботом-напоминалкой. Написать или позвонить тебе в нужное время, чтобы ты ничего не забыл.
    Буду очень рад, если ты будешь мною пользоваться, удачи, Друг:)""")


async def profile(update, context):
    """Заходит в профиль пользователя"""
    await update.message.reply_html(
        rf"""Это твой личный профиль
Имя: name
Фамилия: surname
Возраст: age
О себе: info_user""")


def main():
    global info, name, surname, age, info_user

    info = 0  # 0 is name; 1 is surname; 2 is age; 3 is info
    application = Application.builder().token('6428776449:AAEgccz1sgB9y06_QVCDGFnTZoyU74f_GEg').build()
    reply_keyboard = [['/start', '/help', '/profile']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registration))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reg", complete_registration))
    application.add_handler(CommandHandler("profile", profile))
    # application.add_handler(CommandHandler("close", close_keyboard))
    # application.add_handler(CommandHandler("geocoder", geocoder))
    # application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
