import db_handler as db
from datetime import datetime
from datetime import timedelta
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

    def update_event_location(self, event_id, latitude, longitude):
        try:
            self.logger.write_to_log(f'updating event {event_id} location', 'model')

            geo = f'latitude:{latitude} longitude:{longitude}'
            self.db_handler.update_event_location(event_id, geo)
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

            distance_in_km = self.get_geopy_distance(location)
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

    def get_geopy_distance(self, location):
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

            shift_id = self.db_handler.get_event_id_from_shift(event_id)

            self.db_handler.update_event_price_and_staff(event_id, price, currency_id, int(pro)+int(mid)+int(beginers))
            self.logger.write_to_log('event data updated with price, currency and staff number', 'model')

            if shift_id is None:
                self.create_shift(event_id, int(pro), int(mid), int(beginers))
            else:
                self.update_shift(shift_id, int(pro), int(mid), int(beginers))

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

    def update_shift(self, shift_id, pro, mid, beginner):
        """
        Updates shift instance if price updates
        :param shift_id: id of shift
        :param pro: number of professionals
        :param mid:number of middles
        :param beginner:number of beginners
        :return: None
        """
        try:
            self.db_handler.update_shift_by_id(shift_id, pro, mid, beginner)
            self.logger.write_to_log('shift updated', 'model')
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

    def is_event_processed(self, event_id):
        try:
            res = self.db_handler.is_event_processed(event_id)

            self.logger.write_to_log('event status got', 'model')

            return bool(res)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_shift_extended_info_by_id(self, shift_id):
        try:
            self.logger.write_to_log('shift extended information requested', 'model')
            shift_info = self.db_handler.get_shift_extended_info_by_id(shift_id)
            return shift_info
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_registered_to_shift_staff(self, shift_id):
        try:
            registered_to_shift = self.db_handler.get_registered_to_shift(shift_id)
            self.logger.write_to_log('list of registered to shift got', 'model')

            return registered_to_shift
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staff_by_id(self, staff_id):
        try:
            staff = self.db_handler.get_staff_by_id(staff_id)

            self.logger.write_to_log(f'staff by id {staff_id} got', 'model')

            return staff
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def update_shift_supervisor(self, shift_id, staff_id):
        try:
            self.db_handler.update_shift_supervisor(shift_id, staff_id)
            self.logger.write_to_log(f'shift {shift_id} supervisor updated', 'model')
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staff_shifts(self, staff_id, worked=True):
        """
        Returns extended information about shifts staff worked
        :param staff_id: telegram id of staff
        :param worked: boolean value, marks which types of shift requests needed (worked of canceled). True by default
        :return: list of extended information about shifts
        """
        try:
            self.logger.write_to_log('requested staff shifts', 'model')

            shifts = []

            shift_registrations = self.db_handler.get_staff_shift_registrations(staff_id)
            if worked:
                for reg_id, shift_id, staff_id, date_registered, registered, check_in, check_out, rating, payment in shift_registrations:
                    if registered == 1:
                        shifts.append(self.db_handler.get_shift_extended_info_by_id(shift_id))
            else:
                for reg_id, shift_id, staff_id, date_registered, registered, check_in, check_out, rating, payment in shift_registrations:
                    if registered == 0:
                        shifts.append(self.db_handler.get_shift_extended_info_by_id(shift_id))

            self.logger.write_to_log('got staff shifts', 'model')

            return shifts
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_available_shift_for_staff(self, staff_id, staff_qualification_id):
        """
        Checks if there's shifts available for staff
        :param staff_id: telegram id of staff
        :param staff_qualification_id: id of qualification of staff
        :return: list of available shifts
        """
        try:
            self.logger.write_to_log(f'requested available shifts for {staff_id}', 'model')

            staff = self.db_handler.get_staff_by_id(staff_id)
            shifts = self.db_handler.get_upcoming_shifts()
            _, quali_name = self.db_handler.get_qualification_by_id(staff_qualification_id)

            available_shifts = []

            for shift in shifts:
                registered_to_shift = self.db_handler.get_staff_id_registered_to_shift_by_id(shift[0])

                staff_needed = 0
                staff_current_quali_registered = 0

                if quali_name == 'професіонал':
                    if shift[2] == 0:
                        continue
                    else:
                        staff_needed = shift[2]
                elif quali_name == 'середній рівень':
                    if shift[3] ==0:
                        continue
                    else:
                        staff_needed = shift[3]
                elif quali_name == 'початківець':
                    if shift[4] == 0:
                        continue
                    else:
                        staff_needed = shift[4]

                if (staff_id,) in registered_to_shift:
                    continue

                for reg in registered_to_shift:
                    if reg[0] != staff_id:
                        worker = self.db_handler.get_staff_by_id(reg[0])
                        if worker[5] == staff_qualification_id:
                            staff_current_quali_registered += 1

                if staff_needed > staff_current_quali_registered:
                    available_shifts.append(shift)

            self.logger.write_to_log(f'got available shifts for {staff_id}', 'model')

            return available_shifts
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def register_for_shift(self, shift_id, staff_id):
        """
        Checks if staff can register for shift (due to time limits) and registers (or not) him to shift
        :param shift_id: shift id
        :param staff_id: staff telegram id
        :return: status (1 - registered to shift, 0 - no)
        """
        try:
            result = False
            conflict = False

            date = datetime.now()
            mysql_date = f'{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:00'

            shifts_registered_on = self.db_handler.get_staff_registered_shifts_by_id(staff_id)
            shift_pretending = self.db_handler.get_shift_extended_info_by_id(shift_id)

            if shifts_registered_on.__len__() > 0:
                for shift in shifts_registered_on:
                    diff = shift[1] - shift_pretending[8]

                    if diff > timedelta(minutes=0):    # shift is later
                        interval = (diff - (shift_pretending[9] - shift_pretending[8])).seconds / 3600
                        if interval >= config.HOURS_BETWEEN_SHIFTS:
                            conflict = False
                        else:
                            conflict = True
                            break
                    else:   # pretending is later
                        diff = shift_pretending[8] - shift[1]
                        interval = (diff.days * 24) + (diff - (shift[2] - shift[1])).seconds / 3600
                        if interval >= config.HOURS_BETWEEN_SHIFTS:
                            conflict = False
                        else:
                            conflict = True
                            break

            if conflict:
                result = False
            else:
                if self.db_handler.get_shift_registration_by_staff_id_and_shift_id(staff_id, shift_id) is not None:
                    self.db_handler.reregister_staff_to_shift(shift_id, staff_id, mysql_date)
                else:
                    self.db_handler.register_staff_to_shift(shift_id, staff_id, mysql_date)
                self.logger.write_to_log('staff registered to shift', 'model')
                result = True

            return result
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staff_registered_shifts(self, staff_id):
        try:
            self.logger.write_to_log('staff registered shifts requested', 'model')

            shifts = self.db_handler.get_staff_registered_shifts_by_id_extended(staff_id)

            self.logger.write_to_log('staff registered shifts got', 'model')
            return shifts
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staff_registered_shift_details(self, shift_registration_id, staff_id):
        try:
            self.logger.write_to_log('registered shift details requested', 'model')

            shift = self.db_handler.get_staff_registered_shifts_by_shift_registration_id_extended(shift_registration_id, staff_id)

            self.logger.write_to_log('registered shift details got', 'model')
            return shift
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def cancel_shift_registration(self, shift_reg_id, staff_id):
        try:
            self.logger.write_to_log(f'requested canceling of shift registration for user {staff_id}', 'model')

            date = datetime.now()
            mysql_date = f'{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:00'

            self.db_handler.cancel_shift_registration_for_user(shift_reg_id, staff_id, mysql_date)

            self.logger.write_to_log(f'shift registration for user {staff_id} canceled', 'model')
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staffs_shift_registrations(self, staff_id):
        try:
            self.logger.write_to_log('requested staffs all shift registrations', 'model')
            return self.db_handler.get_staffs_shift_registrations(staff_id)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def check_in_to_shift(self, shift_reg_id, staff_id):
        """
        Checks if user can already check in to the shift
        :param shift_reg_id: shift registration id
        :param staff_id: staff telegram id
        :return: 1 if checked in to shift, 0 if not
        """
        try:
            self.logger.write_to_log(f'requested check in to shift {shift_reg_id}', 'model')
            date = datetime.now()
            mysql_date = f'{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:00'
            dates = self.db_handler.get_event_date_by_shift_registration_id_and_staff_id(shift_reg_id, staff_id)
            status = 0

            diff = dates[2] - date

            if diff.days == 0:
                if (diff.seconds / 60) < config.CHECK_IN_ALLOWED_BEFORE_SHIFT_MIN:
                    self.db_handler.check_in_to_shift(mysql_date, shift_reg_id)
                    self.logger.write_to_log(f'check in entered for shift {shift_reg_id}', 'model')
                    status = 1
                else:
                    status = 0
                    self.logger.write_to_log(f'check in is not set to shift {shift_reg_id}', 'model')
            else:
                status = 0
                self.logger.write_to_log(f'check in is not set to shift {shift_reg_id}', 'model')

            return status
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def is_staff_supervisor_on_shift(self, shift_reg_id, staff_id):
        """
        Checks if user is supervisor on shift
        :param shift_reg_id: shift registration id
        :param staff_id: staff telegram id
        :return: true if staff is suprvisor on shift, false if not
        """
        try:
            res = False
            self.logger.write_to_log(f'requested shift supervisor status', 'model')
            shift_registration = self.db_handler.get_event_date_by_shift_registration_id_and_staff_id(shift_reg_id, staff_id)

            if shift_registration is not None:
                event_data = self.db_handler.get_shift_extended_info_by_id(shift_registration[0])

                if str(event_data[5]) == str(staff_id):
                    res = True

                self.logger.write_to_log(f'got shift supervisor status', 'model')

            return res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def check_out_off_shift(self, staff_id, shift_reg_id):
        """
        Checks if check out is made not earlier than event ends
        :param staff_id: staff telegram id
        :param shift_reg_id: shift request id
        :return: true if event is ended already, false if not
        """
        try:
            res = False

            date = datetime.now()
            mysql_date = f'{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:00'
            dates = self.db_handler.get_event_date_by_shift_registration_id_and_staff_id(shift_reg_id, staff_id)

            diff = dates[3] - date
            shift_reg = self.db_handler.get_shift_registration_by_shift_reg_id(shift_reg_id)

            if diff.days <= 0 and diff.seconds >= 0:
                res = True

                if shift_reg[6] is not None:
                    mysql_date = f'{shift_reg[6].year}-{shift_reg[6].month}-{shift_reg[6].day} {shift_reg[6].hour}:{shift_reg[6].minute}:00'

                self.db_handler.check_out_off_shift(shift_reg_id, mysql_date)
            return res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staff_registered_to_shift(self, shift_id):
        """
        Returns list of staff registered for shift
        :param shift_id: shift id
        :return: set of list of staff registered, and id of supervisor
        """
        try:
            self.logger.write_to_log(f'requested staff list for shift {shift_id}', 'model')

            shift_list = self.db_handler.get_staff_on_shift(shift_id)
            supervisor = self.db_handler.get_supervisor_on_shift(shift_id)

            self.logger.write_to_log(f'got staff list for shift {shift_id}', 'model')
            return shift_list, supervisor
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staff_list_to_set_rating(self, shift_id):
        """
        Returns list of staff worked on shift, for setting rating, if event is ended
        :param shift_id: shift id
        :return: list of staff if event is over, empty list, or 0 if there's too early
        """
        try:
            self.logger.write_to_log('requested staff list for setting rating', 'model')

            res = []
            status = 1

            shift = self.db_handler.get_shift_extended_info_by_id(shift_id)
            date = datetime.now()

            diff = date-shift[9]

            if diff.days >= 0 and diff.seconds >= 0:
                staff_on_shift = self.db_handler.get_staff_on_shift(shift_id)

                for sos in staff_on_shift:
                    rating = self.db_handler.get_staff_rating_for_shift(sos[0], shift_id)
                    if rating[0] is None or rating[0] == '':
                        res.append(sos)

                self.logger.write_to_log('got staff list for setting rating', 'model')
            else:
                status = 0
                self.logger.write_to_log('staff list for setting rating was not formed', 'model')

            if status == 1:
                return res
            else:
                return status
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def set_staff_rating_for_shift(self, staff_id, shift_id, rating):
        """
        Setting rating to staff
        :param staff_id: staff telegram id
        :param shift_id: shift id
        :param rating: rating of staff from 1 to 5
        :return: None
        """
        try:
            self.db_handler.set_staff_rating_for_shift(staff_id, shift_id, rating)
            self.logger.write_to_log(f'rating set to user {staff_id} for shift {shift_id}', 'model')

            sh_reg = self.db_handler.get_shift_registration_by_staff_id_and_shift_id(staff_id, shift_id)

            self.check_out_off_shift(staff_id, sh_reg[0])
            self.calculate_payment_for_shift(shift_id, staff_id)
            self.update_staff_rating(staff_id)

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def calculate_payment_for_shift(self, shift_id, staff_id):
        try:
            staff = self.db_handler.get_staff_by_id(staff_id)
            shift_reg = self.db_handler.get_shift_registration_by_staff_id_and_shift_id(staff_id, shift_id)

            on_shift = shift_reg[6] - shift_reg[5]
            payment = ((on_shift.days * 24) + (on_shift.seconds / 3600)) * float(staff[10])
            payment += round((payment / 100) * (float(shift_reg[7]) * 3), 2)    # bonus for rating

            self.db_handler.set_payment_for_shift(shift_id, staff_id, payment)
            self.logger.write_to_log('payment for shift calculated and set to user', 'model')
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def update_staff_rating(self, staff_id):
        try:
            ratings = self.db_handler.get_staff_shift_ratings(staff_id)

            rating = 0

            for shift_reg in ratings:
                rating += float(shift_reg[7])

            rating /= len(ratings)

            self.db_handler.update_staff_rating_and_events_count(staff_id, rating, len(ratings))
            self.logger.write_to_log(f'staff {staff_id} events number were updated', 'model')
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')