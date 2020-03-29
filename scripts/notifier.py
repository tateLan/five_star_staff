import config
from emoji import emojize
from telebot import types


class Notifier:
    def __init__(self, bot):
        self.bot = bot

    def notify_manager_about_qualification_request(self, managers_list):
        """
        Notifies managers about new request
        :param managers_list: list of managers, registered in system
        :return: list of managers id, and message_ids for updating table
        """
        results = []
        for manager, manager_menu_id in managers_list:
            self.bot.edit_message_text(chat_id=manager[0],
                                       message_id=manager_menu_id,
                                       text=f'Для вас є сповіщення. Потрапити до меню, ви можете натиснувши відповідну кнопку нижче',
                                       reply_markup=None)

            msg = f'Була створена заявка на підтвердження кваліфікації! ' \
                  f'Будь ласка, перейдіть в відповідний розділ меню щоб підтверити її'

            inline_kb = types.InlineKeyboardMarkup()
            inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :house:", use_aliases=True)}Головне меню',
                                                     callback_data=f'main_menu_new'))

            notification_id = self.bot.send_message(chat_id=manager[0],
                                  parse_mode='Markdown',
                                  text=msg,
                                  reply_markup=inline_kb).message_id
            results.append((manager[0], notification_id))
        return results

    def notify_manager_about_role_request(self, managers_list):
        """
        Notifies managers about new request
        :param managers_list: list of managers, registered in system
        :return: list of managers id, and message_ids for updating table
        """
        results = []
        for manager, manager_menu_id in managers_list:
            self.bot.edit_message_text(chat_id=manager[0],
                                       message_id=manager_menu_id,
                                       text=f'Для вас є нове сповіщення. Потрапити до меню, ви можете натиснувши відповідну кнопку нижче',
                                       reply_markup=None)

            msg = f'Була створена заявка на підтвердження посади! ' \
                  f'Будь ласка, перейдіть в відповідний розділ меню щоб підтверити її'

            inline_kb = types.InlineKeyboardMarkup()
            inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :house:", use_aliases=True)}Головне меню',
                                                     callback_data=f'main_menu_new'))

            notification_id = self.bot.send_message(chat_id=manager[0],
                                  parse_mode='Markdown',
                                  text=msg,
                                  reply_markup=inline_kb).message_id
            results.append((manager[0], notification_id))
        return results

    def notify_about_exception(self, err):
        """
        Notifies developer, about any exception
        :param err: instance of exception
        :return: None
        """
        msg = f'{(emojize(":x:", use_aliases=True) * 7)}\nException\n' \
              f'{format(err)}\n' \
              f'{(emojize(":x:", use_aliases=True) * 7)}'
        self.bot.send_message(chat_id=config.DEVELOPER_ID, text=msg)

    def notify_user_about_accepted_request(self, user_id, user_message_id):
        """
        Notifies staff about accepting any of their request
        :param user_id: staff telegram id
        :param user_message_id: message id of last message, needed to be changed
        :return: id of new message, which might need to be changed
        """
        self.bot.edit_message_text(chat_id=user_id,
                                   message_id=user_message_id,
                                   text=f'Для вас є нове сповіщення. Потрапити до меню, ви можете натиснувши відповідну кнопку нижче',
                                   reply_markup=None)

        msg = f'Один з ваших запитів було схавено! Ви можете перейти до головного меню, ' \
              f'та переглянути стан вашого облікового запису!'

        inline_kb = types.InlineKeyboardMarkup()
        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :house:", use_aliases=True)}Головне меню',
                                                 callback_data=f'main_menu_new'))

        notification_id = self.bot.send_message(chat_id=user_id,
                                                parse_mode='Markdown',
                                                text=msg,
                                                reply_markup=inline_kb).message_id
        return notification_id

    def notify_about_price_changing(self, event_id):
        # TODO: implement client notification
        pass

    def notify_waiter_about_upcoming_shift(self, notification, main_menu_id):
        """
        Notifies waiter about upcoming shift(24 or 3 hours)
        :param notification: set of data, needed for notification (staff id,
                                                                   time left to shift,
                                                                   start time,
                                                                   shift title)
        :return: None
        """
        self.bot.edit_message_text(chat_id=notification[0],
                                   message_id=main_menu_id,
                                   text=f'Для вас є сповіщення. Потрапити до меню, ви можете натиснувши відповідну кнопку нижче',
                                   reply_markup=None)

        msg = f'{emojize(" :boom:", use_aliases=True)}Увага! До зміни {notification[3]} лишилось *{notification[1]}*\n' \
              f'{emojize(" :clock430:", use_aliases=True)}Початок зміни о {notification[2]}'

        inline_kb = types.InlineKeyboardMarkup()
        inline_kb.row(types.InlineKeyboardButton(text=f'{emojize(" :house:", use_aliases=True)}Головне меню',
                                                 callback_data=f'main_menu_new'))

        self.bot.send_message(chat_id=notification[0],
                              parse_mode='Markdown',
                              text=msg,
                              reply_markup=inline_kb)
