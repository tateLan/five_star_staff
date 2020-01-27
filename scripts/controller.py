import config
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
        #   +         +       +          +-        +-          +           +       +           +-              +-              +-
        request_id, event_id, client_id, title, location, date_starts, date_ends, guests, type_of_event_id, class_of_event_id, staff_needed = model.get_event_request_extended_info()
        _, client_username, f_name, l_name, company, phone, email = model.get_client_by_id(client_id)
        inline_kb = types.InlineKeyboardMarkup()

        class_of_event = None
        type_of_event = None

        if type_of_event_id is not None:
            _, type_of_event = model.get_type_of_event_by_id(type_of_event_id)
        if class_of_event_id is not None:
            _, class_of_event = model.get_class_of_event_by_id(class_of_event_id)

        msg = get_extended_event_info_message((request_id, event_id, client_id, title, location, date_starts, date_ends,
                                               guests, type_of_event_id, class_of_event_id, staff_needed, type_of_event,
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
        if staff_needed is None or staff_needed == '':
            inline_kb.row(types.InlineKeyboardButton(text='Внести кількість персоналу', callback_data=f'edit_event_id:{event_id}_staff'))

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


@bot.callback_query_handler(func=lambda call: call.data.split('update_event_type_id:').__len__() > 0)
def get_event_type(call):
    try:
        id = call.data.split('update_event_type_id:')[1].split('_')[0]
        type_id = call.data.split('update_event_type_id:')[1].split('_set:')[1]

        model.update_event_type(id, type_id)

        msg = f'{emojize(" :tada:", use_aliases=True)} Тип події оновлено!'
        inline_kb = types.InlineKeyboardMarkup()

        inline_kb.row(
            types.InlineKeyboardButton(text='До меню редагування події', callback_data='confirm_event_requests'))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=inline_kb)
    except Exception as err:
        method_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {method_name} - {err}', 'controller')


@bot.callback_query_handler(func=lambda call: call.data.split('edit_event_id:').__len__() > 0)
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
            pass
        elif parameter == 'staff':
            pass

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

            inline_kb.row(
                types.InlineKeyboardButton(text='До меню редагування події', callback_data='confirm_event_requests'))

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

            inline_kb.row(types.InlineKeyboardButton(text='До меню редагування події', callback_data='confirm_event_requests'))

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
    request_id, event_id, client_id, title, location, date_starts, date_ends, guests, type_of_event_id, class_of_event_id, staff_needed, type_of_event, class_of_event, client_username, f_name, l_name, company, phone, email = params
    new_line = '\n'

    msg = f'{emojize(" :dizzy:", use_aliases=True)}{type_of_action}\n' \
          f'{"-" * 20}\n' \
          f'{emojize(" :clipboard:", use_aliases=True)}ПІП: {l_name} {f_name}\n' \
          f'{"Telegram нік клієнта: @" + str(client_username) + new_line if client_username is not None else ""}' \
          f'{emojize(" :phone:", use_aliases=True)}Номер телефону: {phone}\n' \
          f'{emojize(" :e-mail:", use_aliases=True) + "e-mail: " + str(email) + new_line if email is not None else ""}' \
          f'{emojize(" :office:", use_aliases=True) + "Компанія: " + str(company) + new_line if company is not None else ""}' \
          f'{"-" * 20}\n' \
          f'{emojize(" :dizzy:", use_aliases=True) + "Назва події: " + str(title) + new_line if title is not None and title != "" else ""}' \
          f'{emojize(" :clock4:", use_aliases=True)}Дата події: {date_starts}\n' \
          f'{emojize(" :clock430:", use_aliases=True)}Дата закінчення: {date_ends}\n' \
          f'{emojize(" :triangular_flag_on_post:", use_aliases=True) + "Місце проведення: " + str(location) + new_line if location is not None else ""}' \
          f'{emojize(" :tophat:", use_aliases=True) + "Кількість гостей: " + str(guests) + new_line if guests is not None else ""}' \
          f'{"Тип події: " + str(type_of_event) + new_line if type_of_event is not None else ""}' \
          f'{"Клас події: " + str(class_of_event) + new_line if class_of_event is not None else ""}' \
          f'{emojize(" :busts_in_silhouette:", use_aliases=True) + "Кількість персоналу: " + str(staff_needed) + new_line if staff_needed is not None else ""}'

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

            staff_requests_str = f'{emojize(" :busts_in_silhouette:", use_aliases=True)}{emojize(":negative_squared_cross_mark:", use_aliases=True) if staff_pending_requests > 0 else emojize(" :white_check_mark:", use_aliases=True)} Не підтверджених заявок персоналу{(": " + str(staff_pending_requests)) if staff_pending_requests > 0 else " немає"}'
            event_requests_str = f'{emojize(" :dizzy:", use_aliases=True)}{emojize(":negative_squared_cross_mark:", use_aliases=True) if event_pending_requests > 0 else emojize(" :white_check_mark:", use_aliases=True)} Не підтверджених заявок на події{(": " + str(event_pending_requests)) if event_pending_requests > 0 else " немає"}'

            msg = f'Меню менеджера\n' \
                  f'{"-" * 20}\n' \
                  f'{staff_requests_str}\n' \
                  f'{event_requests_str}\n'


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

            update = types.InlineKeyboardButton(text=f'{emojize(" :repeat:", use_aliases=True)}Оновити статус',
                                                callback_data='main_menu')
            if staff_pending_requests > 0 and event_pending_requests > 0:
                inline_kb.row(confirm_requests, confirm_event_requests)
            elif (staff_pending_requests == 0) and (event_pending_requests > 0):
                inline_kb.row(confirm_event_requests)
            elif (staff_pending_requests > 0) and (event_pending_requests == 0):
                inline_kb.row(confirm_requests)

            inline_kb.row(modify_events)
            inline_kb.row(set_main_on_shift, change_main_on_shift)
            inline_kb.row(get_manager_stat)
            inline_kb.row(update)

            # TODO: update manager menu

            logger.write_to_log('displayed manager menu', message.chat.id)
        elif user_role == 'офіціант':
            logger.write_to_log('requested waiter menu', message.chat.id)
            # TODO: waiter menu
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
