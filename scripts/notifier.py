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