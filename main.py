import logging
import requests
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, Updater
import asyncio
import shutil
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import aiohttp
import os
import requests
from data import db_session
from data.users import User
from message_script import send_message
import datetime
import sqlalchemy
import schedule

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)

# GLOBAL PARAMS
TOKEN = '6428776449:AAEgccz1sgB9y06_QVCDGFnTZoyU74f_GEg'
LIST_MESSAGE = ['Я уже готов отправить твоё письмо. Напиши его', 'Кому ты хочешь отправить сообщение? Введи его адресс',
                'А какой заголовок?', 'Если ты хочешь отправить что-то ещё, скинь мне, а как закончишь, напиши (/send)']
LIST_TIMERS = ['На какое число ты хочешь создать таймер?', 'Записал число, на какой час?(0-23)',
               'Записал час, сколько минут(0-59)', 'Какой текст написать вам?',
               'Создал таймер. Всё будет сделано!']


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    await context.bot.send_photo(update.message.chat_id, open(f'sprites\hello_world.png', 'rb'))
    user = update.effective_user
    await update.message.reply_html(
        rf"""Привет {user.mention_html()}! Я Почта_Бот. Я готов помогать тебе со многими важными задачами
Чтобы ты хотел сделать, отправить сообщение(/mes) или поставить таймер для себя (/time)""")
    db_sess = db_session.create_session()
    new_user = User()
    new_user.id = update.message.chat_id
    new_user.name = user.mention_html()
    db_sess.add(new_user)
    db_sess.commit()


def job():
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        for timers in user.user_timers.split('-^system_separator_to_messages^-'):
            timers = timers.split('-^system_separator^-')
            if timers[0] == datetime.datetime.day and timers[1] == datetime.datetime.hour and timers[
                2] == datetime.datetime.minute:
                reminder(user.id, timers[3])


def reminder(user, mes):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={user}&text={mes}"
    print(requests.get(url).json())


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("""Привет, я Почти_Бот. Во мне включены(пока нет) 2 очень важные функции.
Во первых, я твоя личная почта, не такая продвинутая как @gmail, @mail и другие, но всё же
Я могу(пока не могу) отправлять за тебя письма другим людям на любую почту, оповещать тебя о новых сообщениях и рассылках
Во вторых, я также могу(не могу) быть для тебя ботом-напоминалкой. Написать или позвонить тебе в нужное время, чтобы ты ничего не забыл.
Буду очень рад, если ты будешь мною пользоваться, удачи, Друг:)""")


async def message(update, context):
    """Отправляет сообщение когда получена команда /message"""
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.id == update.message.chat_id:
            user.user_message = ''
            user.message_flag = True
            user.timer_flag = False
    db_sess.commit()
    await update.message.reply_text(LIST_MESSAGE[0])


async def timer_about(update, context):
    """Отправляет сообщение когда получена команда /time"""
    await update.message.reply_text(
        """Я уже готов создать для тебя новый таймер(/newtime) или открыть уже созданнные тобой(/mytime)""")


async def user_timers(update, context):
    """Отправляет сообщение когда получена команда /mytime"""
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.id == update.message.chat_id:
            timer = user.user_timers.split('-^system_separator_to_messages^-')
            timers = ''
            for elem in timer:
                elem = elem.split('-^system_separator^-')
                if len(elem) > 1:
                    timers += f'\n{elem[0]} числа в {elem[1]} часов {elem[2]} минут'
            await update.message.reply_text(f'Ваши таймеры:{timers}')


async def create_timer(update, context):
    """Отправляет сообщение когда получена команда /newtime"""
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.id == update.message.chat_id:
            user.timer_flag = True
            user.message_flag = False
        db_sess.commit()
    await update.message.reply_text(LIST_TIMERS[0])


async def return_to_start(update, context):
    """Отправляет сообщение когда получена команда /back"""
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.id == update.message.chat_id:
            user.timer_flag = False
            user.message_flag = False
            user.user_message = ''
            user.count_steps_timer = 1
            user.count_steps_message = 1
    db_sess.commit()
    if os.path.isdir(fr'data/user_documents/{update.message.chat_id}'):
        try:
            shutil.rmtree(fr'data/user_documents/{update.message.chat_id}')
        except Exception:
            pass
    await update.message.reply_text(
        """Чтобы ты хотел сделать, отправить сообщение(/mes) или поставить таймер для себя (/time)""")


async def downloader(update, context):
    fileName = update.message.document.file_name
    file = await context.bot.get_file(update.message.document)
    if not os.path.isdir(fr'data/user_documents/{update.message.chat_id}'):
        os.mkdir(fr'data/user_documents/{update.message.chat_id}')
    with open(fr'data/user_documents/{update.message.chat_id}/{fileName}', 'wb+') as f:
        response = requests.get(file.file_path)
        f.write(response.content)


async def send(update, context):
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.id == update.message.chat_id:
            message_data = user.user_message.split('-^system_separator^-')
            await update.message.reply_text(
                send_message(message_data[0], message_data[1], message_data[2], update.message.chat_id))
    await return_to_start(update, context)


async def text(update, context):
    """Отправляет сообщение когда получена команда /newtime"""
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.id == update.message.chat_id:
            if user.timer_flag:
                try:
                    if user.count_steps_timer == 1 and int(update.message.text) != float(update.message.text) or not (
                            1 <= int(update.message.text) <= 31):
                        raise Exception
                    if user.count_steps_timer == 2 and int(update.message.text) != float(update.message.text) or not (
                            0 <= int(update.message.text) <= 23):
                        raise Exception
                    if user.count_steps_timer == 3 and int(update.message.text) != float(update.message.text) or not (
                            0 <= int(update.message.text) <= 59):
                        raise Exception
                except Exception:
                    await update.message.reply_text(bad_input())
                    await return_to_start(update, context)
                if user.count_steps_timer < 4:
                    await update.message.reply_text((LIST_TIMERS[user.count_steps_timer]))
                    user.user_timers += update.message.text + '-^system_separator^-'
                    user.count_steps_timer += 1
                else:
                    user.user_timers += update.message.text + '-^system_separator_to_messages^-'
                    await update.message.reply_text((LIST_TIMERS[user.count_steps_timer]))
                    await return_to_start(update, context)
            if user.message_flag:
                if user.count_steps_message < 4:
                    await update.message.reply_text((LIST_MESSAGE[user.count_steps_message]))
                    user.user_message += update.message.text + '-^system_separator^-'
                    user.count_steps_message += 1
                else:
                    await update.message.reply_text((LIST_MESSAGE[user.count_steps_message]))
    db_sess.commit()


def bad_input():
    return 'Вы ввели что-то неправильно, попробуйте ещё раз'


def main():
    application = Application.builder().token('6428776449:AAEgccz1sgB9y06_QVCDGFnTZoyU74f_GEg').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("mes", message))
    application.add_handler(CommandHandler("time", timer_about))
    application.add_handler(CommandHandler("newtime", create_timer))
    application.add_handler(CommandHandler("back", return_to_start))
    application.add_handler(CommandHandler("mytime", user_timers))
    application.add_handler(CommandHandler("send", send))
    application.add_handler(MessageHandler(filters.Document.ALL, downloader))
    db_session.global_init("db/blogs.db")
    application.run_polling()


if __name__ == '__main__':
    main()
