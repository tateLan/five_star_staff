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


def init_controller():
    """
    Controller initialization
    :return: None
    """
    try:
        logger.write_to_log('controller initialised', 'sys')
        bot.polling(none_stop=True)

    except Exception as err:
        meth_name = sys._getframe( ).f_code.co_name
        logger.write_to_log('exception', 'sys')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'sys')


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
        meth_name = sys._getframe( ).f_code.co_name
        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
        meth_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
        meth_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
        meth_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
        meth_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
        meth_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
        meth_name = sys._getframe( ).f_code.co_name
        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
        meth_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
        meth_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
        meth_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
        meth_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


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
            # TODO: manager menu
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
        meth_name = sys._getframe( ).f_code.co_name

        logger.write_to_log('exception', 'controller')
        logger.write_to_err_log(f'exception in method {meth_name} - {err}', 'controller')


@bot.message_handler(content_types=['text'])
def echo_msg(message):
    bot.send_message(message.chat.id, 'микола, не балуйся тут з своїми ' + message.text)
    bot.send_message(message.chat.id, 'як буде готово, я скажу')
