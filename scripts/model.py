import db_handler as db
from datetime import datetime
import sys
import config
import math
import geopy.distance


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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_role_by_id(self, role_id):
        """
        returns role information by role id
        :param role_id:role id
        :return: role information
        """
        try:
            role = self.db_handler.get_role_by_id(role_id)

            self.logger.write_to_log('got role by id', 'model')
            return role
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_qualification_by_id(self, quali_id):
        """
        Returns qualification instance
        :param quali_id: id
        :return:qualification instance
        """
        try:
            quali = self.db_handler.get_qualification_by_id(quali_id)

            self.logger.write_to_log('got qualification by id', 'model')
            return quali
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

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
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_unaccepted_request_count(self):
        """
        Method returns number of unaccepted requests
        :return: number of requests
        """
        try:
            role_requests = self.db_handler.get_unaccepted_role_requests()
            quali_requests = self.db_handler.get_unaccepted_qualification_requests()

            self.logger.write_to_log('count of unaccepted requests got', 'model')

            return role_requests.__len__() + quali_requests.__len__()
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_role_request_status(self, user_id):
        """
        Returns role request status
        :param user_id: user telegram id
        :return: Status
        """
        try:
            status = self.db_handler.get_role_request_status(user_id)

            self.logger.write_to_log('got role request status', user_id)
            return status
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_qualification_request_status(self, user_id):
        """
        Returns qualification request status
        :param user_id: user telegram id
        :return: Status
        """
        try:
            status = self.db_handler.get_qualification_request_status(user_id)

            self.logger.write_to_log('got qualification request status', user_id)
            return status
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_unaccepted_role_requests(self):
        """
        Returns role pending request
        :return: pending role request
        """
        try:
            role_request = self.db_handler.get_unaccepted_role_requests()

            self.logger.write_to_log('role requests got', 'model')

            return role_request

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_unaccepted_qualification_requests(self):
        """
        Returns qualification pending requests
        :return: pending qualification requests
        """
        try:
            role_requests = self.db_handler.get_unaccepted_qualification_requests()

            self.logger.write_to_log('qualification requests got', 'model')

            return role_requests

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_user_name_by_id(self, user_id):
        """
        Returns user full name by telegram id
        :param user_id:  user telegram id
        :return: set of first name, middle name and last name of user
        """
        try:
            res = self.db_handler.get_user_name_by_id(user_id)

            self.logger.write_to_log('user full name got', user_id)

            return res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def accept_role_request(self, request_id, admin_id, id_user):
        """
        Accepts role request with specified id
        :param request_id: id of request
        :param admin_id: telegram id of user which accepted (manager or admin)
        :param id_user: telegram id of user which needed to be updated
        :return: None
        """
        try:
            now = datetime.now()
            role_id = self.db_handler.get_role_id_from_role_request(id_user)[0]
            mysql_date = f'{now.year}-{now.month}-{now.day} {now.time().hour}:{now.time().minute}:00'

            self.db_handler.accept_role_request(request_id, admin_id, mysql_date)
            self.logger.write_to_log(f'role request id:{request_id} confirmed', admin_id)
            self.db_handler.update_staff_role(id_user, role_id)
            self.logger.write_to_log(f'user data update in staff', id_user)
            self.notifier.notify_user_about_accepted_request(user_id=id_user, request_type='заявка на посаду')

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def change_role_request(self, request_id, role_id, admin_id, user_id):
        """
        Changes user requested role and confirms it
        :param request_id: id of role request
        :param role_id: id of role needed to change
        :param admin_id: telegram id of user (admin)
        :param user_id: telegram id of user (staff)
        :return: None
        """
        try:
            now = datetime.now()
            mysql_date = f'{now.year}-{now.month}-{now.day} {now.time().hour}:{now.time().minute}:00'

            self.db_handler.modify_role_request(request_id, role_id)
            self.db_handler.accept_role_request(request_id, admin_id, mysql_date)
            self.logger.write_to_log(f'role request id:{request_id} confirmed', admin_id)
            self.db_handler.update_staff_role(user_id, role_id)
            self.logger.write_to_log(f'user data update in staff', user_id)
            self.notifier.notify_user_about_accepted_request(user_id=user_id, request_type='заявка на посаду')

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def accept_qualification_request(self, request_id, admin_id, id_user):
        """
        Updates qualification request
        :param request_id: id of request
        :param admin_id: user telegram id (admin)
        :param id_user: user telegram id (staff)
        :return: None
        """
        try:
            now = datetime.now()
            mysql_date = f'{now.year}-{now.month}-{now.day} {now.time().hour}:{now.time().minute}:00'
            qual_id = self.db_handler.get_qualification_id_from_qualification_request(id_user)[0]

            self.db_handler.accept_qualification_request(request_id, admin_id, mysql_date)
            self.logger.write_to_log(f'qualification request id:{request_id} confirmed', admin_id)
            self.db_handler.update_staff_qualification(id_user, qual_id)
            self.logger.write_to_log(f'user data update in staff', id_user)
            self.notifier.notify_user_about_accepted_request(user_id=id_user, request_type='заявка на кваліфікацію')

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def change_qualification_request(self, request_id, qualification_id, admin_id, user_id):
        """
        Modifies qualification request due to selected option by admin/manager
        :param request_id: id of request
        :param qualification_id: id of selected qualification
        :param admin_id: user telegram id (admin)
        :param user_id:  user telegram id (staff)
        :return: None
        """
        try:
            now = datetime.now()
            mysql_date = f'{now.year}-{now.month}-{now.day} {now.time().hour}:{now.time().minute}:00'

            self.db_handler.modify_qualification_request(request_id, qualification_id)

            _, qualification_name = self.db_handler.get_qualification_by_id(qualification_id)

            if qualification_name == 'професіонал':
                self.db_handler.update_staff_rate(user_id, config.PRO_RATE)
            elif qualification_name == 'середній рівень':
                self.db_handler.update_staff_rate(user_id, config.MIDDLE_RATE)

            self.db_handler.accept_qualification_request(request_id, admin_id, mysql_date)
            self.logger.write_to_log(f'qualification request id:{request_id} confirmed', admin_id)
            self.db_handler.update_staff_qualification(user_id, qualification_id)
            self.logger.write_to_log(f'user data update in staff', user_id)
            self.notifier.notify_user_about_accepted_request(user_id=user_id, request_type='заявка на кваліфікацію')

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_users_count(self):
        """
        Returns string of number registered users by every role
        :return: string with numbers of staff
        """
        try:
            roles = self.db_handler.get_roles_list()
            reply = ''

            for role_id, role_name in roles:
                reply += f'{role_name}ів - {self.db_handler.get_staff_count_by_role(role_id)[0]}\n'

            return reply


        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_db_session_duration(self):
        """
        Returns duration of current mysql session for admin statistics
        :return: session duration (seconds)
        """
        try:
            session_duration = self.db_handler.get_session_duration()

            self.logger.write_to_log('got session duration', sys._getframe().f_code.co_name)

            return session_duration
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_unaccepted_event_requests(self):
        """
        Returns list of unaccepted event requests
        :return:list of unaccepted event requests
        """
        try:
            self.logger.write_to_log('requested events unaccepted request', 'model')

            event_requests = self.db_handler.get_unaccepted_events_list()

            return event_requests

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_unaccepted_event_requests_count(self):
        """
        Returns count of unaccepted event requests
        :return: count of unaccepted event requests
        """
        return self.get_unaccepted_event_requests().__len__()

    def get_client_by_id(self, client_id):
        try:
            self.logger.write_to_log('requested event request', 'model')

            client = self.db_handler.get_client_by_id(client_id)

            return client
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_event_request(self):
        try:
            self.logger.write_to_log('requested event request', 'model')
            request = self.db_handler.get_event_request()

            return request
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_event_request_extended_info(self):
        try:
            self.logger.write_to_log('requested extended event request', 'model')
            request = self.db_handler.get_event_request_extended_info()

            return request
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_type_of_event_by_id(self, type_event_id):
        try:
            self.logger.write_to_log(f'event type {type_event_id} requested', 'model')
            return self.db_handler.get_event_type_by_id(type_event_id)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_class_of_event_by_id(self, class_event_id):
        try:
            self.logger.write_to_log(f'event class {class_event_id} requested', 'model')
            return self.db_handler.get_event_class_by_id(class_event_id)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def update_event_location(self, id, latitude, longitude):
        try:
            self.logger.write_to_log(f'updating event {id} location', 'model')

            geo = f'latitude:{latitude} longitude:{longitude}'
            self.db_handler.update_event_location(id, geo)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def update_event_title(self, id, title):
        try:
            self.logger.write_to_log(f'updating event {id} title', 'model')

            self.db_handler.update_event_title(id, title)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_event_types_list(self):
        try:
            self.logger.write_to_log('requested event types', 'model')

            return self.db_handler.get_event_types()

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_event_classes_list(self):
        try:
            self.logger.write_to_log('requested event classes', 'model')

            return self.db_handler.get_event_classes()

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def update_event_type(self, id, event_type):
        try:
            self.logger.write_to_log(f'updating event {id} type', 'model')

            self.db_handler.update_event_type(id, event_type)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def update_event_class(self, id, event_class):
        try:
            self.logger.write_to_log(f'updating event {id} class', 'model')

            self.db_handler.update_event_class(id, event_class)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def decline_event_request(self, event_id, manager_id):
        try:
            event_request_id = self.db_handler.get_event_request_id_by_event_id(event_id)[0]
            self.db_handler.update_event_request_accepted(event_request_id, manager_id)
            self.logger.write_to_log('event request processed', f'{manager_id}')
            self.db_handler.delete_event_by_id(event_id)
            self.logger.write_to_log(f'event {event_id} data was deleted', f'{manager_id}')
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def calculate_event_price_and_parameters(self, event_id):
        """
        Returns set of paramters needed to register event
        :param event_id: id of event to calculate
        :return: set of (price, number of professional staff, middle lvl staff, new staff)
        """
        try:
            price = 0
            proffesional_staff = 0
            middle_staff = 0
            new_staff = 0
            _, req_id, title, client_id, location, date_starts, date_ends, guests, event_type_id, event_class_id, _ = self.db_handler.get_event_request_extended_info_by_id(event_id)
            _, event_class_name, guests_per_waiter = self.db_handler.get_event_class_by_id(event_class_id)

            distance_in_km = self.get_geopy_diatance(location)
            price = distance_in_km * config.PRICE_OF_KM
            num_of_staff = math.ceil(guests / guests_per_waiter)

            if event_class_name == 'найвищий':  #85% of pro
                new_staff = 0
                proffesional_staff = math.ceil(num_of_staff * 0.85)
                middle_staff = num_of_staff - proffesional_staff
            elif event_class_name == 'високий':     #75% of pro
                new_staff = 0
                proffesional_staff = math.ceil(num_of_staff * 0.75)
                middle_staff = num_of_staff - proffesional_staff
            elif event_class_name == 'середній':
                new_staff = round(num_of_staff * 0.2)
                middle_staff = num_of_staff - new_staff
            elif event_class_name == 'початковий':
                middle_staff = math.ceil(num_of_staff * 0.3)
                new_staff = round(num_of_staff - middle_staff)

            hours_of_shift = (date_ends - date_starts).seconds / 3600

            price += proffesional_staff * config.PRO_RATE * hours_of_shift
            price += middle_staff * config.MID_RATE * hours_of_shift
            price += new_staff * config.NEW_RATE * hours_of_shift

            return (price,proffesional_staff,middle_staff,new_staff)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_geopy_diatance(self, location):
        """
        Returns distance in km to place where event going to be
        :param location: string with location of event
        :return: distance in km
        """
        try:
            event = (float(location.split('latitude:')[1].split(' ')[0]), float(location.split('longitude:')[1]))
            base = (float(config.OFFICE_COORDINATES[0]), float(config.OFFICE_COORDINATES[1]))

            return geopy.distance.vincenty(event, base).km
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def accept_event_price(self, event_id, price, pro, mid, beginers, processed_staff_id, currency):
        try:
            self.logger.write_to_log(f'price about event {event_id} being updated', 'model')
            self.notifier.notify_about_price_changing(event_id)

            self.update_event_request_processed(event_id, processed_staff_id)
            currencies = self.db_handler.get_currencies()
            currency_id = 0

            for id, name in currencies:
                if name == currency:
                    currency_id = id
                    break

            self.db_handler.update_event_price_and_staff(event_id, price, currency_id, int(pro)+int(mid)+int(beginers))
            self.logger.write_to_log('event data updated with price, currency and staff number', 'model')

            self.create_shift(event_id, int(pro), int(mid), int(beginers))
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def update_event_request_processed(self, event_id, processed_staff_id):
        try:
            self.logger.write_to_log('requested event request id', 'model')
            event_request_id = self.db_handler.get_event_request_id_by_event_id(event_id)[0]

            self.db_handler.update_event_request_accepted(event_request_id, processed_staff_id)
            self.logger.write_to_log(f'event request {event_request_id} updated', 'model')
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def create_shift(self, event_id, pro, mid, beginner):
        """
        Creates shift instance
        :param event_id: id of event, on which shift based
        :param pro: number of professional staff
        :param mid: number of middle staff
        :param beginner: number of beginners staff
        :return: None
        """
        try:
            self.db_handler.create_shift(event_id, pro, mid, beginner)
            self.logger.write_to_log('shift created', 'model')
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_upcoming_events(self):
        try:
            events = self.db_handler.get_upcoming_events()
            self.logger.write_to_log('upcoming events got', 'model')
            return events
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_upcoming_shifts(self):
        try:
            shifts = self.db_handler.get_upcoming_shifts()

            self.logger.write_to_log('upcoming shifts got', 'model')
            return shifts
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_client_by_event_request_id(self, event_request_id):
        try:
            _, client_id, _, _, _ = self.db_handler.get_event_request_by_id(event_request_id)
            client = self.db_handler.get_client_by_id(client_id)

            self.logger.write_to_log('client data got', 'model')

            return client
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_event_request_extended_info_by_id(self, event_id):
        try:
            self.logger.write_to_log('got event extended information', 'model')
            return self.db_handler.get_event_request_extended_info_by_id(event_id)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')


