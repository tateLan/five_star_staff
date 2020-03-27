import calendar
import db_handler as db
from datetime import datetime
import config
from datetime import timedelta
from emoji import emojize
import geopy.distance
import math
import os
import sys
import xlsxwriter as xlw
from setuptools.command.setopt import setopt


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

            managers_main_menu_ids = []

            for manager in self.get_managers_list():
                managers_main_menu_ids.append((manager, self.get_staff_main_menu_msg_id(manager[0])))

            messages = self.notifier.notify_manager_about_role_request(managers_main_menu_ids)

            for staff_id, msg_id in messages:
                self.update_staff_main_menu_id(staff_id, msg_id)


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

            managers_main_menu_ids = []

            for manager in self.get_managers_list():
                managers_main_menu_ids.append((manager, self.get_staff_main_menu_msg_id(manager[0])))

            messages = self.notifier.notify_manager_about_qualification_request(managers_main_menu_ids)

            for staff_id, msg_id in messages:
                self.update_staff_main_menu_id(staff_id, msg_id)

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

            price += price * 0.4

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
        :return: true if staff is supervisor on shift, false if not
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

    def close_shift(self, shift_id, supervisor_id):
        """
        Checks if all conditions satisfied, for ending shift
        :param shift_id: id of shift
        :param supervisor_id: telegram id of supervisor
        :return: False if its too early to close shift, True, if shift is ended
        """
        try:
            res = False
            event = self.db_handler.get_shift_extended_info_by_id(shift_id)
            staff_on_shift = self.db_handler.get_staff_on_shift_for_closing(shift_id)
            staff_all_set_up = 0
            sh_reg = self.db_handler.get_shift_registration_by_staff_id_and_shift_id(supervisor_id, shift_id)

            diff = datetime.now() - event[9]

            if diff.days >= 0 and diff.seconds >= 0:
                for staff in staff_on_shift:
                    if str(staff[0]) != str(supervisor_id):
                        if staff[1] is not None and staff[2] is not None:
                            staff_all_set_up += 1

                if staff_all_set_up == len(staff_on_shift)-1:   # supervisor anyway is on shift
                    res = True
            else:
                res = False    # too early

            if res:
                self.check_out_off_shift(supervisor_id, sh_reg[0])
                self.db_handler.update_shift_status(shift_id)

            return res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staff_ended_shifts(self, staff_id, page):
        """
        Returns n of ended shifts, by staff telegram id.
            N is set up in config file by STAT_ITEMS_ON_ONE_PAGE
        :param staff_id: staff telegram id
        :param page: page of results
        :return: set of overall number of pages, and list of ended shifts
        """
        try:
            overall_shifts = self.db_handler.get_ended_staff_shifts(staff_id)
            res = []
            size = config.STAT_ITEMS_ON_ONE_PAGE

            res = overall_shifts[page*size : (page*size) + size]
            self.logger.write_to_log('list of ended shifts of staff is here', str(staff_id))

            return math.ceil(len(overall_shifts) / size), res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_all_ended_shifts_for_manager_stat(self, page):
        """
        Returns n of ended shifts, by staff telegram id.
            N is set up in config file by STAT_ITEMS_ON_ONE_PAGE
        :param page: page of results
        :return: set of overall number of pages, and list of ended shifts
        """
        try:
            overall_shifts = self.db_handler.get_all_ended_shifts()
            res = []
            size = config.STAT_ITEMS_ON_ONE_PAGE

            res = overall_shifts[page * size: (page * size) + size]
            self.logger.write_to_log('list of ended shifts of staff is here', 'model')

            return math.ceil(len(overall_shifts) / size), res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_shift_report_info_waiter(self, sh_reg_id, is_manager_called=False):
        """
        Formats waiter part of shift report in archive
        :param sh_reg_id: shift registration id
        :param is_manager_called: indicates if called by waiter or manager
        :return: string with personal waiter info about shift
        """
        try:
            staff_id = self.db_handler.get_shift_registration_by_shift_reg_id(sh_reg_id)[2]
            is_supervisor = self.is_staff_supervisor_on_shift(sh_reg_id, staff_id)
            msg = ''

            if not is_manager_called:
                if is_supervisor:
                    msg += f'{emojize(" :cop:", use_aliases=True)}Ви були головним на цій зміні!\n'

            check_in, check_out, rating, payment = self.db_handler.get_waiter_personal_info_from_shift_registration(sh_reg_id)

            msg += f'{emojize(" :heavy_plus_sign:", use_aliases=True)}check-in: {check_in if check_in is not None and check_in !="" else "Інформація тимчасово відсутня"}\n'\
                   f'{emojize(" :heavy_minus_sign:", use_aliases=True)}check-out: {check_out if check_out is not None and check_out !="" else "Інформація тимчасово відсутня"}\n' \
                   f'{emojize(" :hourglass:", use_aliases=True)}на зміні: {check_out - check_in}\n'\
                   f'{emojize(" :chart_with_upwards_trend:", use_aliases=True)}Рейтинг: {rating if rating is not None and rating !="" else "Інформація тимчасово відсутня"}\n'\
                   f'{emojize(" :moneybag:", use_aliases=True)}Нараховано: *{payment if payment is not None and payment !="" else "Інформація тимчасово відсутня"}*\n'

            return msg
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_shift_report_info_manager(self, shift_id):
        """
        Generates manager string for shift archive, about shift
        :param shift_id: shift id
        :return: string with manager version of information about string
        """
        try:
            _, _, pro, mid, beg, supervisor_id, _, _, _, _, _, _, _, _, price, curr_id  = self.db_handler.get_shift_extended_info_by_id(shift_id)
            curr_name = [x[1] for x in self.db_handler.get_currencies() if x[0] == curr_id][0]
            shift_registrations = self.db_handler.get_shift_registrations_by_shift_id(shift_id)

            res = f'На зміну було зареєстровано:\n' \
                  f'{emojize(":full_moon:", use_aliases=True)}Професіоналів: {pro}\n' \
                  f'{emojize(":last_quarter_moon:", use_aliases=True)}Середнього рівня: {mid}\n' \
                  f'{emojize(":new_moon:", use_aliases=True)}Початківців: {beg}\n' \
                  f'{emojize(":moneybag:", use_aliases=True)}Ціна за подію: {price} {curr_name}\n' \
                  f'{"-" * 20}\n' \
                  f'Статистика працівників:\n' \
                  f'{"-" * 20}\n'

            for sh_reg in shift_registrations:
                usr = self.db_handler.get_staff_by_id(sh_reg[2])
                staff_str = f'{usr[3]} {usr[1]} {usr[2]}\n'
                res += staff_str

                if str(usr[0]) == str(supervisor_id):
                    res += f'{emojize(":cop:", use_aliases=True)}Головний на зміні\n'

                res += self.get_shift_report_info_waiter(sh_reg[0], is_manager_called=True)
                res += f'{"-" * 20}\n'

            return res

        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_shift_report_general_info(self, shift_id):
        """
        Formats string with general information about shift
        :param shift_id: shift id
        :return: string with general information about shift
        """
        try:
            title, date_starts, date_ends, guests, type_event, class_event = self.db_handler.get_shift_general_info_for_archive(shift_id)

            msg = f'{title}\n' \
                  f'{"-" * 20}\n' \
                  f'{emojize(" :clock4:", use_aliases=True)}Дата початку: {date_starts}\n' \
                  f'{emojize(" :clock430:", use_aliases=True)}Дата закінчення: {date_ends}\n' \
                  f'{emojize(" :tophat:", use_aliases=True)}Кількість гостей :{guests}\n'\
                  f'{emojize(" :abc:", use_aliases=True)}Тип події: {type_event}\n' \
                  f'{emojize(" :top:", use_aliases=True)}Клас події :{class_event}\n'

            self.logger.write_to_log('shift general info got', 'model')

            return msg
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_shift_report_info(self, shift_id=0, shift_reg_id=0):
        """
        Generates message for displaying shift in archive, depends of arguments which where passed in
        :param shift_id: shift id, if its for waiter, by default 0
        :param shift_reg_id: shift registration id, if its for manager by default 0
        :return: string with all needed information about shift
        """
        try:
            personal_data = f'{"-" * 20}\n'
            general_shift_info = []

            if shift_id == 0:  # waiter
                shift_id = self.db_handler.get_shift_registration_by_shift_reg_id(shift_reg_id)[1]
                personal_data += self.get_shift_report_info_waiter(shift_reg_id)
            elif shift_reg_id == 0:  # manager
                personal_data += self.get_shift_report_info_manager(shift_id)

            general_shift_info = self.get_shift_report_general_info(shift_id)

            msg = general_shift_info + personal_data

            return msg
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_month_staff_worked(self, staff_id, page):
        """
        Generates list of months staff worked by pages. Page contains N months,
            N is STAT_ITEMS_ON_ONE_PAGE from config
        :param staff_id: staff telegram id
        :return: list of strings with month name and year staff worked
        """
        try:
            registrations = self.db_handler.get_staff_shift_registrations_ended(staff_id)
            month_list = []

            for reg in registrations:
                if (reg[5].month, reg[5].year) not in month_list:
                    month_list.append((reg[5].month, reg[5].year))

            size = config.STAT_ITEMS_ON_ONE_PAGE
            res = month_list[page * size: (page * size) + size]

            return math.ceil(len(month_list) / size), res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staff_financial_report_for_month(self,staff_id, period):
        """
        Gets staff worked shift for specified month
        :param staff_id: staff telegram id
        :param period: string formated 'month-year'
        :return: list of sets which contains data about ended shift
        """
        try:
            month = int(period.split('-')[0])
            year = int(period.split('-')[1])

            start_date = datetime(year, month, 1)
            end_date = datetime(year, month, calendar.monthrange(year, month)[1])

            registrations = self.db_handler.get_shift_registrations_for_period(staff_id, start_date, end_date)
            res = []
            i = 1

            for reg in registrations:
                res.append((i, reg[2], reg[3], reg[4], reg[4]-reg[3], reg[5], reg[6]))
                i += 1

            return res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def generate_waiter_financial_report_excel_file(self, staff_info, period, month_report, path):
        """
        Creates excel worksheet with financial report for waiter
        :param staff_info: list with staff infomation
        :param period: string with period of report formated 'month-year'
        :param month_report: list woth report
        :param path: path to file, needed to create
        :return: None
        """
        try:
            workbook = xlw.Workbook(path)
            worksheet = workbook.add_worksheet()

            file_header_format = workbook.add_format({
                'font_size':20,
                'align': 'center',
                'valign': 'vcenter'
            })
            table_header_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 12,
                'fg_color': '#C0C0C0'})
            cell_format = workbook.add_format({
                'font_size': 12,
                'align':'center',
                'valign':'vcenter'
            })
            sum_format = workbook.add_format({
                'font_size': 12,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': '#99FF99'
            })

            worksheet.set_column('A:A', 10)
            worksheet.set_column('B:B', 30)
            worksheet.set_column('C:C', 20)
            worksheet.set_column('D:D', 20)
            worksheet.set_column('E:E', 20)
            worksheet.set_column('F:F', 10)
            worksheet.set_column('G:G', 15)

            worksheet.merge_range('A1:G2', f'{staff_info[3]} {staff_info[1]} {period}', file_header_format)

            row = 4
            column = 0

            for line in month_report:
                for item in line:
                    if row == 4:
                        worksheet.write(row, column, item.__str__(), table_header_format)
                    else:
                        if month_report.index(line) == len(month_report)-1 and line.index(item) == len(line)-1:
                            worksheet.write(row, column, item.__str__(), sum_format)
                        else:
                            worksheet.write(row, column, item.__str__(), cell_format)
                    column += 1
                row += 1
                column = 0

            workbook.close()
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_waiter_excel_financial_report_path(self, staff_id, period):
        """
        Returns path of excel file which contains month report
        :param staff_id: staff telegram id
        :param period: string with period, formated 'month-year'
        :return: string with excel workshhet path
        """
        try:
            headers = ('№п/п', 'Назва події', 'Check-in', 'Check-out', 'Час на зміні', 'Рейтинг', 'Нараховано')
            path = f'{config.WORKING_DIR}/user_reports/{staff_id}_{period}.xlsx'

            if os.path.isfile(path):
                os.remove(path)

            staff = self.get_staff_by_id(staff_id)
            report = self.get_staff_financial_report_for_month(staff_id, period)
            report_with_headers = [headers]
            sum_for_month = sum([x[6] for x in report])

            for rep in report:
                report_with_headers.append(rep)

            report_with_headers.append(('','','','','','',sum_for_month))

            self.generate_waiter_financial_report_excel_file(staff, period, report_with_headers, path)
            self.logger.write_to_log('excel file with month report generated', 'model')

            return path
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_month_all_staff_worked(self, page):
        """
        Generates list of months when any staff worked
        :param page: page of results
        :return: set, consists of (overall number of pages, list of periods)
        """
        try:
             registrations = self.db_handler.get_ended_shift_registrations()

             month_list = []

             for reg in registrations:
                 if (reg[5].month, reg[5].year) not in month_list:
                     month_list.append((reg[5].month, reg[5].year))

             size = config.STAT_ITEMS_ON_ONE_PAGE
             res = month_list[page * size: (page * size) + size]

             self.logger.write_to_log('got list of month all staff worked', 'model')

             return math.ceil(len(month_list) / size), res
        except Exception as err:
             method_name = sys._getframe().f_code.co_name

             self.logger.write_to_log('exception', 'model')
             self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_general_financial_report_for_month(self, period):
        """
        Gets list of sets, with report about month
        :param period: string with period, formated like 'month-year'
        :return: list of sets, which formated like (id of shift, list with shift registrations to that shift)
        """
        try:
            month = int(period.split('-')[0])
            year = int(period.split('-')[1])
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month, calendar.monthrange(year, month)[1])

            res = []

            worked_shifts = [x[0] for x in self.db_handler.get_ended_shift_ids_in_period(start_date, end_date)]   # to unpack sets, cuz they're formated like (value,)

            for shift in worked_shifts:
                res.append((shift, self.db_handler.get_ended_registrations_by_shift_id(shift)))

            self.logger.write_to_log(f'overall financial report for period {period} get', 'model')

            return res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_shift_text_fin_report(self, shift):
        """
        Generates short information about shift for manager financial report
        :param shift: shift id
        :return: string with short shift report
        """
        try:
            shift_info = shift[1]
            sum_to_pay = 0
            event_info = self.get_shift_extended_info_by_id(shift[0])

            for sh_reg in shift_info:
                sum_to_pay += float(sh_reg[6])

            msg = f'назва події: {event_info[6]}\n' \
                  f'id зміни: {str(shift[0])}\n' \
                  f'{emojize(" :busts_in_silhouette:", use_aliases=True)}працівників на зміні: {len(shift_info)}\n' \
                  f'{emojize(" :heavy_plus_sign:", use_aliases=True)}ціна події: {event_info[14]}\n' \
                  f'{emojize(" :heavy_minus_sign:", use_aliases=True)}загальна сума виплат: {sum_to_pay}\n' \
                  f'{emojize(" :moneybag:", use_aliases=True)}залишок після виплати зп: *{float(event_info[14]) - sum_to_pay}*\n'

            return msg, sum_to_pay, event_info[14]
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_short_text_financial_report_for_month(self, period):
        """
        Generates short text financial report for month
        :param period: period of report
        :return: string with report
        """
        try:
            report = self.get_general_financial_report_for_month(period)

            overall_income = 0
            overall_outcome = 0

            res = f'{"-" * 20}\n' \
                  f'Відпрацьовано змін:{len(report)}\n'
            res += f'{"-" * 20}\n'

            for item in report:
                shift_report, outcome, income = self.get_shift_text_fin_report(item)

                overall_income += float(income)
                overall_outcome += float(outcome)

                res += shift_report
                res += f'{"-" * 20}\n'

            res += f'{emojize(" :heavy_plus_sign:", use_aliases=True)}Загальний дохід: {overall_income}\n' \
                   f'{emojize(" :heavy_minus_sign:", use_aliases=True)}Загальні витрати: {overall_outcome}\n' \
                   f'{emojize(" :moneybag:", use_aliases=True)}Прибуток: *{overall_income - overall_outcome}*\n'
            return res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_full_month_financial_report(self, period):
        """
        Generates all needed data about shift, to write em to excel file with report
        :param period: string with period
        :return: list of sets about shift (dictionary with shift data,
                                           list with headers about staff,
                                           list with staff shift registration data
                                           set with overall outcome, profit)
        """
        try:
            report = self.get_general_financial_report_for_month(period)
            res = []

            for shift in report:
                shift_ext = self.get_shift_extended_info_by_id(shift[0])
                shift_info = {'id:': shift[0],
                              'назва:': shift_ext[6],
                              'Дата початку:': shift_ext[8],
                              'Дата закінчення: ': shift_ext[9],
                              'Ціна:': shift_ext[14],
                              'Клас: ': [x[1] for x in self.get_event_types_list() if x[0] == shift_ext[11]][0],
                              'Тип: ': [x[1] for x in self.get_event_classes_list() if x[0] == shift_ext[12]][0]}
                staff_headers = ['Прізвище', 'Ім\'я', 'По-батькові', 'Посада', 'Кваліфікація',
                                 'Check-in', 'Check-out', 'На зміні', 'Рейтинг', 'Нараховано']
                staff_info = []
                overall_outcome = 0

                for sh_reg in shift[1]:
                    staff_ext = self.get_staff_by_id(sh_reg[1])
                    temp_staff = [staff_ext[3], staff_ext[1], staff_ext[2],
                                  self.get_role_by_id(staff_ext[4])[1],
                                  self.get_qualification_by_id(staff_ext[5])[1],
                                  sh_reg[3], sh_reg[4], (sh_reg[4] - sh_reg[3]), sh_reg[5],
                                  sh_reg[6]]

                    overall_outcome += float(sh_reg[6])
                    staff_info.append(temp_staff)

                res.append((shift_info, staff_headers, staff_info, (overall_outcome, float(shift_ext[14]) - overall_outcome)))
            return res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def generate_detailed_manager_month_fin_report_excel(self, report, path, period):
        try:
            workbook = xlw.Workbook(path)
            worksheet = workbook.add_worksheet()

            file_header_format = workbook.add_format({
                'bold': 1,
                'font_size': 20,
                'align': 'center',
                'valign': 'vcenter'
            })
            shift_header_format = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 18,
                'fg_color': '#f6f9d4'
            })
            staff_header_format = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 18,
                'fg_color': '#e0c2cd'
            })
            table_header_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 12,
                'fg_color': '#C0C0C0'})
            cell_format = workbook.add_format({
                'font_size': 12,
                'align': 'center',
                'valign': 'vcenter'
            })
            pre_sum_to_pay_format = workbook.add_format({
                'top': 1,
                'align': 'right'
            })
            sum_to_pay_format = workbook.add_format({
                'font_size': 12,
                'align': 'center',
                'valign': 'vcenter',
                'top': 1,
                'fg_color': '#dde8cb'
            })
            pre_sum_of_profit_format = workbook.add_format({
                'align': 'right'
            })
            sum_of_profit_format = workbook.add_format({
                'font_size': 12,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': '#afd095'
            })

            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 20)
            worksheet.set_column('D:D', 20)
            worksheet.set_column('E:E', 20)
            worksheet.set_column('F:F', 20)
            worksheet.set_column('G:G', 20)
            worksheet.set_column('H:H', 20)
            worksheet.set_column('I:I', 20)
            worksheet.set_column('J:J', 20)

            worksheet.merge_range('A1:J3', f'Звіт за {period}', file_header_format)

            row = 7
            col = 0
            overall_outcome = 0
            overall_income = 0

            for shift in report:
                shift_info = list(shift[0].items())
                staff_headers = shift[1]
                staff_info = shift[2]
                final_numbers = shift[3]

                worksheet.merge_range(f'A{row}:J{row}', f'Зміна {shift_info[0][0]} {shift_info[0][1]}'
                                                        f' {shift_info[1][0]} {shift_info[1][1]}', shift_header_format)

                row += 1
                for i in range(2, len(shift_info)):
                    worksheet.write(row, 0, str(shift_info[i][0]))
                    worksheet.write(row, 1, str(shift_info[i][1]))
                    row += 1

                row += 2
                worksheet.merge_range(f'A{row}:J{row}', f'Працівники:', staff_header_format)

                for i in range(len(staff_headers)):
                    worksheet.write(row, i, str(staff_headers[i]), table_header_format)
                row += 1

                for worker in staff_info:
                    for i in range(len(worker)):
                        worksheet.write(row, i, str(worker[i]), cell_format)
                    row += 1

                row += 1
                worksheet.merge_range(f'A{row}:I{row}', 'Разом до виплати:', pre_sum_to_pay_format)
                worksheet.write(row-1, 9, str(final_numbers[0]), sum_to_pay_format)
                row += 1
                worksheet.merge_range(f'A{row}:I{row}', 'Прибуток:', pre_sum_of_profit_format)
                worksheet.write(row-1, 9, str(final_numbers[1]), sum_of_profit_format)

                overall_outcome += float(final_numbers[0])
                overall_income += float(final_numbers[1])

                row += 3
            worksheet.write(row, 0, 'Загальні витрати: ')
            worksheet.write(row, 1, overall_outcome, sum_to_pay_format)

            worksheet.write(row+1, 0, 'Загальний дохід: ')
            worksheet.write(row+1, 1, overall_income, sum_of_profit_format)




            workbook.close()
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_manager_excel_financial_report_path(self, period):
        try:
            path = f'{config.WORKING_DIR}/user_reports/detailed_report_{period}.xlsx'

            if os.path.isfile(path):
                os.remove(path)

            report = self.get_full_month_financial_report(period)

            self.generate_detailed_manager_month_fin_report_excel(report, path, period)

            self.logger.write_to_log('detailed month fin report in excel generated', 'model')

            return path
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staff_ever_worked(self, page):
        """
        Returns list of staff ever worked(have ended shift)
        :param page: int number of page
        :return: list of staff
        """
        try:
            self.logger.write_to_log('staff ever worked requested', 'model')

            staff_list = self.db_handler.get_staff_ever_worked()
            size = config.STAT_ITEMS_ON_ONE_PAGE

            res = staff_list[page * size: (page * size) + size]

            return math.ceil(len(staff_list) / size), res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_upcoming_shifts_for_notifier(self):
        try:
            self.logger.write_to_log('list of upcoming shift registrations requested', 'model')

            return self.db_handler.get_upcoming_shifts_for_notifier()
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def update_staff_main_menu_id(self, staff_id, menu_msg_id):
        """
        Updates data about main menu for each user
        :param staff_id: staff telegram id
        :param menu_msg_id: message id of new main menu message
        :return: None
        """
        try:
            flag = True if self.db_handler.get_staff_main_menu_msg_id(staff_id) is not None else False

            if flag:
                self.db_handler.update_staff_main_menu_msg_id(staff_id, menu_msg_id)
            else:
                self.db_handler.insert_staff_main_menu_msg_id(staff_id, menu_msg_id)

            self.logger.write_to_log('main menu message id updated', 'model')
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_staff_main_menu_msg_id(self, staff_id):
        """
        Returns message id of last main menu message
        :param staff_id: staff telegram id
        :return: id of message
        """
        try:
            res = self.db_handler.get_staff_main_menu_msg_id(staff_id)

            self.logger.write_to_log('main menu message id got', 'model')

            return res[1]
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_managers_list(self):
        """
        Returns list of manager accounts
        :return: list of manager staff info
        """
        try:
            role_id = [x[0] for x in self.db_handler.get_roles_list() if x[1] == 'менеджер'][0]
            staff_by_role = self.db_handler.get_all_staff_by_role_id(role_id)

            self.logger.write_to_log('managers list got', 'model')

            return staff_by_role
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')

    def get_user_qualification_by_id(self, staff_id):
        try:
            staff = self.db_handler.get_staff_by_id(staff_id)
            qualification = self.get_qualification_by_id(staff[5])[1]

            return qualification
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'model')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'model')