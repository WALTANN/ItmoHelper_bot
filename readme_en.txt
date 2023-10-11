^^ItmoHelper bot^^ is a bot parser. Thanks to the selenium library, it finds elements on the Itmo website and sends them to the user.
The sqlite3 library is also used to store user data. The library has not been added to GIT, since there is already
there is user data. All data is stored by the unique_id of the Telegram user, so that it is not possible to create many profiles.



!! Since there is no database file, you should comment out the lines of interaction with the database so that the bot does not give an error,
after creating the first profile, you can uncomment the lines



---Description of functions:
::start() - a function to start the bot.

::menu() is a function that returns menu buttons, thanks to which the user interacts with the bot.

::registration() is a function for registering a profile in the Bot, all subsequent functions of the "/reg" command are created to
fill in the sqlite3/users table.

::new_user_login() is a function for updating the user's login via the edit_profile() function.

::new_user_password() - the function is similar to the previous one, only changing the password.

::help_message() is a function that outputs the capabilities of the bot.

::get_text_messages() - function with the bot's response to message.text (without command)

::edit_profile() - a function with profile editing, called when opening a profile on the message 'Profile'

::games() - function with games

::users_wish() is a function that sends a user's wish to the admin of the bot