import time
import telebot
import random
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.by import By

import sqlite3

bot = telebot.TeleBot('token')

score21_user, score21_bot = 0, 0
login = None
admins = [747864333]


# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- КОМАНДЫ БОТА _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

@bot.message_handler(commands=['start'])
def start_message(message):
    mark = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Профиль💻')
    btn2 = types.KeyboardButton('Расписание🗓')
    btn3 = types.KeyboardButton('Ссылки🔗')
    btn4 = types.KeyboardButton('Помощь🆘')
    btn5 = types.KeyboardButton('Погода⛅️')
    btn6 = types.KeyboardButton('Игры🎮️')
    btn7 = types.KeyboardButton('Пожелание📝')
    mark.row(btn1, btn2)
    mark.row(btn3)
    mark.row(btn4, btn5)
    mark.row(btn6)
    mark.row(btn7)
    connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
    curbaz = connect.cursor()
    curbaz.execute('SELECT * FROM users')
    users = curbaz.fetchall()
    if len(users) % 10 <= 1 or len(users) % 10 >= 5:
        bot.send_message(message.chat.id,
                         f'<b>Привет</b>, {message.from_user.first_name} •⩊•! \nЯ твой бот-помощник по сайтам'
                         f' итмо. \nВ нашей команде уже: ' + str(
                             len(users)) + ' человек \nЧтобы узнать мои функции введи /help\nНапиши мне '
                                           '/reg, чтобы войти в ИТМО',
                         parse_mode='html', reply_markup=mark)
    else:
        bot.send_message(message.chat.id,
                         f'<b>Привет</b>, {message.from_user.first_name} •⩊•! \nЯ твой бот-помощник по сайтам итмо.'
                         f' \nВ нашей команде уже: ' + str(
                             len(users)) + ' человека \nЧтобы узнать мои функции введи /help'
                                           '\nНапиши мне /reg, чтобы войти в ИТМО',
                         parse_mode='html', reply_markup=mark)


@bot.message_handler(commands=['reg'])
def registration(message):
    global find_user
    connect = sqlite3.connect('itmohelpbot.sql')
    cursor = connect.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users(uid int, name varchar(50), passw varchar(50), wins int, rasp int)')
    connect.commit()
    cursor.close()
    connect.close()
    connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
    curbaz = connect.cursor()
    curbaz.execute('SELECT * FROM users')
    users = curbaz.fetchall()
    for el in users:
        if str(message.from_user.id) != str(el[0]):
            find_user = 0
        else:
            find_user = 1
            break

    if find_user == 0:
        mark = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Отмена')
        mark.row(btn1)
        bot.send_message(message.chat.id, 'Время регистрации, введи логин <b>itmoID</b>!', parse_mode='html',
                         reply_markup=mark)
        bot.register_next_step_handler(message, user_login_registration)

    else:
        bot.send_message(message.chat.id, 'Ты зареган!')


def user_login_registration(message):
    global login
    if message.text.lower() == 'отмена':
        mark = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Профиль💻')
        btn2 = types.KeyboardButton('Расписание🗓')
        btn3 = types.KeyboardButton('Ссылки🔗')
        btn4 = types.KeyboardButton('Помощь🆘')
        btn5 = types.KeyboardButton('Погода⛅️')
        btn6 = types.KeyboardButton('Игры🎮️')
        btn7 = types.KeyboardButton('Пожелание📝')
        mark.row(btn1, btn2)
        mark.row(btn3)
        mark.row(btn4, btn5)
        mark.row(btn6)
        mark.row(btn7)
        bot.send_message(message.chat.id, 'Регистрация отменена', reply_markup=mark)
    else:
        login = message.text.strip()
        bot.send_message(message.chat.id, 'Введи пароль!', parse_mode='html')
        bot.register_next_step_handler(message, user_password_registration)


def user_password_registration(message):
    mark = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Профиль💻')
    btn2 = types.KeyboardButton('Расписание🗓')
    btn3 = types.KeyboardButton('Ссылки🔗')
    btn4 = types.KeyboardButton('Помощь🆘')
    btn5 = types.KeyboardButton('Погода⛅️')
    btn6 = types.KeyboardButton('Игры🎮️')
    btn7 = types.KeyboardButton('Пожелание📝')
    mark.row(btn1, btn2)
    mark.row(btn3)
    mark.row(btn4, btn5)
    mark.row(btn6)
    mark.row(btn7)
    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, 'Регистрация отменена', reply_markup=mark)
    else:
        passw = message.text.strip()
        connect = sqlite3.connect('itmohelpbot.sql')
        cursor = connect.cursor()
        uid = message.from_user.id
        cursor.execute("INSERT INTO users (uid, name, passw, wins, rasp) VALUES('%s', '%s', '%s', '%s', '%s')" % (
            uid, login, passw, 0, 0))
        connect.commit()
        cursor.close()
        connect.close()
        bot.send_message(message.chat.id, 'Регистрация прошла успешно!', reply_markup=mark)


@bot.message_handler(commands=['new_login'])
def new_user_login(message):
    bot.send_message(message.chat.id, 'Введи новый логин')
    bot.register_next_step_handler(message, new_user_login_for_replace)


def new_user_login_for_replace(message):
    mark = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Профиль💻')
    btn2 = types.KeyboardButton('Расписание🗓')
    btn3 = types.KeyboardButton('Ссылки🔗')
    btn4 = types.KeyboardButton('Помощь🆘')
    btn5 = types.KeyboardButton('Погода⛅️')
    btn6 = types.KeyboardButton('Игры🎮️')
    btn7 = types.KeyboardButton('Пожелание📝')
    mark.row(btn1, btn2)
    mark.row(btn3)
    mark.row(btn4, btn5)
    mark.row(btn6)
    mark.row(btn7)
    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, 'Отменено', reply_markup=mark)
    else:
        newlog = message.text.strip()
        sqlite_connection = sqlite3.connect('itmohelpbot.sql')
        cursor = sqlite_connection.cursor()
        user_id = str(message.chat.id)
        cursor.execute('''UPDATE users SET name = ? WHERE uid = ?''', (newlog, user_id))

        sqlite_connection.commit()
        cursor.close()
        bot.send_message(message.chat.id, 'Логин изменен!', reply_markup=mark)


@bot.message_handler(commands=['new_pass'])
def new_user_password(message):
    bot.send_message(message.chat.id, 'Введи новый пароль')
    bot.register_next_step_handler(message, new_user_password_for_replace)


def new_user_password_for_replace(message):
    mark = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Профиль💻')
    btn2 = types.KeyboardButton('Расписание🗓')
    btn3 = types.KeyboardButton('Ссылки🔗')
    btn4 = types.KeyboardButton('Помощь🆘')
    btn5 = types.KeyboardButton('Погода⛅️')
    btn6 = types.KeyboardButton('Игры🎮️')
    btn7 = types.KeyboardButton('Пожелание📝')
    mark.row(btn1, btn2)
    mark.row(btn3)
    mark.row(btn4, btn5)
    mark.row(btn6)
    mark.row(btn7)
    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, 'Отменено', reply_markup=mark)
    else:
        new_password = message.text.strip()
        sqlite_connection = sqlite3.connect('itmohelpbot.sql')
        cursor = sqlite_connection.cursor()
        user_id = str(message.chat.id)
        cursor.execute('''UPDATE users SET passw = ? WHERE uid = ?''', (new_password, user_id))

        sqlite_connection.commit()
        cursor.close()
        bot.send_message(message.chat.id, 'Пароль изменен! ✅', reply_markup=mark)


@bot.message_handler(commands=['help'])
def helpmes(message):
    message_for_user_1 = '\n\n0) Я реагирую на любой регистр букв, можешь писать слова любыми буквами'
    message_for_user_2 = '\n\n1) Написав мне слово "ссылки", ты получишь важные ссылки, связанные с ИТМО'
    message_for_user_3 = '\n\n2) Напиши мне ключевые слова ссылок и я тебе их скину'
    message_for_user_4 = '\n\n3) Написав слово <b>"помощь"</b> или <b>"хелп"</b> я опять покажу тебе свои команды'
    message_for_user_5 = (
        '\n\n4) Если у тебя есть пожелания (как улучшить, что добавить), то напиши моему создателю.\nНапишие мне в '
        'одном'
        'сообщении слово "Пожелание" и напиши само пожелание\nНапример: "Пожелание сделайте майнинг!!!!"')
    message_for_user_6 = '\n\n5) Напиши мне /reg, чтобы войти в ИТМО'
    message_for_user_7 = '\n\nВсе мои функции также отображены у тебя в кнопках, используй их!'

    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name}, мои возможности:' + message_for_user_1 + message_for_user_2 +
                     message_for_user_3 + message_for_user_4 + message_for_user_5 + message_for_user_6 +
                     message_for_user_7,
                     parse_mode='html')


@bot.message_handler(commands=['code'])
def codemes(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='GitHub', callback_data='github')
    btn2 = types.InlineKeyboardButton(text='.txt', callback_data='txt')
    markup.row(btn1)
    markup.row(btn2)
    bot.send_message(message.chat.id, 'Выбери, как ты хочешь получить код', reply_markup=markup)


# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  Реакции БОТА _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  реакшн фо меседж БОТА _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
    global el, find_user, achievement_wins_info, achievement_check_study_schedule_info
    if message.text.lower() == 'пожелание📝':
        mark = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Отмена')
        btn2 = types.KeyboardButton('Что такое пожелание?')
        mark.row(btn1)
        mark.row(btn2)
        bot.send_message(message.chat.id, 'Введи свое пожелание и я отправлю его админу', reply_markup=mark)
        bot.register_next_step_handler(message, poj)

    elif message.text.lower() == 'расписание🗓':
        message_random = random.randint(0, 4)
        if message_random == 0:
            bot.send_message(message.chat.id, 'Ищу расписание по звёздам..')
        if message_random == 2:
            bot.send_message(message.chat.id, 'Пытаюсь найти расписание в слитых базах..')
        if message_random == 3:
            bot.send_message(message.chat.id, 'Анализирую my.itmo, может там что-то есть...')
        if message_random == 1:
            bot.send_message(message.chat.id, 'Сейчас будет magic (вполне реально)')
        if message_random == 4:
            bot.send_message(message.chat.id, 'Вот я тоже ленивый, но ради тебя зайду на my.itmo')
        message_about_study_schedule = ''
        teacher_info = []
        auditorium_info = []
        other_info = []
        lesson_info_for_out = []
        connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
        curbaz = connect.cursor()
        curbaz.execute('SELECT * FROM users')
        users = curbaz.fetchall()

        for el in users:
            if str(message.from_user.id) == str(el[0]):
                find_user = 0
                break
            else:
                find_user = 1

        if find_user == 0:
            sqlite_connection = sqlite3.connect('itmohelpbot.sql')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            user_id = str(el[0])
            value = int(el[4]) + 1
            cursor.execute('''UPDATE users SET rasp = ? WHERE uid = ?''', (value, user_id))

            sqlite_connection.commit()
            cursor.close()
            user_login = el[1]
            user_pass = el[2]
            driver = webdriver.Chrome()
            driver.get(
                "https:/my.itmo.ru/login")
            time.sleep(2)
            login_itmo = driver.find_element(By.ID, "username")
            login_itmo.clear()
            login_itmo.send_keys(str(user_login))

            password_itmo = driver.find_element(By.ID, "password")
            password_itmo.clear()
            password_itmo.send_keys((str(user_pass)))
            button_in = driver.find_element(By.ID, "kc-login")
            button_in.click()
            time.sleep(4)

            para = driver.find_elements(By.CLASS_NAME, 'title')
            time_start = driver.find_elements(By.CLASS_NAME, 'time-start')
            time_end = driver.find_elements(By.CLASS_NAME, 'time-end')
            lesson_info = driver.find_elements(By.CLASS_NAME, 'lesson-info')
            for k in range(len(lesson_info)):
                # if len(lesson2[k].text) > 0 and lesson2[k].text.lower() != 'коллоквиум':
                lesson_info_for_out.append(lesson_info[k].text)
            if len(para) > 2:
                if len(lesson_info_for_out) > 0:
                    for i in range(0, len(lesson_info_for_out) - 1, 3):
                        teacher_info.append(lesson_info_for_out[i])
                        auditorium_info.append(lesson_info_for_out[i + 1])
                        other_info.append(lesson_info_for_out[i + 2])
                for i in range(1, len(para) - 1):
                    message_about_study_schedule += 'Пара ' + str(i) + ' ⌛️ : ' + str(
                        time_start[i - 1].text) + '-' + str(
                        time_end[i - 1].text) + '\n📖: ' + str(
                        para[i].text) + ' ' + other_info[i - 1].lower() + '\n🤓: ' + teacher_info[i - 1] + '\n🏕: ' + \
                                                    auditorium_info[i - 1] + '\n' '*' + '\n'
                for i in range(1, 4):
                    message_about_study_schedule = message_about_study_schedule.replace('*',
                                                                                        '\n-_-_-_-_-_-_-_-_-_-_-_-_-\n',
                                                                                        1)
                message_about_study_schedule = message_about_study_schedule.replace('*', '')
                bot.send_message(message.chat.id, '<b>-_-_-_Расписание_-_-_-</b>\n\n' + message_about_study_schedule,
                                 parse_mode='html')
            else:
                bot.send_message(message.chat.id, 'Сегодня пар нет, кайфуем')
        else:
            bot.send_message(message.chat.id, 'Пройди регистрацию /reg')

    elif message.text.lower() == 'профиль💻':
        mark = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Изменить логин🗓🆕')
        btn2 = types.KeyboardButton('Изменить пароль🗓🆕')
        btn3 = types.KeyboardButton('Вернуться в меню')
        btn4 = types.KeyboardButton('Удалить профиль')
        mark.row(btn1, btn2)
        mark.row(btn3)
        mark.row(btn4)
        connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
        curbaz = connect.cursor()
        curbaz.execute('SELECT * FROM users')
        users = curbaz.fetchall()
        i = 0
        for el in users:
            if str(message.from_user.id) == str(el[0]):
                find_user = 0
                i += 1
                break
            else:
                find_user = 1
                i += 1
        if find_user == 0:
            achievement_wins = int(el[3])
            achievement_check_study_schedule = int(el[4])

            if achievement_wins <= 100:
                achievement_wins_info = 'Бронза'
            elif (achievement_wins < 300) and (achievement_wins > 100):
                achievement_wins_info = 'Серебро'
            elif achievement_wins == 300:
                achievement_wins_info = 'Золото'
            if achievement_check_study_schedule <= 40:
                achievement_check_study_schedule_info = 'Бронза'
            elif (achievement_check_study_schedule < 100) and (achievement_check_study_schedule > 40):
                achievement_check_study_schedule_info = 'Серебро'
            elif achievement_check_study_schedule == 100:
                achievement_check_study_schedule_info = 'Золото'
            if (achievement_wins_info == achievement_check_study_schedule_info) and (achievement_wins_info == 'Золото'):
                status_of_user = 'Бог🙊'
            elif achievement_wins_info == achievement_check_study_schedule_info and achievement_wins_info == 'Серебро':
                status_of_user = 'Красавчик👿'
            else:
                status_of_user = 'Юзер👨🏻‍💻'
            for ele in admins:
                if str(ele) == str(message.chat.id):
                    status_of_user = '<b><i>admin🦄</i></b>'
            bot.send_message(message.chat.id,
                             '-------<b>ТВОЙ ПРОФИЛЬ</b>-------\n\n\n-_-_-<b><i>ОСНОВНОЕ</i></b>-_-_-\n\n' +
                             f'⛄️ <b>Имя аккаунта</b>: {message.from_user.first_name}' +
                             '\n<b>Статус:</b> ' + status_of_user + '\n🆔 <b>Уникальный id:</b>  <i>' + str(
                                 el[0]) + '</i>\n📈 По счету в боте: ' + str(i) +
                             '\n\n\n-_-_-<b><i>ИТМО ID</i></b>-_-_-\n' + '\n🔒 <b>Логин ItmoID:</b> <i>' + str(
                                 el[1]) + '</i>\n🗝️ <b>Пароль ItmoID:</b> <i>' +
                             str(el[2]) + '\n\n\n-_-_-<b>АЧИВКИ</b>-_-_-\n' + '</i>\n🎮️ <b>Побед в играх:</b> ' + str(
                                 el[3]) + '\n🔰 <b>Ачивка 1</b> (победы) прогресс <b>' + str(
                                 achievement_wins) + '/300</b> - ' + achievement_wins_info +
                             '\n👀 <b>Ачивка 2</b> (просмотров расписания) прогресс <b>' + str(
                                 achievement_check_study_schedule) + '/100</b> - ' +
                             achievement_check_study_schedule_info,
                             parse_mode='html', reply_markup=mark)
            bot.register_next_step_handler(message, edit_profile)
        else:
            bot.send_message(message.chat.id, 'Пройди регистрацию! /reg')

    elif message.text.lower() == 'игры🎮️':
        markup = types.ReplyKeyboardMarkup()
        btn10 = types.KeyboardButton('🪨✂️🧻')
        btn11 = types.KeyboardButton('21')
        btn12 = types.KeyboardButton('Вернуться в меню')
        markup.row(btn10, btn11)
        markup.row(btn12)
        bot.send_message(message.chat.id, 'Игры', reply_markup=markup)
        bot.register_next_step_handler(message, games)

    elif message.text.lower() == 'погода⛅️':
        driver = webdriver.Chrome()
        driver.get('https://yandex.ru/pogoda/saint-petersburg?lat=60.050076&lon=30.340248')
        time.sleep(6)
        temperature_info = driver.find_element(By.XPATH, '//*[@id="content_left"]/div[2]/div[1]/div[5]/a/div/div[1]')
        analytics_weather_info = driver.find_element(By.XPATH,
                                                     '//*[@id="content_left"]/div[2]/div[1]/div[5]/a/div/div[2]')
        humidity_weather_info = driver.find_element(By.XPATH, '//*[@id="content_left"]/div[2]/div[1]/div[7]/div[2]')
        pressure_weather_info = driver.find_element(By.XPATH, '//*[@id="content_left"]/div[2]/div[1]/div[7]/div[3]')
        wind_weather_info = driver.find_element(By.XPATH, '//*[@id="content_left"]/div[2]/div[1]/div[7]/div[1]')
        analytics_weather_info_text = analytics_weather_info.text
        analytics_weather_info_text = analytics_weather_info_text.replace('\n', ' ')
        analytics_weather_info_text = analytics_weather_info_text.replace('Ощущается', '\nОщущается')
        bot.send_message(message.chat.id,
                         'Сейчас в Петербурге: ' + analytics_weather_info_text + '\n' + '-' + '\n<b>Температура:</b> ' +
                         temperature_info.text + ' гр.'
                         + '\n' + '-' + '\n' + '<b>Ветер:</b> ' + wind_weather_info.text + '\n' + '-' + '\n' +
                         '<b>Влажность:</b> ' + humidity_weather_info.text
                         + '\n' + '-' + '\n' + '<b>Давление:</b> ' + pressure_weather_info.text, parse_mode='html')

    elif message.text.lower() == 'помощь🆘':
        helpmes(message)
    elif message.text.lower() == 'хелп':
        helpmes(message)

    elif message.text.lower() == 'итмо':
        bot.send_message(message.chat.id, 'Главный сайт - https://itmo.ru/')
    elif message.text.lower() == 'itmo':
        bot.send_message(message.chat.id, 'Главный сайт - https://itmo.ru/')
    elif message.text.lower() == 'хелпдеск':
        bot.send_message(message.chat.id, 'HelpDesk - https://helpdesk.itmo.ru/servicedesk/customer/user/profile')
    elif message.text.lower() == 'хелп деск':
        bot.send_message(message.chat.id, 'HelpDesk - https://helpdesk.itmo.ru/servicedesk/customer/user/profile')
    elif message.text.lower() == 'helpdesk':
        bot.send_message(message.chat.id, 'HelpDesk - https://helpdesk.itmo.ru/servicedesk/customer/user/profile')
    elif message.text.lower() == 'help desk':
        bot.send_message(message.chat.id, 'HelpDesk - https://helpdesk.itmo.ru/servicedesk/customer/user/profile')
    elif message.text.lower() == 'май итмо':
        bot.send_message(message.chat.id, 'My.Itmo - https://my.itmo.ru/schedule?date=2023-09-21')
    elif message.text.lower() == 'майитмо':
        bot.send_message(message.chat.id, 'My.Itmo - https://my.itmo.ru/schedule?date=2023-09-21')
    elif message.text.lower() == 'myitmo':
        bot.send_message(message.chat.id, 'My.Itmo - https://my.itmo.ru/schedule?date=2023-09-21')
    elif message.text.lower() == 'my itmo':
        bot.send_message(message.chat.id, 'My.Itmo - https://my.itmo.ru/schedule?date=2023-09-21')
    elif message.text.lower() == 'бжд':
        bot.send_message(message.chat.id, 'Itmo Lifesafety (БЖД) - https://lifesafety.itmo.ru/m/my/')
    elif message.text == 'id':
        bot.send_message(message.chat.id, message.chat.id)

    elif message.text.lower() == 'ссылки🔗':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='TG', callback_data='tg')
        btn2 = types.InlineKeyboardButton(text='VK', callback_data='vk')
        btn3 = types.InlineKeyboardButton(text='BROWSER', callback_data='br')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, 'Выбери, где ты хочешь получить ссылки', reply_markup=markup)

        # -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- КМН _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

    elif message.text.lower() == '🪨✂️🧻':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='🪨', callback_data='1')
        btn2 = types.InlineKeyboardButton(text='✂️', callback_data='2')
        btn3 = types.InlineKeyboardButton(text='🧻', callback_data='3')
        markup.row(btn1, btn2, btn3)
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, Выбери чем ходишь',
                         reply_markup=markup)

    elif message.text.lower() == 'кмн камень':
        # 0 - камень 1 - ножницы 2 - бумага
        random_kmn_motion = random.randint(0, 3)
        if random_kmn_motion == 0:
            bot.reply_to(message, 'Я тоже выбрал камень! Ничья!')
        elif random_kmn_motion == 1:
            bot.reply_to(message, 'Мой ход - ножницы, ты победил(\n+1 балл в копилку')
            connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
            curbaz = connect.cursor()
            curbaz.execute('SELECT * FROM users')
            users = curbaz.fetchall()

            for el in users:
                if str(message.from_user.id) == str(el[0]):
                    find_user = 0
                    break
                else:
                    find_user = 1

            if find_user == 0:
                sqlite_connection = sqlite3.connect('itmohelpbot.sql')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")
                id = str(el[0])
                parol = int(el[3]) + 1
                cursor.execute('''UPDATE users SET wins = ? WHERE uid = ?''', (parol, id))

                sqlite_connection.commit()
                cursor.close()
        else:
            bot.reply_to(message, 'Ха-а-ах, легко, мой выбор - бумага')
    elif message.text.lower() == 'кмн ножницы':
        # 0 - камень 1 - ножницы 2 - бумага
        random_kmn_motion = random.randint(0, 3)
        if random_kmn_motion == 0:
            bot.reply_to(message, 'Угадай кто победитель?')
            time.sleep(1)
            bot.reply_to(message, 'Бот - победитель. Не зря взял камень')
        elif random_kmn_motion == 1:
            bot.reply_to(message, 'И у меня ножницы!')
        else:
            bot.reply_to(message, 'Сегодня не мой день... Меня разрезали\n+1 балл в копилку')
            connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
            curbaz = connect.cursor()
            curbaz.execute('SELECT * FROM users')
            users = curbaz.fetchall()

            for el in users:
                if str(message.from_user.id) == str(el[0]):
                    find_user = 0
                    break
                else:
                    find_user = 1

            if find_user == 0:
                sqlite_connection = sqlite3.connect('itmohelpbot.sql')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")
                id = str(el[0])
                parol = int(el[3]) + 1
                cursor.execute('''UPDATE users SET wins = ? WHERE uid = ?''', (parol, id))

                sqlite_connection.commit()
                cursor.close()
    elif message.text.lower() == 'кмн бумага':
        # 0 - камень 1 - ножницы 2 - бумага
        random_kmn_motion = random.randint(0, 3)
        if random_kmn_motion == 0:
            bot.reply_to(message, 'Ты серьезно? почему бумага? ты победил...\n+1 балл в копилку')
            connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
            curbaz = connect.cursor()
            curbaz.execute('SELECT * FROM users')
            users = curbaz.fetchall()

            for el in users:
                if str(message.from_user.id) == str(el[0]):
                    find_user = 1
                    break
                else:
                    find_user = 0

            if find_user == 1:
                sqlite_connection = sqlite3.connect('itmohelpbot.sql')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")
                id = str(el[0])
                parol = int(el[3]) + 1
                cursor.execute('''UPDATE users SET wins = ? WHERE uid = ?''', (parol, id))

                sqlite_connection.commit()
                cursor.close()
        elif random_kmn_motion == 1:
            bot.reply_to(message,
                         f'Не в этот раз, {message.from_user.first_name}, мои ножницы осилили твою бумагу')
        else:
            bot.reply_to(message, 'И вот снова у нас ничья)')
    elif 'ans' in message.text:
        for elements in admins:
            if str(elements) == str(message.from_user.id):
                user_id = ''
                message_from_admin = str(message.text)
                message_from_admin = message_from_admin.replace('ans', '')
                for i in message_from_admin:
                    if i in '0123456789':
                        user_id += i
                message_from_admin = message_from_admin.replace(user_id, '')
                message_from_admin = message_from_admin.strip()
                message_from_admin = '"' + message_from_admin + '"'
                bot.send_message(user_id, 'Ответ от админа: ' + message_from_admin)
            else:
                bot.reply_to(message, 'Такого я пока что не знаю')
                bot.send_message(message.chat.id,
                                 'Вводи в любой момент команду /help (можно отправить слово "помощь\хелп", чтобы '
                                 'не забывать, что я могу!\nТакже, ты можешь написать /code и увидеть исходный код')

    else:
        bot.reply_to(message, 'Такого я пока что не знаю')
        bot.send_message(message.chat.id,
                         'Вводи в любой момент команду /help (можно отправить слово "помощь\хелп", чтобы не '
                         'забывать, что я могу!\nТакже, ты можешь написать /code и увидеть исходный код')


def edit_profile(message):
    markup = types.ReplyKeyboardMarkup()
    btn10 = types.KeyboardButton('Отмена')
    markup.row(btn10)
    mark = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Профиль💻')
    btn2 = types.KeyboardButton('Расписание🗓')
    btn3 = types.KeyboardButton('Ссылки🔗')
    btn4 = types.KeyboardButton('Помощь🆘')
    btn5 = types.KeyboardButton('Погода⛅️')
    btn6 = types.KeyboardButton('🪨✂️🧻')
    btn7 = types.KeyboardButton('Пожелание📝')
    mark.row(btn1, btn2)
    mark.row(btn3)
    mark.row(btn4, btn5)
    mark.row(btn6)
    mark.row(btn7)
    if message.text.lower() == 'вернуться в меню':
        bot.send_message(message.chat.id, 'Вы в меню!', reply_markup=mark)
    elif message.text.lower() == 'изменить логин🗓🆕':
        bot.send_message(message.chat.id, 'Смена Логина', reply_markup=markup)
        new_user_login(message)
    elif message.text.lower() == 'изменить пароль🗓🆕':
        bot.send_message(message.chat.id, 'Смена пароля', reply_markup=markup)
        new_user_password(message)
    elif message.text.lower() == 'удалить профиль':
        connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
        curbaz = connect.cursor()
        id = message.chat.id
        curbaz.execute('''DELETE FROM users WHERE uid = ?''', (id,))
        connect.commit()
        bot.send_message(message.chat.id, 'Профиль удален', reply_markup=mark)
    else:
        bot.send_message(message.chat.id, 'Выбери действие из кнопок!')
        bot.register_next_step_handler(message, edit_profile)


def games(message):
    markup = types.ReplyKeyboardMarkup()
    btn10 = types.KeyboardButton('Отмена')
    markup.row(btn10)
    mark = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Профиль💻')
    btn2 = types.KeyboardButton('Расписание🗓')
    btn3 = types.KeyboardButton('Ссылки🔗')
    btn4 = types.KeyboardButton('Помощь🆘')
    btn5 = types.KeyboardButton('Погода⛅️')
    btn6 = types.KeyboardButton('Игры🎮️')
    btn7 = types.KeyboardButton('Пожелание📝')
    mark.row(btn1, btn2)
    mark.row(btn3)
    mark.row(btn4, btn5)
    mark.row(btn6)
    mark.row(btn7)
    if message.text.lower() == 'вернуться в меню':
        bot.send_message(message.chat.id, 'Вы в меню!', reply_markup=mark)
    elif message.text.lower() == '21':
        # markup = types.ReplyKeyboardMarkup()
        # btn10 = types.KeyboardButton('Еще')
        # btn11 = types.KeyboardButton('Стоп')
        # markup.row(btn10)
        # markup.row(btn11)
        # global score21_user
        # global score21_bot
        # a = random.randint(1, 11)
        # b = random.randint(1, 10)
        # score21_user = score21_user + a + b
        # a = random.randint(1, 11)
        # b = random.randint(1, 10)
        # score21_bot = score21_bot + a + b
        # for i in range(0, 3):
        #     if score21_bot < 21:
        bot.send_message(message.chat.id, 'Разработка...')
        bot.register_next_step_handler(message, games)
    elif message.text.lower() == '🪨✂️🧻':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='🪨', callback_data='1')
        btn2 = types.InlineKeyboardButton(text='✂️', callback_data='2')
        btn3 = types.InlineKeyboardButton(text='🧻', callback_data='3')
        markup.row(btn1, btn2, btn3)
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, Выбери чем ходишь',
                         reply_markup=markup)
        bot.register_next_step_handler(message, games)
    else:
        bot.send_message(message.chat.id, 'Используй кнопки!')
        bot.register_next_step_handler(message, games)


def poj(message):
    mark = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Профиль💻')
    btn2 = types.KeyboardButton('Расписание🗓')
    btn3 = types.KeyboardButton('Ссылки🔗')
    btn4 = types.KeyboardButton('Помощь🆘')
    btn5 = types.KeyboardButton('Погода⛅️')
    btn6 = types.KeyboardButton('Игры🎮️')
    btn7 = types.KeyboardButton('Пожелание📝')
    mark.row(btn1, btn2)
    mark.row(btn3)
    mark.row(btn4, btn5)
    mark.row(btn6)
    mark.row(btn7)
    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, 'Пожелание отменено', reply_markup=mark)
    elif message.text.lower() == 'что такое пожелание?':
        bot.send_message(message.chat.id, '<b>Пожелание</b> - это возможность задать вопрос моему админу, попросить '
                                          'добавить мне новые функции или же просто выразить свою благодарность.'
                                          '\n<b>Админ</b> ответит как только сможет', parse_mode='html')
        bot.register_next_step_handler(message, poj)
    else:
        s = message.text
        s = s.lower()
        s = s.strip()
        s = '"' + s + '"'
        bot.send_message(747864333, 'Пожелание от ' + str(message.chat.id) + ': ' + s + '\nПользователь: ' + str(
            message.from_user.first_name))
        bot.send_message(message.chat.id, 'Пожелание отправлено админу ✅, он ответит по-возможности', reply_markup=mark)


# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  Callback БОТА _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_mess(callback):
    # 0 - камень 1 - ножницы 2 - бумага
    global el, find_user, find_user
    random_kmn_motion = random.randint(0, 3)
    if callback.data == '1':
        if random_kmn_motion == 0:
            bot.send_message(callback.message.chat.id, 'Я тоже выбрал камень! Ничья!')
        elif random_kmn_motion == 1:
            bot.send_message(callback.message.chat.id, 'Мой ход - ножницы, ты победил(\n+1 балл в копилку')
            connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
            curbaz = connect.cursor()
            curbaz.execute('SELECT * FROM users')
            users = curbaz.fetchall()

            for el in users:
                if str(callback.message.chat.id) == str(el[0]):
                    find_user = 0
                    break
                else:
                    find_user = 1

            if find_user == 0:
                sqlite_connection = sqlite3.connect('itmohelpbot.sql')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")
                id = str(el[0])
                wins_info = int(el[3]) + 1
                cursor.execute('''UPDATE users SET wins = ? WHERE uid = ?''', (wins_info, id))

                sqlite_connection.commit()
                cursor.close()
        else:
            bot.send_message(callback.message.chat.id, 'Ха-а-ах, легко, мой выбор - бумага')
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == '2':
        if random_kmn_motion == 0:
            bot.send_message(callback.message.chat.id, 'Угадай кто победитель?')
            time.sleep(1)
            bot.send_message(callback.message.chat.id, 'Бот - победитель. Не зря взял камень')
        elif random_kmn_motion == 1:
            bot.send_message(callback.message.chat.id, 'И у меня ножницы!')
        else:
            bot.send_message(callback.message.chat.id, 'Сегодня не мой день... Меня разрезали\n+1 балл в копилку')
            connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
            curbaz = connect.cursor()
            curbaz.execute('SELECT * FROM users')
            users = curbaz.fetchall()

            for el in users:
                if str(callback.message.chat.id) == str(el[0]):
                    find_user = 0
                    break
                else:
                    find_user = 1

            if find_user == 0:
                sqlite_connection = sqlite3.connect('itmohelpbot.sql')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")
                id = str(el[0])
                wins_info = int(el[3]) + 1
                cursor.execute('''UPDATE users SET wins = ? WHERE uid = ?''', (wins_info, id))

                sqlite_connection.commit()
                cursor.close()
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == '3':
        if random_kmn_motion == 0:
            bot.send_message(callback.message.chat.id,
                             'Ты серьезно?! почему бумага? \nты победил...\n+1 балл в копилку')
            connect = sqlite3.connect('itmohelpbot.sql')  # создание базы
            curbaz = connect.cursor()
            curbaz.execute('SELECT * FROM users')
            users = curbaz.fetchall()

            for el in users:
                if str(callback.message.chat.id) == str(el[0]):
                    find_user = 0
                    break
                else:
                    find_user = 1

            if find_user == 0:
                sqlite_connection = sqlite3.connect('itmohelpbot.sql')
                cursor = sqlite_connection.cursor()
                id = str(el[0])
                wins_info = int(el[3]) + 1
                cursor.execute('''UPDATE users SET wins = ? WHERE uid = ?''', (wins_info, id))

                sqlite_connection.commit()
                cursor.close()
        elif random_kmn_motion == 1:
            bot.send_message(callback.message.chat.id, 'Не в этот раз, мои ножницы осилили твою бумагу')
        else:
            bot.send_message(callback.message.chat.id, 'И вот снова у нас ничья)')
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'tg':
        bot.send_message(callback.message.chat.id,
                         '<b>Тг:</b> \nhttps://t.me/addlist/0xk0Edml0KsyZDJi - папка с кучей каналов итмо'
                         '\n@Olimpiads_ru_bot - хакатоны и олимпиады\n@itmo_career_center_bot - доступ в клуб "Карьера"'
                         '\nhttps://t.me/+HdedkrBbI0YwYmFi - чат по практике и стажировкам\nhttps://t.me/megabytecode - мегабайт',
                         parse_mode='html')
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'vk':
        bot.send_message(callback.message.chat.id,
                         '<b>Вк:</b>\nhttps://vk.com/kb_ballroom - Кронверские барсы\nhttps://vk.com/itmobuddy - buddy system'
                         '\nhttps://vk.com/lifesafety_itmo - бжд\nhttps://vk.com/club_nirs_itmo - учебный центр студ. науки'
                         '\nhttps://vk.com/fltc.itmo - языки\nhttps://vk.com/itmostudents - itmo students'
                         '\nhttps://vk.com/alumni.itmo - выпускники\nhttps://vk.com/mb.news - магабайт'
                         '\nhttps://vk.com/yagodnoeitmo - Ягодное\nhttps://vk.com/itmo_uni - группа итмо на англ'
                         '\nhttps://vk.com/scamt - научный центр scamt\nhttps://vk.com/itmo.expert - itmo expert'
                         '\nhttps://vk.com/physics.itmo - новый физтех\nhttps://vk.com/itmomegabattle - мегабатл'
                         '\nhttps://vk.com/adapteritmo - адаптер\nhttps://vk.com/pro.itmo - про итмо'
                         '\nhttps://vk.com/artmo.club - клуб артмо\nhttps://vk.com/itmo_speaking_club - speaking club'
                         '\nhttps://vk.com/muzclubitmo - клуб живой звук\nhttps://vk.com/ktu.crew - КТУ'
                         '\nhttps://vk.com/health_itmo - здоровье \nhttps://vk.com/itmoru - оф. страница ИТМО',
                         parse_mode='html')
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'br':
        bot.send_message(callback.message.chat.id,
                         '<b>Браузер:</b>\nГлавный сайт - https://itmo.ru/\nMy.Itmo - https://my.itmo.ru/schedule?date=2023-09-21'
                         '\nHelpDesk - https://helpdesk.itmo.ru/servicedesk/customer/user/profile\n'
                         'Ису Итмо - https://isu.ifmo.ru/pls/apex/f?p=2143:1:109969888406175\n'
                         'Itmo Lifesafety (БЖД) - https://lifesafety.itmo.ru/m/my/', parse_mode='html')
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'github':
        bot.send_message(callback.message.chat.id, 'https://github.com/WALTANN/ItmoHelper-bot')
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'txt':
        bot.send_message(callback.message.chat.id,
                         "Код пока не выложен :((, но ты можешь посмотреть его на GitHub'е - https://github.com/WALTANN/ItmoHelper-bot")
        bot.delete_message(callback.message.chat.id, callback.message.message_id)


bot.polling(none_stop=True, interval=0)
