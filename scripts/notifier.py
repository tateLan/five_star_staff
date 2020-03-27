import config
from emoji import emojize
from telebot import types


class Notifier:
    def __init__(self, bot):
        self.bot = bot

    def notify_manager_about_qualification_request(self, managers_list):
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
        msg = f'{(emojize(":x:", use_aliases=True) * 7)}\nException\n' \
              f'{format(err)}\n' \
              f'{(emojize(":x:", use_aliases=True) * 7)}'
        self.bot.send_message(chat_id=config.DEVELOPER_ID, text=msg)

    def notify_user_about_accepted_request(self, user_id, request_type):
        # TODO: implement user notification
        pass

    def notify_about_price_changing(self, event_id):
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
