import db_handler as db
import user_menu


class Model:
    def __init__(self, bot, logger, notifier):
        """
        Initialization of Model class
        :param bot: bot instance for passing into notifier class
        :param logger: logger instance
        """
        try:
            self.db_handler = db.DbHandler()
            self.bot = bot
            self.logger = logger
            self.notifier = notifier
            logger.write_to_log('model initialised', 'sys')
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def get_start_command_response(self, user_id):
        """
        Method generating response for user starting work with system
        :param user_id: telegram user id
        :return: /start command response
        """
        try:
            self.logger.write_to_log('/start command response requested', user_id)
            res = self.db_handler.get_user_by_telegram_id(user_id)
            reply = ''

            if res == '0':
                reply = 'Вітаю! Ви ще не зареєстровані в нашій системі, будь ласка пройдіть реєстрацію'
            else:
                reply = 'Вітаємо з поверненням, '

                for x in res:
                    reply += x
                    reply += ' '

            self.logger.write_to_log('/start command response created', user_id)
            return reply

        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def register_user_telegram_id(self, user_id):
        """
        Method adds new users telegram id to db
        :param user_id: user's telegram id
        :return: None
        """
        try:
            self.db_handler.set_user_telegram_id(user_id)
            self.logger.write_to_log('user telegram id added to db', user_id)
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def register_user_first_name(self, message):
        """
        Registers user first name into db
        :param message: message instance
        :return: None
        """
        try:
            self.db_handler.set_user_first_name(message.chat.id, message.text)

            self.logger.write_to_log('user first name added to db', message.chat.id)
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def register_user_middle_name(self, message):
        """
        Registers user middle name into db
        :param message: message instance
        :return: None
        """
        try:
            self.db_handler.set_user_middle_name(message.chat.id, message.text)

            self.logger.write_to_log('user middle name added to db', message.chat.id)
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def register_user_last_name(self, message):
        """
        Registers user last name into db
        :param message: message instance
        :return: None
        """
        try:
            self.db_handler.set_user_last_name(message.chat.id, message.text)

            self.logger.write_to_log('user last name added to db', message.chat.id)
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def get_roles_list(self):
        """
        Returns list of available roles
        :return: list of roles
        """
        try:
            roles = self.db_handler.get_roles_list()
            self.logger.write_to_log('roles got', 'model')
            return roles
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def register_role_request(self, role, user_id):
        """
        Registers user request to role confirmation
        :param role: requested role (text)
        :param user_id: user telegram id
        :return: None
        """
        try:
            roles_list = self.db_handler.get_roles_list()
            id_not_set = self.db_handler.get_not_set_role()
            selected_id = None

            for x in roles_list:
                if x[1] == role:
                    selected_id = x[0]
                    break
            self.db_handler.left_role_approving_request(user_id, selected_id)
            self.logger.write_to_log('role approving request left', user_id)

            self.db_handler.set_user_role(user_id, id_not_set)
            self.logger.write_to_log('user role changed to undefined', user_id)

            self.notifier.notify_manager_about_role_request()
            self.logger.write_to_log('manager notified about role request', user_id)
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def get_qualification_list(self):
        """
        Method returns list of qualifications
        :return: list of qualifications
        """
        try:
            qualifications = self.db_handler.get_qualifications_list()
            self.logger.write_to_log('qualifications got', 'model')
            return qualifications
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def register_qualification_request(self, quali, user_id):
        """
        Method registers user qualification request
        :param quali: qualification (text)
        :param user_id: user telegram id
        :return: None
        """
        try:
            qualifications_list = self.db_handler.get_qualifications_list()
            id_not_set = self.db_handler.get_not_set_qualification()
            selected_id = None

            for x in qualifications_list:
                if x[1] == quali:
                    selected_id = x[0]
                    break
            self.db_handler.left_qualification_approving_request(user_id, selected_id)
            self.logger.write_to_log('qualification approving request left', user_id)

            self.db_handler.set_user_qualification(user_id, id_not_set)
            self.logger.write_to_log('user qualification changed to undefined', user_id)

            self.notifier.notify_manager_about_qualification_request()
            self.logger.write_to_log('manager notified about qualification request', user_id)
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def get_user_role_by_id(self, user_id):
        """
        Returns information about user role
        :param user_id: user telegram id
        :return: set of role id and role name
        """
        try:
            role = self.db_handler.get_user_role_by_id(user_id)

            self.logger.write_to_log('got user role information', user_id)

            return role
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')

    def get_unaccepted_request_count(self):
        """
        Method returns number of unaccepted requests
        :return: number of requests
        """
        try:
            role_requests = self.db_handler.get_unaccepted_role_requests()
            quali_requests = self.db_handler.get_unaccepted_qualification_requests()

            return role_requests.__len__() + quali_requests.__len__()
        except Exception as err:
            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception - {err}', 'model')
