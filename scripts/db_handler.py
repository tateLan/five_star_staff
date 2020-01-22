import mysql.connector
import config
from datetime import datetime


class DbHandler:
    def __init__(self):
        """
        Method creates db connection
        :return:
        """
        self.connect = mysql.connector.connect(
            host='vps721220.ovh.net',
            user='five_star',
            passwd='qualityisma1n',
            database='five_star_db',
            auth_plugin='mysql_native_password'
        )
        self.curs = self.connect.cursor(buffered=True)

        self.session_time_alive = datetime.now()

        print('db connected successfully!')

    def check_session_time_alive(func):
        """
        Decorator which tracks connection timeout
        :param func: function needed to be wrapped
        :return: wrapped function
        """
        def inner_func(self, *args):
            """
            Wraps function to check connection timeout
            :param args: arguments of function
            :return: None
            """
            now = datetime.now()
            hours = (now - self.session_time_alive).seconds / 3600

            if hours >= 4.9:
                self.connect = mysql.connector.connect(
                    host='vps721220.ovh.net',
                    user='five_star',
                    passwd='qualityisma1n',
                    database='five_star_db',
                    auth_plugin='mysql_native_password'
                )
                self.curs = self.connect.cursor(buffered=True)
                self.session_time_alive = datetime.now()
            if args.__len__() == 0:
                return func(self)
            else:
                return func(self, args)

        return inner_func

    @check_session_time_alive
    def get_user_by_telegram_id(self, *args):
        """
        Method requests info about user by his telegram id, and returns first and last name if exists
        of 0 otherwise
        :param id: user telegram id
        :return: first and last name of 0 if not exists
        """
        id = args[0][0]
        q = f'select first_name, last_name from staff where id={id};'

        self.curs.execute(q)

        res = self.curs.fetchone()
        if type(res) is type(None):
            return '0'
        else:
            return res

    @check_session_time_alive
    def set_user_telegram_id(self, *args):
        """
        Method adding users telegram id to table staff
        :param user_id: user telegram id
        """
        user_id = args[0][0]
        q = f'INSERT INTO five_star_db.staff (id, current_rating, general_rating,' \
            f' events_done, rate) VALUES ({user_id}, 0, 0, 0, ' \
            f'{config.START_RATE})'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def set_user_first_name(self, *args):
        """
        Method updates staff account with first name
        :param user_id: user telegram id
        :param name: first name of user
        """
        user_id, name = args[0]
        q = f"UPDATE five_star_db.staff SET first_name = '{name}' WHERE (id = '{user_id}');"

        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def set_user_middle_name(self, *args):
        """
        Method updates staff account with middle name
        :param user_id: user telegram id
        :param m_name: user middle name
        """
        user_id, m_name = args[0]
        q = f"UPDATE five_star_db.staff SET middle_name = '{m_name}' WHERE (id = '{user_id}');"

        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def set_user_last_name(self, *args):
        """
        Method updates staff account with last name
        :param user_id: user telegram id
        :param l_name: last name
        """
        user_id, l_name = args[0]
        q = f"UPDATE five_star_db.staff SET last_name = '{l_name}' WHERE (id = '{user_id}');"

        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def set_user_role(self, *args):
        """
        Inserts role into users account
        :param user_id: user telegram id
        :param role_id: id of role
        :return:
        """
        user_id, role_id = args[0]
        q = f"UPDATE five_star_db.staff SET staff_role = {role_id} WHERE (id ={user_id});"
        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def set_user_qualification(self, *args):
        """
        Updates user qualification
        :param user_id: user telegram id
        :param role_quali: qualification code
        :return: None
        """
        user_id, role_quali = args[0]
        q = f'UPDATE five_star_db.staff SET qualification = {role_quali} WHERE (id = {user_id});'
        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_roles_list(self):
        """
        Returns list of roles
        :return:  set of roles
        """
        q = "select * from roles where name_role != 'не підтверджено';"
        self.curs.execute(q)
        res = self.curs.fetchall()

        return res

    @check_session_time_alive
    def get_role_by_id(self, *args):
        """
        Returns role by its id
        :param role_id: id of role
        :return: role instance
        """
        role_id = args[0][0]
        q = f'select * from roles where id_role = {role_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_not_set_role(self):
        """
        Returns id of 'not set' role
        :return: role id
        """
        cursor = self.connect.cursor()
        q = "select id_role from roles where name_role = 'не підтверджено';"
        cursor.execute(q)
        res = cursor.fetchone()

        return res[0]

    @check_session_time_alive
    def left_role_approving_request(self, *args):
        """
        Creates role request
        :param user_id: user telegram id who left request
        :param role_id: id of reole, needed to approve
        :return: None
        """
        user_id, role_id = args[0]
        cursor = self.connect.cursor()
        q = f"INSERT INTO five_star_db.role_confirmation (staff_id, requested_role, confirmed) VALUES ({user_id}, {role_id}, 0);"
        cursor.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_qualifications_list(self):
        """
        Returns id's of qualifications, except 'not set'
        :return: id of qualifications
        """
        cursor = self.connect.cursor()
        q = "select * from qualification where degree != 'не підтверджено';"
        cursor.execute(q)
        res = cursor.fetchall()

        return res

    @check_session_time_alive
    def get_not_set_qualification(self):
        """
        Returns id 'not set' qualification
        :return: id of 'not 'set'
        """
        cursor = self.connect.cursor()
        q = "select id from qualification where degree = 'не підтверджено';"
        cursor.execute(q)
        res = cursor.fetchone()

        return res[0]

    @check_session_time_alive
    def left_qualification_approving_request(self, *args):
        """
        Creates request to approve user qualification
        :param user_id: user telegram id
        :param quali_id: id of  qualification
        :return: None
        """
        user_id, quali_id = args[0]
        cursor = self.connect.cursor()
        q = f"INSERT INTO five_star_db.qualification_confirmation (staff_id, requested_qualification, confirmed) VALUES ({user_id}, {quali_id}, 0);"
        cursor.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_user_role_by_id(self, *args):
        """
        Returns information about user role
        :param user_id: user telegram id
        :return: set of role id and role name
        """
        user_id = args[0][0]
        q = f'select roles.id_role, roles.name_role from staff left join roles on staff.staff_role = roles.id_role where id = {user_id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_unaccepted_role_requests(self):
        """
        Returns unaccepted role requests
        :return: unaccepted requests
        """
        self.connect.commit()
        q = 'select * from role_confirmation where confirmed = 0'

        self.curs.execute(q)
        return self.curs.fetchall()

    @check_session_time_alive
    def get_unaccepted_qualification_requests(self):
        """
        Returns unaccepted qualification requests
        :return: unaccepted qualification requests
        """
        self.connect.commit()
        q = 'select * from qualification_confirmation where confirmed = 0'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_role_request_status(self, *args):
        """
        Returns user's role request status
        :param user_id: user telegram id
        :return: status of request
        """
        user_id = args[0][0]
        self.connect.commit()
        q = f'select confirmed from role_confirmation where staff_id = {user_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_qualification_request_status(self, *args):
        """
        Returns user's qualification request status
        :param user_id: user telegram id
        :return: status of request
        """
        user_id = args[0][0]
        self.connect.commit()
        q = f'select confirmed from qualification_confirmation where staff_id = {user_id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_user_name_by_id(self, *args):
        """
        returns users full name by telegram id
        :param user_id: user telegram id
        :return: set of first name, middle name, last name
        """
        user_id = args[0][0]
        q = f'select first_name, middle_name, last_name from staff where id = {user_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def accept_role_request(self, *args):
        """
        updates table 'role_requests'. confirms requested role
        :param request_id: id of request
        :param admin_id: telegram id of user whicj confirms (admin of manager)
        :param date: date of confirmation
        :return: None
        """
        request_id, admin_id, date = args[0]
        q = f"update role_confirmation set date_confirmed = '{date}', confirmed_by = {admin_id}, confirmed = 1 where id = {request_id};"

        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def update_staff_role(self, *args):
        """
        Updates user role in staff table
        :param user_id:  user telegram id
        :param role_id: role id
        :return:  None
        """
        user_id ,role_id = args[0]
        q = f'update staff set staff_role = {role_id} where id = {user_id};'

        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def get_role_id_from_role_request(self, *args):
        """
        Returns role id, requested by user
        :param request: id of role request
        :return: role id
        """
        request = args[0][0]
        q = f'select requested_role from role_confirmation where staff_id = {request};'

        self.curs.execute(q)

        return self.curs.fetchone()
