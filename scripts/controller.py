import config
from datetime import datetime
import model as md
import telebot
from telebot import types
from log_handler import LogHandler
import notifier as nt
from emoji import emojize
import sys


bot = telebot.TeleBot(config.TOKEN)

notifier = nt.Notifier(bot)
logger = LogHandler(notifier)
model = md.Model(bot, logger, notifier)

location_update_queue = {}
title_update_queue = {}
staff_update_queue = {}


def init_controller():
    """
    Controller initialization
    :return: None
    """
    try:
        logger.write_to_log('controller initialised', 'sys')
        bot.polling(none_stop=True)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name
        logger.write_to_log('exception', 'sys')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'sys')


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
            show_main_menu(message, edit=False)

        logger.write_to_log('handled /start command', message.chat.id)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name
        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.message_handler(commands=['menu'])
def handle_menu(message):
    show_main_menu(message=message, edit=False)


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
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


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
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


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
            markup.add(types.InlineKeyboardButton(text=x[1], callback_data=f'role_option_{x[1]}'))

        bot.send_message(message.chat.id, 'Виберіть посаду', reply_markup=markup)

        logger.write_to_log('requested user\'s role', message.chat.id)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def main_menu(call):
    """
    Callback handler for main menu
    :param call: callback query instance
    :return: None
    """
    try:
        show_main_menu(message=call.message, edit=True)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu_new')
def main_menu_without_edit(call):
    """
    Callback handler for main menu without editing
    :param call: callback instance
    :return: None
    """
    try:
        show_main_menu(message=call.message, edit=False)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=None)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call : call.data == 'confirm_requests')
def confirm_requests_handler(call):
    try:
        logger.write_to_log('requested list of pending requests', call.message.chat.id)

        qualification_requests = model.get_unaccepted_qualification_requests()
        role_requests = model.get_unaccepted_role_requests()

        inline_kb = types.InlineKeyboardMarkup(row_width=1)

        quali_req_btn = types.InlineKeyboardButton(text=f'Заявки на кваліфікацію({qualification_requests.__len__()})',
                                                   callback_data='quali_requests_approving')
        role_req_btn = types.InlineKeyboardButton(text=f'Заявки на посаду({role_requests.__len__()})',
                                                  callback_data='role_requests_approving')
        back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                  callback_data='main_menu')

        if qualification_requests.__len__() > 0 and role_requests.__len__() > 0:
            inline_kb.add(quali_req_btn, role_req_btn, back_to_main)

        elif qualification_requests.__len__() > 0 and role_requests.__len__() == 0:
            inline_kb.add(quali_req_btn, back_to_main)

        elif qualification_requests.__len__() == 0 and role_requests.__len__() > 0:
            inline_kb.add(role_req_btn, back_to_main)

        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=None)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Виберіть категорію заявок які хочете опрацювати:',
                              reply_markup=inline_kb)
        logger.write_to_log('displayed list of pending requests', call.message.chat.id)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name
        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'role_requests_approving')
def role_req_approving(call):
    """
    Callback handler for role approving query method
    :param call: callback query instance
    :return: None
    """
    try:
        logger.write_to_log('entered into role requests approving menu', call.message.chat.id)

        role_request = model.get_unaccepted_role_requests()

        req_id, staff_id, requested_role_id, date_placed, _, _, confirmed = role_request[0]

        first_n, middle_n, last_n = model.get_user_name_by_id(staff_id)

        reply = f'Заявка на підтвердження посади\n' \
                f'id заявки: {req_id}\n' \
                f'{"-" * 20}\n' \
                f'id працівника: {staff_id}\n' \
                f'ПІБ: {last_n} {first_n} {middle_n}\n' \
                f'посада вказана в заявці: {model.get_role_by_id(requested_role_id)[1]}'

        inline_kb = types.InlineKeyboardMarkup()

        accept_role = types.InlineKeyboardButton(text=f'{emojize(" :white_check_mark:", use_aliases=True)}Підтвердити',
                                                 callback_data='accept_role_request')
        decline_request = types.InlineKeyboardButton(text=f'{emojize(" :x:", use_aliases=True)}Змінити',
                                                     callback_data='decline_role_request')

        inline_kb.row(accept_role, decline_request)

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Назад до меню',
                                                 callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=reply,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'accept_role_request')
def accept_role_request(call):
    """
    Callback handler for accepting role request
    :param call: callback instance
    :return: None
    """
    try:
        id = call.message.text.split('id заявки: ')[1].split('\n')[0]
        id_user = call.message.text.split('id працівника: ')[1].split('\n')[0]

        model.accept_role_request(id, call.message.chat.id, id_user)

        msg = f'Заявку {id} було успішно підтверджено!{emojize(" :tada:", use_aliases=True)}'

        role_requests = model.get_unaccepted_role_requests()

        inline_kb = types.InlineKeyboardMarkup(row_width=1)
        back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}До меню', callback_data='main_menu')

        if len(role_requests) > 0:
            next_role = types.InlineKeyboardButton(text=f'{emojize(" :arrow_forward:", use_aliases=True)}Наступна заявка', callback_data='role_requests_approving')
            inline_kb.add(next_role, back_to_main)
        else:
            inline_kb.add(back_to_main)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'decline_role_request')
def decline_role_request_handler(call):
    """
    Method shows user options to change requested role to some another
    :param call: callback instance
    :return: None
    """
    try:
        logger.write_to_log('entered into role requests changing menu', call.message.chat.id)

        role_request = model.get_unaccepted_role_requests()

        req_id, staff_id, requested_role_id, date_placed, _, _, confirmed = role_request[0]

        first_n, middle_n, last_n = model.get_user_name_by_id(staff_id)

        reply = f'Заявка на підтвердження посади\n' \
                f'id заявки: {req_id}\n' \
                f'{"-" * 20}\n' \
                f'id працівника: {staff_id}\n' \
                f'ПІБ: {last_n} {first_n} {middle_n}\n' \
                f'посада вказана в заявці: {model.get_role_by_id(requested_role_id)[1]}\n' \
                f'{"-" * 20}\n' \
                f'Виберіть посаду, яку необіхдно призначити даному працівнику:'

        inline_kb = types.InlineKeyboardMarkup()

        for x in model.get_roles_list():
            inline_kb.add(types.InlineKeyboardButton(text=x[1], callback_data=f'change_request_role_option_{x[1]}'))

        inline_kb.add(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Назад до меню',
                                                 callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=reply,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('change_request_').__len__() == 2)
def change_request_option_handler(call):
    """
    Callback handler for changing requests details
    :param call: callback instance
    :return: None
    """
    try:
        type_of_request = call.data.split('change_request_')[1].split('_')[0]
        request_id = call.message.text.split('id заявки: ')[1].split('\n')[0]
        staff_id = call.message.text.split('id працівника: ')[1].split('\n')[0]
        changed_parameter = call.data.split('_')[-1]

        logger.write_to_log(f'started approving request {request_id}', staff_id)

        if type_of_request == 'role':
            roles = model.get_roles_list()
            role_id = 0
            for r in roles:
                if r[1] == changed_parameter:
                    role_id = r[0]
                    break

            model.change_role_request(request_id, role_id, call.message.chat.id, staff_id)

            msg = f'Заявку {request_id} було успішно підтверджено!{emojize(" :tada:", use_aliases=True)}'

            role_requests = model.get_unaccepted_role_requests()

            inline_kb = types.InlineKeyboardMarkup(row_width=1)
            back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}До меню',
                                                      callback_data='main_menu')

            if len(role_requests) > 0:
                next_role = types.InlineKeyboardButton(
                    text=f'{emojize(" :arrow_forward:", use_aliases=True)}Наступна заявка',
                    callback_data='role_requests_approving')
                inline_kb.add(next_role, back_to_main)
            else:
                inline_kb.add(back_to_main)

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=msg,
                                  reply_markup=inline_kb)
        else:  # qual
            quals = model.get_qualification_list()
            qual_id = 0
            for r in quals:
                if r[1] == changed_parameter:
                    qual_id = r[0]
                    break

            model.change_qualification_request(request_id, qual_id, call.message.chat.id, staff_id)
            msg = f'Заявку {request_id} було успішно підтверджено!{emojize(" :tada:", use_aliases=True)}'

            qual_requests = model.get_unaccepted_qualification_requests()

            inline_kb = types.InlineKeyboardMarkup(row_width=1)
            back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}До меню',
                                                      callback_data='main_menu')

            if len(qual_requests) > 0:
                next_role = types.InlineKeyboardButton(
                    text=f'{emojize(" :arrow_forward:", use_aliases=True)}Наступна заявка',
                    callback_data='quali_requests_approving')
                inline_kb.add(next_role, back_to_main)
            else:
                inline_kb.add(back_to_main)

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=msg,
                                  reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'quali_requests_approving')
def quali_requests_approving_handler(call):
    try:
        logger.write_to_log('entered into qualification requests approving menu', call.message.chat.id)
        qualification_requests = model.get_unaccepted_qualification_requests()

        req_id, staff_id, requested_q_id, date_placed, _, _, confirmed = qualification_requests[0]
        first_n, middle_n, last_n = model.get_user_name_by_id(staff_id)

        reply = f'Заявка на підтвердження кваліфікації\n' \
                f'id заявки: {req_id}\n' \
                f'{"-" * 20}\n' \
                f'id працівника: {staff_id}\n' \
                f'ПІБ: {last_n} {first_n} {middle_n}\n' \
                f'кваліфікація вказана в заявці: {model.get_qualification_by_id(requested_q_id)[1]}'

        inline_kb = types.InlineKeyboardMarkup()

        accept_role = types.InlineKeyboardButton(text=f'{emojize(" :white_check_mark:", use_aliases=True)}Підтвердити',
                                                 callback_data='accept_qualification_request')
        decline_request = types.InlineKeyboardButton(text=f'{emojize(" :x:", use_aliases=True)}Змінити',
                                                         callback_data='decline_qualification_request')

        inline_kb.row(accept_role, decline_request)

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Назад до меню',
                                                 callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=reply,
                              reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'accept_qualification_request')
def accept_qualification_request_handler(call):
    try:
        id = call.message.text.split('id заявки: ')[1].split('\n')[0]
        id_user = call.message.text.split('id працівника: ')[1].split('\n')[0]

        model.accept_qualification_request(id, call.message.chat.id, id_user)
        msg = f'Заявку {id} було успішно підтверджено!{emojize(" :tada:", use_aliases=True)}'

        qual_requests = model.get_unaccepted_qualification_requests()

        inline_kb = types.InlineKeyboardMarkup(row_width=1)
        back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}До меню',
                                                  callback_data='main_menu')

        if len(qual_requests) > 0:
            next_role = types.InlineKeyboardButton(
                text=f'{emojize(" :arrow_forward:", use_aliases=True)}Наступна заявка',
                callback_data='quali_requests_approving')
            inline_kb.add(next_role, back_to_main)
        else:
            inline_kb.add(back_to_main)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'decline_qualification_request')
def decline_qualification_request_handler(call):
    try:
        logger.write_to_log('entered into qualification requests changing menu', call.message.chat.id)

        qual_request = model.get_unaccepted_qualification_requests()[0]

        req_id, staff_id, requested_qualification_id, date_placed, _, _, confirmed = qual_request
        first_n, middle_n, last_n = model.get_user_name_by_id(staff_id)

        reply = f'Заявка на підтвердження кваліфікації\n' \
                f'id заявки: {req_id}\n' \
                f'{"-" * 20}\n' \
                f'id працівника: {staff_id}\n' \
                f'ПІБ: {last_n} {first_n} {middle_n}\n' \
                f'кваліфікація вказана в заявці: {model.get_qualification_by_id(requested_qualification_id)[1]}\n' \
                f'{"-" * 20}\n' \
                f'Виберіть кваліфікацію, яку необіхдно призначити даному працівнику:'

        inline_kb = types.InlineKeyboardMarkup()
        for x in model.get_qualification_list():
            inline_kb.add(types.InlineKeyboardButton(text=x[1], callback_data=f'change_request_qual_option_{x[1]}'))

        inline_kb.add(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Назад до меню',
                                                 callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=reply,
                              reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('_option_').__len__() == 2)
def callback_handler(call):
    """
    Method handles inline
    :param call: callback query instance
    :return: None
    """
    try:
        role = call.data.split('role_option_')

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
                inline_kb.add(types.InlineKeyboardButton(text=x[1], callback_data=f'qual_option_{x[1]}'))

            msg = 'Оцініть свій рівень (даний пункт також потребуватиме ' \
                  'підтвердження адміністратора)'

            bot.send_message(chat_id=call.message.chat.id,
                             text=msg,
                             reply_markup=inline_kb)

        elif call.data.split('qual_option_').__len__() == 2:
            model.register_qualification_request(call.data.split('qual_option_')[1], call.message.chat.id)

            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=None)

            inline_kb = types.InlineKeyboardMarkup(row_width=1)

            inline_kb.add(types.InlineKeyboardButton('Перейти до головного меню', callback_data='main_menu_new'))

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Дані було успішно внесено, '
                                       'після затвердження ви отримаєте сповіщення :)',
                                  reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'adm_stats')
def adm_stats_handler(call):
    """
    Displays admin statistics menu
    :param call: callback instance
    :return:None
    """
    try:
        msg = f'Виберіть необхідний параметр:'

        inline_kb = types.InlineKeyboardMarkup()

        # TODO: add admin statistics

        num_of_users = types.InlineKeyboardButton(text=f'{emojize(" :busts_in_silhouette:", use_aliases=True)}Кількість користувачів', callback_data='adm_stat_users_count')
        db_session_duration = types.InlineKeyboardButton(text=f'{emojize(" :hourglass_flowing_sand:", use_aliases=True)}Тривалість сесії', callback_data='adm_stat_session_duration')
        inline_kb.row(num_of_users, db_session_duration)

        back_to_menu = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                  callback_data='main_menu')
        inline_kb.row(back_to_menu)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'adm_stat_users_count')
def adm_stat_users_count_handler(call):
    """
    Users count statistics menu handler
    :param call: callback instance
    :return: None
    """
    try:
        msg = f'Кількість користувачів зареєстрованих в системі:\n' \
              f'{"-" * 20}\n' \
              f'{model.get_users_count()}\n' \
              f'{"-" * 20}'

        inline_kb = types.InlineKeyboardMarkup()

        back_to_menu = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                  callback_data='main_menu')
        inline_kb.row(back_to_menu)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'adm_stat_session_duration')
def adm_stat_session_duration_handler(call):
    try:
        session_duration = model.get_db_session_duration()

        msg = f'Тривалість поточної сесеї з базою даних:\n' \
              f'{"-" * 20}\n' \
              f'секунд - {session_duration}\n' \
              f'хвилин - {session_duration / 60}\n' \
              f'годин - {session_duration / 3600}\n' \
              f'{"-" * 20}'

        inline_kb = types.InlineKeyboardMarkup()

        back_to_menu = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                  callback_data='main_menu')
        inline_kb.row(back_to_menu)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'confirm_event_requests')
def confirm_event_requests_handler(call):
    """
    Handles command sent to accept event request
    :param call: callback instance
    :return: None
    """
    try:
        #
        # TODO: client bot must guarantee next values to be entered: date starts, date ends and number of guests
        #
        request_id, event_id, client_id, title, location, date_starts, date_ends, guests, type_of_event_id, class_of_event_id, _ = model.get_event_request_extended_info()
        _, client_username, f_name, l_name, company, phone, email = model.get_client_by_id(client_id)
        inline_kb = types.InlineKeyboardMarkup()

        class_of_event = None
        type_of_event = None

        if type_of_event_id is not None:
            _, type_of_event = model.get_type_of_event_by_id(type_of_event_id)
        if class_of_event_id is not None:
            _, class_of_event, _ = model.get_class_of_event_by_id(class_of_event_id)

        msg = get_extended_event_info_message((request_id, event_id, client_id, title, location, date_starts, date_ends,
                                               guests, type_of_event_id, class_of_event_id, type_of_event,
                                               class_of_event, client_username, f_name, l_name, company, phone, email),
                                              type_of_action='Заявка на проведення події')

        if title is None or title == '':
            inline_kb.row(types.InlineKeyboardButton(text='Внести назву події', callback_data=f'edit_event_id:{event_id}_title'))
        if location is None or location == '':
            inline_kb.row(types.InlineKeyboardButton(text='Внести локацію події', callback_data=f'edit_event_id:{event_id}_location'))
        if type_of_event is None or type_of_event == '':
            inline_kb.row(types.InlineKeyboardButton(text='Внести тип події', callback_data=f'edit_event_id:{event_id}_type'))
        if class_of_event is None or type_of_event == '':
            inline_kb.row(types.InlineKeyboardButton(text='Внести клас події', callback_data=f'edit_event_id:{event_id}_class'))

        if (title is not None and title != '') and (location is not None and location != '') and (type_of_event_id is not None and type_of_event_id != '') and (class_of_event_id is not None and class_of_event_id != ''):
            inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :moneybag:", use_aliases=True)}Розрахувати ціну', callback_data='calculate_event_price'))

        decline_event_request = types.InlineKeyboardButton(text=f'{emojize(" :x:", use_aliases=True)}Відхилити заявку', callback_data=f'decline_event_request_id:{event_id}')

        back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                callback_data='main_menu')

        inline_kb.row(decline_event_request)
        inline_kb.row(back_to_main)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('decline_event_request_id:').__len__() > 1)
def decline_event_request_id_handler(call):
    try:
        event_id = call.data.split('decline_event_request_id:')[1]
        model.decline_event_request(event_id, call.message.chat.id)

        msg = f'Заявку було відхилено!'
        inline_kb = types.InlineKeyboardMarkup()
        inline_kb.add(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('update_event_type_id:').__len__() > 1)
def get_event_type(call):
    try:
        id = call.data.split('update_event_type_id:')[1].split('_')[0]
        type_id = call.data.split('update_event_type_id:')[1].split('_set:')[1]

        model.update_event_type(id, type_id)

        msg = f'{emojize(" :tada:", use_aliases=True)} Тип події оновлено!'
        inline_kb = types.InlineKeyboardMarkup()

        if not model.is_event_processed(id):
            inline_kb.row(
                types.InlineKeyboardButton(text='До меню редагування події', callback_data='confirm_event_requests'))
        else:
            inline_kb.row(
                types.InlineKeyboardButton(text='До меню редагування події', callback_data='edit_event_details')
            )

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('update_event_class_id:').__len__() > 1)
def get_event_type(call):
    try:
        id = call.data.split('update_event_class_id:')[1].split('_')[0]
        class_id = call.data.split('update_event_class_id:')[1].split('_set:')[1]

        model.update_event_class(id, class_id)

        msg = f'{emojize(" :tada:", use_aliases=True)} Клас події оновлено!'
        inline_kb = types.InlineKeyboardMarkup()

        if not model.is_event_processed(id):
            inline_kb.row(
                types.InlineKeyboardButton(text='До меню редагування події', callback_data='confirm_event_requests'))
        else:
            inline_kb.row(
                types.InlineKeyboardButton(text='До меню редагування події', callback_data='edit_event_details')
            )

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('edit_event_id:').__len__() > 1)
def edit_event_handler(call):
    try:
        id = call.data.split('edit_event_id:')[1].split('_')[0]
        parameter = call.data.split('edit_event_id:')[1].split('_')[1]

        if parameter == 'title':
            msg = 'Відправте назву події:'

            title_request_sent = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=call.message.message_id,
                                                       text=msg,
                                                       reply_markup=None)

            title_update_queue[call.message.chat.id] = id

            bot.register_next_step_handler(title_request_sent, get_event_title)
        elif parameter == 'location':
            msg = f'Відправте боту локацію на якій проходитиме святкування події (використовуйте тільки вбудовані засоби Telegram):'
            location_request_sent = bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,text=msg,
                                          reply_markup=None)
            location_update_queue[call.message.chat.id] = id

            bot.register_next_step_handler(location_request_sent, get_event_location)
        elif parameter == 'type':
            msg = 'Виберіть тип події:'
            inline_kb = types.InlineKeyboardMarkup()

            for event_id, event_type in model.get_event_types_list():
                inline_kb.add(types.InlineKeyboardButton(text=event_type,
                                                         callback_data=f'update_event_type_id:{id}_set:{event_id}'))

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=msg,
                                  reply_markup=inline_kb)
        elif parameter == 'class':
            msg = 'Виберіть клас події:'
            inline_kb = types.InlineKeyboardMarkup()

            for event_id, event_class, _ in model.get_event_classes_list():
                inline_kb.add(types.InlineKeyboardButton(text=event_class,
                                                         callback_data=f'update_event_class_id:{id}_set:{event_id}'))

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=msg,
                                  reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'calculate_event_price')
def calculate_event_price_handler(call):
    """
    Handles event price calculation request
    :param call: callback instance
    :return: None
    """
    try:
        event_id = call.message.text.split('id події:')[1].split('\n')[0]

        price, professional_staff, middle_staff, new_staff = model.calculate_event_price_and_parameters(event_id)
        new_line = '\n'
        msg = f'Ціна та параметри обслуговування події id:{event_id}:\n' \
              f'{"-" * 20}\n' \
              f'Загальна кількість офіціантів: {professional_staff + middle_staff + new_staff}\n' \
              f'{emojize(" :full_moon:", use_aliases=True) + "Професійних офіціантів: " + str(professional_staff) + new_line if professional_staff > 0 else ""}' \
              f'{emojize(" :last_quarter_moon:", use_aliases=True) + "Офіціантів середнього рівня: " + str(middle_staff) + new_line if middle_staff > 0 else ""}' \
              f'{emojize(" :new_moon:", use_aliases=True) + "Офіціантів початківців: " + str(new_staff) + new_line if new_staff > 0 else ""}' \
              f'{"-" * 20}\n' \
              f'{emojize(" :moneybag:", use_aliases=True)}Ціна обслуговування події: *{round(price, 3)}грн.*'

        inline_kb = types.InlineKeyboardMarkup()
        approve_price = types.InlineKeyboardButton(text=f'{emojize(" :white_check_mark:", use_aliases=True)}Підтвердити ціну',
                                                   callback_data='approve_event_price')
        back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                  callback_data='main_menu')
        inline_kb.row(approve_price)
        # inline_kb.row(back_to_main)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              parse_mode='Markdown',
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'approve_event_price')
def approve_event_price_handler(call):
    try:
        event_id = call.message.text.split('id:')[1].split('\n')[0].replace(':', '')
        pro_staff = call.message.text.split('Професійних офіціантів: ')[1].split('\n')[0] if call.message.text.split('Професійних офіціантів: ').__len__() > 1 else 0
        mid_staff = call.message.text.split('Офіціантів середнього рівня: ')[1].split('\n')[0] if call.message.text.split('Офіціантів середнього рівня: ').__len__() > 1 else 0
        beginner_staff = call.message.text.split('Офіціантів початківців: ')[1].split('\n')[0] if call.message.text.split('Офіціантів початківців: ').__len__() > 1 else 0
        price = call.message.text.split('💰Ціна обслуговування події: ')[1].split('грн')[0]

        model.accept_event_price(event_id, price, pro_staff, mid_staff, beginner_staff, call.message.chat.id, 'uah')

        msg = f'{emojize(" :tada:", use_aliases=True)}Дані про подію було внесено. Клієнта буде сповіщено про зміну ціни'
        inline_kb = types.InlineKeyboardMarkup()

        inline_kb.add(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                  callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'edit_event_details')
def edit_event_details_handler(call):
    """
    Creates menu which displays all upcoming events, which can be edited
    :param call: callback instance
    :return: None
    """
    try:
        events = model.get_upcoming_events()

        msg = 'Виберіть подію, яку необхідно редагувати:(якщо вам необхідно ' \
              'повернутися до головного меню, все одно зайдіть в будь-яку подію, ' \
              'та  натисніть на \'перерахувати ціну\')'
        inline_kb = types.InlineKeyboardMarkup()

        for event_id, req_id, title, _, date_starts, _, _, _, _, _, _, _, _ in events:
            _, _, fn, ln, _, _, _ = model.get_client_by_event_request_id(req_id)
            inline_kb.add(types.InlineKeyboardButton(text=f'{title} {fn} {ln} {date_starts.date()}', callback_data=f'modify_event_id:{event_id}'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('modify_event_id:').__len__() > 1)
def modify_event_id_handler(call):
    """
    Modifies event data and recalculating its price
    :param call:
    :return:
    """
    try:
        event_id = call.data.split('modify_event_id:')[1]

        request_id, event_id, client_id, title, location, date_starts, date_ends, guests, type_of_event_id, class_of_event_id, _ = model.get_event_request_extended_info_by_id(event_id)
        _, client_username, f_name, l_name, company, phone, email = model.get_client_by_id(client_id)

        class_of_event = None
        type_of_event = None

        if type_of_event_id is not None:
            _, type_of_event = model.get_type_of_event_by_id(type_of_event_id)
        if class_of_event_id is not None:
            _, class_of_event, _ = model.get_class_of_event_by_id(class_of_event_id)

        msg = get_extended_event_info_message((request_id, event_id, client_id, title, location, date_starts, date_ends,
                                               guests, type_of_event_id, class_of_event_id, type_of_event,
                                               class_of_event, client_username, f_name, l_name, company, phone, email),
                                              type_of_action='Зміна пареметрів події')

        inline_kb = types.InlineKeyboardMarkup()

        inline_kb.row(types.InlineKeyboardButton(text='Внести назву події', callback_data=f'edit_event_id:{event_id}_title'))
        inline_kb.row(types.InlineKeyboardButton(text='Внести локацію події', callback_data=f'edit_event_id:{event_id}_location'))
        inline_kb.row(types.InlineKeyboardButton(text='Внести тип події', callback_data=f'edit_event_id:{event_id}_type'))
        inline_kb.row(types.InlineKeyboardButton(text='Внести клас події', callback_data=f'edit_event_id:{event_id}_class'))
        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :moneybag:", use_aliases=True)}Перерахувати вартість події',
                                                  callback_data='calculate_event_price'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'set_main_on_shift')
def set_main_on_shift_handler(call):
    """
    Checks if there's shifts without supervisor and shows list of em
    :param call:
    :return:
    """
    try:
        shifts = model.get_upcoming_shifts()
        shifts_without_supervisor = []

        for shift in shifts:
            if shift[5] is None or shift[5] == '':
                shifts_without_supervisor.append(shift)

        msg = 'Виберіть зміну для призначення головного:'
        inline_kb = types.InlineKeyboardMarkup()

        for shift in shifts_without_supervisor:
            _, _, _, title, _, date_starts, _, guests, _, _, staff = model.get_event_request_extended_info_by_id(shift[1])
            inline_kb.add(types.InlineKeyboardButton(text=f'{title} {date_starts} {staff}', callback_data=f'set_supervisor_to_shift_id:{shift[0]}'))

        back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                  callback_data='main_menu')

        inline_kb.add(back_to_main)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func= lambda call: call.data.split('set_supervisor_to_shift_id:').__len__() > 1)
def set_supervisor_to_shift_id_handler(call):
    try:
        shift_id = call.data.split('set_supervisor_to_shift_id:')[1]

        _, event_id, pro, mid, beg, supervisor_id, title, location, date_starts, date_ends, guests, type_id, class_id, staff, price, currency_id = model.get_shift_extended_info_by_id(shift_id)
        registered_to_shift = model.get_registered_to_shift_staff(shift_id)

        msg = ''
        inline_kb = types.InlineKeyboardMarkup()

        if len(registered_to_shift) == 0:
            msg = 'На дану зміну ще не зареєстровано жодного працівника. Повторіть спробу пізніше'
        else:
            msg = f'{emojize(" :white_check_mark:", use_aliases=True) if len(registered_to_shift) == staff else emojize(" :negative_squared_cross_mark:", use_aliases=True)}Зареєстровано {len(registered_to_shift)}/{staff}\n' \
                  f'Виберіть працівника з списку зареєстрованих на зміну:\n' \
                  f'{"-" * 20}\n' \
                  f'Прізвище, ім\'я, кваліфікація, рейтинг, відпрацьовано подій'
            for registration in registered_to_shift:
                staff_id, fn, _, ln, _, qualification_id, cur_rat, _, _, events_done, _ = model.get_staff_by_id(registration[2])
                _, qualification_name = model.get_qualification_by_id(qualification_id)
                inline_kb.row(types.InlineKeyboardButton(text=f'{ln} {fn} {qualification_name} {cur_rat} {events_done}', callback_data=f'set_supervisor_staff:{staff_id}_shift:{shift_id}'))

        back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                  callback_data='main_menu')
        inline_kb.row(back_to_main)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('set_supervisor_staff:').__len__() > 1)
def set_supervisor_staff_handler(call):
    try:
        staff_id = call.data.split('staff:')[1].split('_')[0]
        shift_id = call.data.split('shift:')[1]

        model.update_shift_supervisor(shift_id, staff_id)

        msg = f'{emojize(":tada:", use_aliases=True)}Головного на зміні успішно призначено!'
        inline_kb = types.InlineKeyboardMarkup()

        inline_kb.add(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                  callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'change_main_on_shift')
def change_main_on_shift_handler(call):
    """
    Handles 'change supervisor' button click
    :param call: callback instance
    :return: None
    """
    try:
        shifts = model.get_upcoming_shifts()
        shifts_with_supervisor = []

        for shift in shifts:
            if shift[5] is not None:
                shifts_with_supervisor.append(shift)

        msg = 'Виберіть зміну для зміни головного:'
        inline_kb = types.InlineKeyboardMarkup()

        for shift in shifts_with_supervisor:
            _, _, _, title, _, date_starts, _, guests, _, _, staff = model.get_event_request_extended_info_by_id(shift[1])
            inline_kb.add(types.InlineKeyboardButton(text=f'{title} {date_starts} {staff}', callback_data=f'change_supervisor_at_shift_id:{shift[0]}'))

        back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                  callback_data='main_menu')

        inline_kb.add(back_to_main)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('change_supervisor_at_shift_id:').__len__() > 1)
def change_supervisor_at_shift_id_handler(call):
    """
    Displays all registered for shift staff
    :param call: callback instance
    :return: None
    """
    try:
        shift_id = call.data.split('change_supervisor_at_shift_id:')[1]

        _, event_id, pro, mid, beg, supervisor_id, title, location, date_starts, date_ends, guests, type_id, class_id, staff, price, currency_id = model.get_shift_extended_info_by_id(
            shift_id)
        registered_to_shift = model.get_registered_to_shift_staff(shift_id)

        msg = ''
        inline_kb = types.InlineKeyboardMarkup()

        msg = f'{emojize(" :white_check_mark:", use_aliases=True) if len(registered_to_shift) == staff else emojize(" :negative_squared_cross_mark:", use_aliases=True)}Зареєстровано {len(registered_to_shift)}/{staff}\n' \
              f'Виберіть працівника з списку зареєстрованих на зміну:\n' \
              f'{"-" * 20}\n' \
              f'Прізвище, ім\'я, кваліфікація, рейтинг, відпрацьовано подій'

        for registration in registered_to_shift:
            staff_id, fn, _, ln, _, qualification_id, cur_rat, _, _, events_done, _ = model.get_staff_by_id(
                registration[2])
            _, qualification_name = model.get_qualification_by_id(qualification_id)
            if staff_id == supervisor_id:
                inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :cop:", use_aliases=True)}{ln} {fn} {qualification_name} {cur_rat} {events_done}',
                                                     callback_data=f'set_supervisor_staff:{staff_id}_shift:{shift_id}'))
            else:
                inline_kb.row(types.InlineKeyboardButton(
                    text=f'{ln} {fn} {qualification_name} {cur_rat} {events_done}',
                    callback_data=f'set_supervisor_staff:{staff_id}_shift:{shift_id}'))

        back_to_main = types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                      callback_data='main_menu')
        inline_kb.row(back_to_main)
        bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=msg,
                                  reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'get_available_shifts')
def get_available_shifts_handler(call):
    """
    Handles button click with available shifts request
    :param call:callback instance
    :return: None
    """
    try:
        staff_info = model.get_staff_by_id(call.message.chat.id)
        shifts = model.get_available_shift_for_staff(call.message.chat.id, staff_info[5])

        msg = ''
        inline_kb = types.InlineKeyboardMarkup()

        if len(shifts) > 0:
            msg = f'Виберіть зміну, для перегляду більш детальної інформації:'

            for shift in shifts:
                event_data = model.get_event_request_extended_info_by_id(shift[1])
                _, type_name = model.get_type_of_event_by_id(event_data[8])
                shift_desc = f'{event_data[3]} {event_data[5]} {type_name}'

                inline_kb.row(types.InlineKeyboardButton(text=shift_desc, callback_data=f'show_shift_info_id:{shift[0]}'))

        else:
            msg=f'Нажаль, більше немає доступних змін для вас{emojize(" :pensive:", use_aliases=True)}'

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                      callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('show_shift_info_id:').__len__() > 1)
def show_shift_info_id_handler(call):
    """
    Shows shift information to staff
    :param call: callback instance
    :return: None
    """
    try:
        shift_id = call.data.split('show_shift_info_id:')[1]
        shift_id, event_id, pros, mids, begs, sup_id, title, loc, starts, ends, guests, type_id, class_id, staff, price, currency = model.get_shift_extended_info_by_id(shift_id)
        _, type_name = [x for x in model.get_event_types_list() if x[0] == type_id][0]
        _, class_name, _ = [x for x in model.get_event_classes_list() if x[0] == class_id][0]

        staff_info = model.get_staff_by_id(call.message.chat.id)
        shifts = [x for x in model.get_available_shift_for_staff(call.message.chat.id, staff_info[5]) if x[0] != shift_id]

        msg = f'{emojize(" :dizzy:", use_aliases=True)}Назва події:{title}\n' \
              f'{"-" * 20}\n' \
              f'{emojize(" :clock4:", use_aliases=True)}Початок: {starts}\n' \
              f'{emojize(" :clock430:", use_aliases=True)}Кінець: {ends}\n' \
              f'{emojize(" :hourglass:", use_aliases=True)}Час на зміні: {ends - starts}\n' \
              f'{emojize(" :busts_in_silhouette:", use_aliases=True)}Кількість гостей: {guests}\n' \
              f'{emojize(" :fireworks:", use_aliases=True)}Тип події: {type_name}\n' \
              f'{emojize(" :star:", use_aliases=True)}Клас події: {class_name}\n'
        inline_kb = types.InlineKeyboardMarkup()

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :triangular_flag_on_post:", use_aliases=True)}Переглянути локацію', callback_data=f'check_location_evid:{event_id}_shid:{shift_id}'))

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :heavy_plus_sign:", use_aliases=True)}Зареєструватись на зміну', callback_data=f'register_to_shift_id:{shift_id}'))

        if shifts.__len__() > 0:
            inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :arrow_forward:", use_aliases=True)}Наступна зміна', callback_data=f'show_shift_info_id:{shifts[0][0]}'))

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                 callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('check_location_evid:').__len__() > 1)
def check_location_handler(call):
    """
    Sends event location to staff, deletes shift message and sends new main menu message
    :param call: callback instance
    :return: None
    """
    try:
        event_id = call.data.split('check_location_evid:')[1].split('_')[0]
        shift_id = call.data.split('shid:')[1]

        location = model.get_event_request_extended_info_by_id(event_id)[4]

        latitude = location.split(':')[1].split(' ')[0]
        longitude = location.split(':')[2]

        inline_kb = types.InlineKeyboardMarkup()

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                 callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                             message_id=call.message.message_id,
                             text='Подія відбуватиметься на наступній локації:',
                             reply_markup=None)

        bot.send_location(chat_id=call.message.chat.id,
                          latitude=latitude,
                          longitude=longitude)

        show_main_menu(call.message, edit=False)


    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('register_to_shift_id').__len__() > 1)
def register_to_shift_id_handler(call):
    try:
        shift_id = call.data.split('register_to_shift_id:')[1]

        msg = f''
        inline_kb = types.InlineKeyboardMarkup()

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                 callback_data='main_menu'))

        if model.register_for_shift(shift_id, call.message.chat.id):
            msg = f'{emojize(":tada:", use_aliases=True)}Вас успішно зареєстровано на зміну!'
        else:
            msg = f'{emojize(" :disappointed:", use_aliases=True)}Вас не було зареєстровано на зміну, оскільки ви зареєстровані на інші зміни, які конфліктують.' \
                  f' Інтервал між змінами повинен бути {config.HOURS_BETWEEN_SHIFTS} годин'

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data == 'check_staff_registered_shifts')
def check_staff_registered_shifts_handler(call):
    """
    Handles 'watch registered shifts' menu item click
    :param call: callback instance
    :return: None
    """
    try:
        shifts = model.get_staff_registered_shifts(call.message.chat.id)

        msg = 'Виберіть зміну з списку:'
        inline_kb = types.InlineKeyboardMarkup()

        if len(shifts) > 0:
            for shift in shifts:
                inline_kb.row(types.InlineKeyboardButton(text=f'{shift[1]} {shift[2]}',
                              callback_data=f'get_info_about_shift_registration:{shift[0]}_staff:{call.message.chat.id}'))
        else:
            msg = 'На жаль наразі немає змін, на які ви були зареєстровані :('

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                 callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)

    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('get_info_about_shift_registration:').__len__() > 1)
def get_info_about_shift_registration_handler(call):
    try:
        shift_registration_id = call.data.split('get_info_about_shift_registration:')[1].split('_')[0]
        staff_id = call.data.split('_staff:')[1]

        msg = ''
        inline_kb = types.InlineKeyboardMarkup()

        _, title, date_starts, date_ends, date_registered, check_in, check_out, rating, payment  = model.get_staff_registered_shift_details(shift_registration_id, staff_id)

        msg = f'{title}\n' \
              f'{"-" * 20}\n' \
              f'{emojize(" :clock4:", use_aliases=True)}Дата початку: {date_starts}\n' \
              f'{emojize(" :clock430:", use_aliases=True)}Дата закінчення: {date_ends}\n'\
              f'{emojize(" :pencil:", use_aliases=True)}Дата реєстрації: {date_registered}\n'\
              f'{emojize(" :heavy_plus_sign:", use_aliases=True)}check-in: {check_in if check_in is not None and check_in !="" else "Інформація тимчасово відсутня"}\n'\
              f'{emojize(" :heavy_minus_sign:", use_aliases=True)}check-out: {check_out if check_out is not None and check_out !="" else "Інформація тимчасово відсутня"}\n'\
              f'{emojize(" :chart_with_upwards_trend:", use_aliases=True)}Рейтинг: {rating if rating is not None and rating !="" else "Інформація тимчасово відсутня"}\n'\
              f'{emojize(" :moneybag:", use_aliases=True)}Заробітна плата: {payment if payment is not None and payment !="" else "Інформація тимчасово відсутня"}\n'

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :x:", use_aliases=True)}Скасувати реєстрацію на зміну',
                                                 callback_data=f'ask_about_cancel_shift_registration:{shift_registration_id}_staff:{staff_id}'))
        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                 callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('ask_about_cancel_shift_registration:').__len__() > 1)
def cancel_shift_registration_handler(call):
    try:
        shift_registration_id = call.data.split('ask_about_cancel_shift_registration:')[1].split('_')[0]
        staff_id = call.data.split('_staff:')[1]

        _, title, date_starts, date_ends, date_registered, check_in, check_out, rating, payment = model.get_staff_registered_shift_details(shift_registration_id, staff_id)

        msg = f'{emojize(" :interrobang:", use_aliases=True)}Ви впевнені, що хочете скасувати свою реєстрацію на зміну * {title} {date_starts} *?'
        inline_kb = types.InlineKeyboardMarkup()

        inline_kb.row(types.InlineKeyboardButton(text=f'Так', callback_data=f'cancel_shift_reg_id:{shift_registration_id}_staff:{staff_id}_yes'),
                      types.InlineKeyboardButton(text=f'Ні', callback_data=f'cancel_shift_reg_id:{shift_registration_id}_staff:{staff_id}_no'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              parse_mode='Markdown',
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('cancel_shift_reg_id:').__len__() > 1)
def cancel_shift_reg_id_handler(call):
    try:
        shift_registration_id = call.data.split('cancel_shift_reg_id:')[1].split('_')[0]
        staff_id = call.data.split('_staff:')[1].split('_')[0]
        answer = True if call.data.split('_staff:')[1].split('_')[1] == 'yes' else False

        msg = ''
        inline_kb = types.InlineKeyboardMarkup()

        if answer:
            model.cancel_shift_registration(shift_registration_id, staff_id)
            msg = f'{emojize(":tada:",use_aliases=True)}Вашу реєстрацію на зміну було знято!'
        else:
            msg = f'Ви залишились зареєстровані на зміну!'

        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :back:", use_aliases=True)}Повернутись до меню',
                                                 callback_data='main_menu'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              parse_mode='Markdown',
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')



def check_shifts_with_supervisor(shifts):
    """
    Counts number of shifts with supervisors and without em
    :param shifts: list of upcoming shifth
    :return: number of shifth with and without supervisor
    """
    try:
        with_super = 0
        without_super = 0

        for _,_,_,_,_,sup in shifts:
            if sup is not None and sup != '':
                with_super += 1
            if sup is None or sup == '':
                without_super +=1

        return with_super, without_super
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


def get_event_title(message):
    try:
        event_id = title_update_queue.pop(message.chat.id)

        if message.text is not None:
            model.update_event_title(event_id, message.text)
            msg = f'{emojize(" :tada:", use_aliases=True)} Назва події оновлена!'
            inline_kb = types.InlineKeyboardMarkup()

            if not model.is_event_processed(event_id):
                inline_kb.row(
                    types.InlineKeyboardButton(text='До меню редагування події', callback_data='confirm_event_requests'))
            else:
                inline_kb.row(types.InlineKeyboardButton(text='До меню редагування події', callback_data='edit_event_details'))

            bot.send_message(chat_id=message.chat.id,
                             text=msg,
                             reply_markup=inline_kb)
        else:
            msg = f'{emojize(" :heavy_exclamation_mark:", use_aliases=True)} Назва події не оновлена! Допускається лише текст!'
            inline_kb = types.InlineKeyboardMarkup()

            inline_kb.row(
                types.InlineKeyboardButton(text='До меню редагування події', callback_data='confirm_event_requests'))

            bot.send_message(chat_id=message.chat.id,
                             text=msg,
                             reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


def get_event_location(message):
    try:
        event_id = location_update_queue.pop(message.chat.id)

        if message.location is not None:
            model.update_event_location(event_id, message.location.latitude, message.location.longitude)

            msg = f'{emojize(" :tada:", use_aliases=True)} Локація події оновлена!'
            inline_kb = types.InlineKeyboardMarkup()
            if not model.is_event_processed(event_id):
                inline_kb.row(types.InlineKeyboardButton(text='До меню редагування події', callback_data='confirm_event_requests'))
            else:
                inline_kb.row(types.InlineKeyboardButton(text='До меню редагування події', callback_data='edit_event_details'))

            bot.send_message(chat_id=message.chat.id,
                                  text=msg,
                                  reply_markup=inline_kb)
        else:
            msg = f'{emojize(" :heavy_exclamation_mark:", use_aliases=True)} Локація події не оновлена! Допускається лише геопозиція засобами Telegram.'
            inline_kb = types.InlineKeyboardMarkup()

            inline_kb.row(
                types.InlineKeyboardButton(text='До меню редагування події', callback_data='confirm_event_requests'))

            bot.send_message(chat_id=message.chat.id,
                             text=msg,
                             reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


def get_extended_event_info_message(params, type_of_action):
    """
    Returns string with event details, depends of type of action (accept or change)
    :param params: set of all needed details
    :param type_of_action: type of needed msg (accept of change)
    :return:
    """
    request_id, event_id, client_id, title, location, date_starts, date_ends, guests, type_of_event_id, class_of_event_id, type_of_event, class_of_event, client_username, f_name, l_name, company, phone, email = params
    new_line = '\n'

    msg = f'{emojize(" :dizzy:", use_aliases=True)}{type_of_action}\n' \
          f'{"-" * 20}\n' \
          f'{emojize(" :clipboard:", use_aliases=True)}ПІП: {l_name} {f_name}\n' \
          f'{"Telegram нік клієнта: @" + str(client_username) + new_line if client_username is not None else ""}' \
          f'{emojize(" :phone:", use_aliases=True)}Номер телефону: {phone}\n' \
          f'{emojize(" :e-mail:", use_aliases=True) + "e-mail: " + str(email) + new_line if email is not None else ""}' \
          f'{emojize(" :office:", use_aliases=True) + "Компанія: " + str(company) + new_line if company is not None else ""}' \
          f'{"-" * 20}\n' \
          f'id події: {event_id}\n' \
          f'{emojize(" :dizzy:", use_aliases=True) + "Назва події: " + str(title) + new_line if title is not None and title != "" else ""}' \
          f'{emojize(" :clock4:", use_aliases=True)}Дата події: {date_starts}\n' \
          f'{emojize(" :clock430:", use_aliases=True)}Дата закінчення: {date_ends}\n' \
          f'{emojize(" :triangular_flag_on_post:", use_aliases=True) + "Місце проведення: " + str(location) + new_line if location is not None else ""}' \
          f'{emojize(" :tophat:", use_aliases=True) + "Кількість гостей: " + str(guests) + new_line if guests is not None else ""}' \
          f'{"Тип події: " + str(type_of_event) + new_line if type_of_event is not None else ""}' \
          f'{"Клас події: " + str(class_of_event) + new_line if class_of_event is not None else ""}' \

    return msg


def classify_role(func):
    """
    Decorator for classification user role
    :param func: function which displays menu
    :return: wrapped function
    """
    def inner_func(message, edit=False):
        role_id, role_name = model.get_user_role_by_id(message.chat.id)
        func(message=message, user_role=role_name, edit=edit)
    return inner_func


@classify_role
def show_main_menu(message, user_role, edit=False):
    """
    Function shows main menu depends of user role
    :param message: message instance
    :param user_role: user role passed via decorator
    :param edit: flag which says if message needed to edit
    :return: None
    """
    try:
        inline_kb = None
        msg = ''

        if user_role == 'не підтверджено':
            logger.write_to_log('requested not accepted menu', message.chat.id)

            role_status = model.get_role_request_status(message.chat.id)[0]
            quali_status = model.get_qualification_request_status(message.chat.id)[0]

            msg = f'Статус ваших заявок:\n' \
                  f'{"-"*20}\n' \
                  f'{emojize(" :negative_squared_cross_mark:", use_aliases=True) if role_status == 0 else emojize(":white_check_mark:", use_aliases=True)}Заявка на посаду: {"підтверджена" if role_status == 1 else "не підтверджена"}\n' \
                  f'{emojize(" :negative_squared_cross_mark:", use_aliases=True) if quali_status == 0 else emojize(":white_check_mark:", use_aliases=True)}Заявка на кваліфікацію: {"підтверджена" if quali_status == 1 else "не підтверджена"}\n' \
                  f'{"-"*20}\n' \
                  f' Щойно вони будуть оброблені, ви будете повідомлені. Ви можете оновити свій статус кнопкою нижче'

            inline_kb = types.InlineKeyboardMarkup()
            inline_kb.add(types.InlineKeyboardButton(text=f'{emojize(" :repeat:", use_aliases=True)}Оновити статус', callback_data='main_menu'))

            logger.write_to_log('displayed not accepted menu', message.chat.id)
        elif user_role == 'адміністратор':
            logger.write_to_log('requested admin panel', message.chat.id)

            pending_requests = model.get_unaccepted_request_count()
            requests_str = f'{emojize(":negative_squared_cross_mark:", use_aliases=True) if pending_requests > 0 else emojize(" :white_check_mark:", use_aliases=True)} Не підтверджених заявок{(": " + str(pending_requests)) if pending_requests > 0 else " немає"}'
            msg = f'Панель адміністратора\n' \
                  f'{"-"*20}\n' \
                  f'{ requests_str }\n' \
                  f'{"-"*20}'

            inline_kb = types.InlineKeyboardMarkup(row_width=1)

            confirm_requests = types.InlineKeyboardButton(text=f'{emojize(":white_check_mark:", use_aliases=True)}Підтвердження заявок', callback_data='confirm_requests')
            stats = types.InlineKeyboardButton(text=f'{emojize(":chart_with_upwards_trend:", use_aliases=True)}Статистика', callback_data='adm_stats')
            update = types.InlineKeyboardButton(text=f'{emojize(" :repeat:", use_aliases=True)}Оновити статус', callback_data='main_menu')
            if pending_requests > 0:
                inline_kb.add(confirm_requests, stats, update)
            else:
                inline_kb.add(stats, update)
            logger.write_to_log('displayed admin panel', message.chat.id)
        elif user_role == 'менеджер':
            logger.write_to_log('requested manager menu', message.chat.id)
            staff_pending_requests = model.get_unaccepted_request_count()
            event_pending_requests = model.get_unaccepted_event_requests_count()
            upcoming_events = model.get_upcoming_events()
            upcoming_shifts = model.get_upcoming_shifts()

            staff_requests_str = f'{emojize(" :busts_in_silhouette:", use_aliases=True)}{emojize(":negative_squared_cross_mark:", use_aliases=True) if staff_pending_requests > 0 else emojize(" :white_check_mark:", use_aliases=True)} Не підтверджених заявок персоналу{(": " + str(staff_pending_requests)) if staff_pending_requests > 0 else " немає"}'
            event_requests_str = f'{emojize(" :dizzy:", use_aliases=True)}{emojize(":negative_squared_cross_mark:", use_aliases=True) if event_pending_requests > 0 else emojize(" :white_check_mark:", use_aliases=True)} Не підтверджених заявок на події{(": " + str(event_pending_requests)) if event_pending_requests > 0 else " немає"}'
            upcoming_shifts_str = f'{emojize(" :open_file_folder:", use_aliases=True)}Змін на черзі: {upcoming_shifts.__len__()}'

            msg = f'Меню менеджера\n' \
                  f'{"-" * 20}\n' \
                  f'{staff_requests_str}\n' \
                  f'{event_requests_str}\n' \
                  f'{upcoming_shifts_str}\n'

            inline_kb = types.InlineKeyboardMarkup(row_width=1)

            confirm_requests = types.InlineKeyboardButton(
                text=f'{emojize(" :busts_in_silhouette:", use_aliases=True)}{emojize(":white_check_mark:", use_aliases=True)}Підтвердження заявок персоналу',
                callback_data='confirm_requests')

            confirm_event_requests = types.InlineKeyboardButton(
                text=f'{emojize(" :dizzy:", use_aliases=True)}{emojize(":white_check_mark:", use_aliases=True)}Підтвердження заявок на події',
                callback_data='confirm_event_requests')

            modify_events = types.InlineKeyboardButton(
                text=f'{emojize(" :pencil:", use_aliases=True)}Редагувати деталі події',
                callback_data='edit_event_details'
            )

            set_main_on_shift = types.InlineKeyboardButton(
                text=f'{emojize(" :cop:", use_aliases=True)}Призначити головного на зміну',
                callback_data='set_main_on_shift')

            change_main_on_shift = types.InlineKeyboardButton(
                text=f'{emojize(" :boy:", use_aliases=True)}Змінити головного на зміні',
                callback_data='change_main_on_shift')

            get_manager_stat = types.InlineKeyboardButton(
                text=f'{emojize(" :bar_chart:", use_aliases=True)}Отримати статистику',
                callback_data='get_manager_statistics')
            # TODO: add manager statistics

            update = types.InlineKeyboardButton(text=f'{emojize(" :repeat:", use_aliases=True)}Оновити статус',
                                                callback_data='main_menu')
            if staff_pending_requests > 0 and event_pending_requests > 0:
                inline_kb.row(confirm_requests, confirm_event_requests)
            elif (staff_pending_requests == 0) and (event_pending_requests > 0):
                inline_kb.row(confirm_event_requests)
            elif (staff_pending_requests > 0) and (event_pending_requests == 0):
                inline_kb.row(confirm_requests)

            if upcoming_events.__len__() > 0:
                inline_kb.row(modify_events)

            with_supervisor, without_supervisor = check_shifts_with_supervisor(upcoming_shifts)

            if 0 < upcoming_shifts.__len__() == with_supervisor:
                inline_kb.row(change_main_on_shift)
            elif 0 < upcoming_shifts.__len__() == without_supervisor:
                inline_kb.row(set_main_on_shift)
            elif 0 < upcoming_shifts.__len__() and (without_supervisor + with_supervisor) == upcoming_shifts.__len__():
                inline_kb.row(set_main_on_shift, change_main_on_shift)
            inline_kb.row(get_manager_stat)
            inline_kb.row(update)

            logger.write_to_log('displayed manager menu', message.chat.id)
        elif user_role == 'офіціант':
            logger.write_to_log('requested waiter menu', message.chat.id)

            staff_id, fn, mn, ln, role_id, qualification_id, curr_rat, gen_rat, reg_date, events_done, rate = model.get_staff_by_id(message.chat.id)
            shifts_ext = model.get_staff_shifts(message.chat.id)
            upcoming_shifts = 0

            for sh in shifts_ext:
                if (sh[8]-datetime.now()).seconds > 0:
                    upcoming_shifts += 1

            msg = f'Меню офіціанта\n' \
                  f'{"-" * 20}\n' \
                  f'{emojize(" :white_check_mark:", use_aliases=True)}Відпрацьованих подій:{events_done}\n' \
                  f'{emojize(" :chart_with_upwards_trend:", use_aliases=True)}Поточний рейтинг:{curr_rat}\n' \
                  f'{emojize(" :soon:", use_aliases=True)}Майбутніх змін:{upcoming_shifts}'

            inline_kb = types.InlineKeyboardMarkup(row_width=1)

            check_available_shifts = types.InlineKeyboardButton(text=f'{emojize(" :boom:", use_aliases=True)}Переглянути доступні зміни', callback_data='get_available_shifts')
            check_registered_shifts = types.InlineKeyboardButton(text=f'{emojize(" :date:", use_aliases=True)}Переглянути зареєстровані зміни', callback_data='check_staff_registered_shifts')
            check_in = types.InlineKeyboardButton(text=f'{emojize(":radio_button:", use_aliases=True)}Підтвердити явку', callback_data=f'check_in')
            check_out = types.InlineKeyboardButton(text=f'{emojize(":ballot_box_with_check:", use_aliases=True)}Закінчити зміну', callback_data=f'check_out')
            update = types.InlineKeyboardButton(text=f'{emojize(" :repeat:", use_aliases=True)}Оновити статус', callback_data='main_menu')
            stat = types.InlineKeyboardButton(text=f'{emojize(":bar_chart:", use_aliases=True)}Статистика', callback_data=f'waiter_statistics')

            # TODO: add shift archive to statistics

            if model.get_available_shift_for_staff(message.chat.id, qualification_id).__len__() > 0:
                inline_kb.row(check_available_shifts)

            if model.get_staff_registered_shifts(message.chat.id).__len__() > 0:
                inline_kb.row(check_registered_shifts)

            inline_kb.row(check_in)
            inline_kb.row(check_out)
            inline_kb.row(stat)
            inline_kb.row(update)

            logger.write_to_log('displayed waiter menu', message.chat.id)

        if edit:
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=message.message_id,
                                  text=msg)
            bot.edit_message_reply_markup(chat_id=message.chat.id,
                                          message_id=message.message_id,
                                          reply_markup=inline_kb)
        else:
            bot.send_message(chat_id=message.chat.id, text=msg, reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.message_handler(content_types=['text'])
def echo_msg(message):
    bot.send_message(message.chat.id, 'як буде готово, я скажу')
    bot.send_message(message.chat.id, 'микола, не балуйся тут з своїми ' + message.text)
