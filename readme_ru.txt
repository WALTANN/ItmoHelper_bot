^^ItmoHelper bot^^ - бот-парсер. Благодаря библиотеке selenium он находит элементы на сайте Itmo и присылает их пользователю.
Также используется библиотека sqlite3 для хранения данных о пользователе. Библиотека не добавлена на GIT, так как там уже
есть данные пользователей. Все данные хранятся по unique_id пользователя Telegram, дабы не было возможным создать много профилей.



!! Так как файла с базой данных нет, следует закомментировать строчки взаимодействия с базой данных, чтобы бот не выдал ошибку, 
после создание первого профиля можно раскоментировать строчки



---Описание функций:
::start() - функция для запуска бота.

::menu() - функция, которая возвращает кнопки меню, благодаря готорый пользователь взаимодействует с ботом.

::registration() - функция для регистрации профиля в Боте, все последующие функции команды "/reg" созданы для 
заполнения таблицы sqlite3/users.

::new_user_login() - функция для обновления login'а пользователя через функцию edit_profile(). 

::new_user_password() - функция аналогична предыдущей, только смена пароля.

::help_message() - функция, которая выводит возможности бота.

::get_text_messages() - функция с реакцией бота на message.text (без комманд)

::edit_profile() - функция с редактированием профиля, вызывается при открытия профиля на сообщение 'Профиль'

::games() - функция с играми

::users_wish() - функция, которая отправляет admin'у бота пожелание пользователя