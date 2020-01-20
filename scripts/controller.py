import config
import model as md
import telebot
from telebot import types
from log_handler import LogHandler

logger = LogHandler()

bot = telebot.TeleBot(config.TOKEN)
model = md.Model(bot, logger)


def init_controller():
    """
    Controller initialization
    :return: None
    """
    try:
        logger.write_to_log('controller initialised', 'sys')
        bot.polling(none_stop=True)
    except Exception as err:
        logger.write_to_log('exception', 'sys')
        logger.write_to_err_log(f'exception - {err}', 'sys')


@bot.message_handler(commands=['start'])
def handle_start(message):
    """
    Method handles user start command
    :param message: message sent by user
    :return: None
    """
    try:
        logger.write_to_log('sent /start command', message.chat.id)

        msg = model.get_start_command_response(message.chat.id)
        is_registered = False if msg.split('Вітаю!').__len__() == 2 else True

        if not is_registered:
            bot.send_message(message.chat.id, msg)
            model.register_user_telegram_id(message.chat.id)

            sent_name_request = bot.send_message(message.chat.id, 'Введіть своє ім\'я')
            bot.register_next_step_handler(sent_name_request, register_user_name)
        else:
            bot.send_message(message.chat.id, msg)

        logger.write_to_log('handled /start command', message.chat.id)
    except Exception as err:
        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception - {err}', 'controller')


def register_user_name(message):
    """
    Writes user first name
    :param message: message instance
    :return: None
    """
    try:
        logger.write_to_log('entered first name', message.chat.id)
        model.register_user_first_name(message)

        sent_middle_name_request = bot.send_message(message.chat.id, 'Введіть побатькові')
        bot.register_next_step_handler(sent_middle_name_request, register_user_middle_name)

    except Exception as err:
        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception - {err}', 'controller')


def register_user_middle_name(message):
    """
    Registers user's middle name
    :param message: message instance
    :return: None
    """
    try:
        logger.write_to_log('entered middle name', message.chat.id)
        model.register_user_middle_name(message)
        sent_last_name_request = bot.send_message(message.chat.id, 'Введіть прізвище')
        bot.register_next_step_handler(sent_last_name_request, get_user_last_name)
    except Exception as err:
        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception - {err}', 'controller')


def get_user_last_name(message):
    """
    Registers users last name
    :param message: message instance
    :return: None
    """
    try:
        model.register_user_last_name(message)

        markup = types.InlineKeyboardMarkup(row_width=1)

        for x in model.get_roles_list():
            markup.add(types.InlineKeyboardButton(text=x[1], callback_data=f'role_{x[1]}'))

        bot.send_message(message.chat.id, 'Виберіть посаду', reply_markup=markup)

        logger.write_to_log('requested user\'s role', message.chat.id)
    except Exception as err:
        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """
    Method handles inline
    :param call: callback query instance
    :return: None
    """
    try:
        role = call.data.split('role_')

        if role.__len__() == 2:
            model.register_role_request(role[1], call.message.chat.id)

            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=None)

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Призначення вас на дану посаду було подано на'
                                       ' розгляд адміністратору. Після прийняття рішення, '
                                       'вас буде повідомлено')

            inline_kb = types.InlineKeyboardMarkup(row_width=1)

            for x in model.get_qualification_list():
                inline_kb.add(types.InlineKeyboardButton(text=x[1], callback_data=f'qual_{x[1]}'))

            msg = 'Оцініть свій рівень (даний пункт також потребуватиме ' \
                  'підтвердження адміністратора)'

            bot.send_message(chat_id=call.message.chat.id,
                             text=msg,
                             reply_markup=inline_kb)
        elif call.data.split('qual_').__len__() == 2:
            model.register_qualification_request(call.data.split('qual_')[1], call.message.chat.id)

            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=None)

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Дані було успішно внесено, '
                                       'після затвердження ви отримаєте сповіщення :)')
        elif call.data == 'another':
            pass
    except Exception as err:
        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception - {err}', 'controller')


    # TODO: main menu

@bot.message_handler(content_types=['text'])
def echo_msg(message):
    bot.send_message(message.chat.id, 'микола, не балуйся тут з своїми ' + message.text)
    bot.send_message(message.chat.id, 'як буде готово, я скажу')
