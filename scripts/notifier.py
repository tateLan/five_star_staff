import config
from emoji import emojize


class Notifier:
    def __init__(self, bot):
        self.bot = bot

    def notify_manager_about_qualification_request(self):
        # TODO:implement qualification request notifier
        pass

    def notify_manager_about_role_request(self):
        # TODO:implement role request notifier
        pass

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

    def notify_waiter_about_upcoming_shift(self, notification):
        """
        Notifies waiter about upcoming shift(24 or 3 hours)
        :param notification: set of data, needed for notification (staff id,
                                                                   time left to shift,
                                                                   start time,
                                                                   shift title)
        :return: None
        """
        msg = f'{emojize(" :boom:", use_aliases=True)}Увага! До зміни {notification[3]} лишилось *{notification[1]}*\n' \
              f'{emojize(" :clock430:", use_aliases=True)}Початок зміни о {notification[2]}'

        self.bot.send_message(chat_id=notification[0],
                              parse_mode='Markdown',
                              text=msg)
