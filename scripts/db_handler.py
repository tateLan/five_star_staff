import mysql.connector
import config


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
        self.curs = self.connect.cursor()
        self.curs.execute('set global wait_timeout=18000')  # 5 hrs timeout
        self.curs.execute('set global interactive_timeout=18000')  # 5 hrs timeout
        print('db connected succesfully!')

    def get_user_by_telegram_id(self, id):
        """
        Method requests info about user by his telegram id, and returns first and last name if exists
        of 0 otherwise
        :param id: user telegram id
        :return: first and last name of 0 if not exists
        """
        q = f'select first_name, last_name from staff where id={id};'

        self.curs.execute(q)

        res = self.curs.fetchone()
        if type(res) is type(None):
            return '0'
        else:
            return res

    def set_user_telegram_id(self, user_id):
        """
        Method adding users telegram id to table staff
        :param user_id: user telegram id
        """
        q = f'INSERT INTO five_star_db.staff (id, current_rating, general_rating,' \
            f' events_done, rate) VALUES ({user_id}, 0, 0, 0, ' \
            f'{config.START_RATE})'

        self.curs.execute(q)
        self.connect.commit()

    def set_user_first_name(self, user_id, name):
        """
        Method updates staff account with first name
        :param user_id: user telegram id
        :param name: first name of user
        """
        q = f"UPDATE five_star_db.staff SET first_name = '{name}' WHERE (id = '{user_id}');"

        self.curs.execute(q)

        self.connect.commit()

    def set_user_middle_name(self, user_id, m_name):
        """
        Method updates staff account with middle name
        :param user_id: user telegram id
        :param m_name: user middle name
        """
        q = f"UPDATE five_star_db.staff SET middle_name = '{m_name}' WHERE (id = '{user_id}');"

        self.curs.execute(q)

        self.connect.commit()

    def set_user_last_name(self, user_id, l_name):
        """
        Method updates staff account with last name
        :param user_id: user telegram id
        :param l_name: last name
        """
        q = f"UPDATE five_star_db.staff SET last_name = '{l_name}' WHERE (id = '{user_id}');"

        self.curs.execute(q)

        self.connect.commit()

    def set_user_role(self, user_id, role_id):
        """
        Inserts role into users account
        :param user_id: user telegram id
        :param role_id: id of role
        :return:
        """
        q = f"UPDATE five_star_db.staff SET staff_role = {role_id} WHERE (id ={user_id});"
        self.curs.execute(q)

        self.connect.commit()

    def set_user_qualification(self, user_id, role_quali):
        """
        Updates user qualification
        :param user_id: user telegram id
        :param role_quali: qualification code
        :return: None
        """
        q = f'UPDATE five_star_db.staff SET qualification = {role_quali} WHERE (id = {user_id});'
        self.curs.execute(q)
        self.connect.commit()

    def get_roles_list(self):
        """
        Returns list of roles
        :return:  set of roles
        """
        q = "select * from roles where name_role != 'не підтверджено';"
        self.curs.execute(q)
        res = self.curs.fetchall()

        return res

    def get_role_by_id(self, role_id):
        q = f'select * from roles where id_role = {role_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    def get_not_set_role(self):
        cursor = self.connect.cursor()
        q = "select id_role from roles where name_role = 'не підтверджено';"
        cursor.execute(q)
        res = cursor.fetchone()

        return res[0]

    def left_role_approving_request(self, user_id, role_id):
        cursor = self.connect.cursor()
        q = f"INSERT INTO five_star_db.role_confirmation (staff_id, requested_role, confirmed) VALUES ({user_id}, {role_id}, 0);"
        cursor.execute(q)
        self.connect.commit()

    def get_qualifications_list(self):
        cursor = self.connect.cursor()
        q = "select * from qualification where degree != 'не підтверджено';"
        cursor.execute(q)
        res = cursor.fetchall()

        return res

    def get_not_set_qualification(self):
        cursor = self.connect.cursor()
        q = "select id from qualification where degree = 'не підтверджено';"
        cursor.execute(q)
        res = cursor.fetchone()

        return res[0]

    def left_qualification_approving_request(self, user_id, quali_id):
        """
        Creates request to approve user qualification
        :param user_id: user telegram id
        :param quali_id: id of  qualification
        :return: None
        """
        cursor = self.connect.cursor()
        q = f"INSERT INTO five_star_db.qualification_confirmation (staff_id, requested_qualification, confirmed) VALUES ({user_id}, {quali_id}, 0);"
        cursor.execute(q)
        self.connect.commit()

    def get_user_role_by_id(self, user_id):
        """
        Returns information about user role
        :param user_id: user telegram id
        :return: set of role id and role name
        """
        q = f'select roles.id_role, roles.name_role from staff left join roles on staff.staff_role = roles.id_role where id = {user_id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    def get_unaccepted_role_requests(self):
        """
        Returns unaccepted role requests
        :return: unaccepted requests
        """
        self.connect.commit()
        q = 'select * from role_confirmation where confirmed = 0'

        self.curs.execute(q)

        return self.curs.fetchall()

    def get_unaccepted_qualification_requests(self):
        """
        Returns unaccepted qualification requests
        :return: unaccepted qualification requests
        """
        self.connect.commit()
        q = 'select * from qualification_confirmation where confirmed = 0'

        self.curs.execute(q)

        return self.curs.fetchall()

    def get_role_request_status(self, user_id):
        """
        Returns user's role request status
        :param user_id: user telegram id
        :return: status of request
        """
        self.connect.commit()
        q = f'select confirmed from role_confirmation where staff_id = {user_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    def get_qualification_request_status(self, user_id):
        """
        Returns user's qualification request status
        :param user_id: user telegram id
        :return: status of request
        """
        self.connect.commit()
        q = f'select confirmed from qualification_confirmation where staff_id = {user_id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    def get_user_name_by_id(self, user_id):
        """
        returns users full name by telegram id
        :param user_id: user telegram id
        :return: set of sirst name, middle name, last name
        """
        q = f'select first_name, middle_name, last_name from staff where id = {user_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    def accept_role_request(self, request_id, admin_id, date):
        """
        updates table 'role_requests'. confirms requested role
        :param request_id: id of request
        :param admin_id: telegram id of user whicj confirms (admin of manager)
        :param date: date of confirmation
        :return: None
        """
        q = f"update role_confirmation set date_confirmed = '{date}', confirmed_by = {admin_id}, confirmed = 1 where id = {request_id};"

        self.curs.execute(q)

        self.connect.commit()

    def update_staff_role(self, user_id, role_id):
        """
        Updates user role in staff table
        :param user_id:  user telegram id
        :param role_id: role id
        :return:  None
        """
        q = f'update staff set staff_role = {role_id} where id = {user_id};'

        self.curs.execute(q)

        self.connect.commit()

    def get_role_id_from_role_request(self, request):
        """
        Returns role id, requested by user
        :param request: id of role request
        :return: role id
        """
        q = f'select requested_role from role_confirmation where staff_id = {request};'

        self.curs.execute(q)

        return self.curs.fetchone()
