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
        print('db connected succesfully!')

    def get_user_by_telegram_id(self, id):
        """
        Method requests info about user by his telegram id, and returns first and last name if exists
        of 0 otherwise
        :param id: user telegram id
        :return: first and last name of 0 if not exists
        """

        cursor = self.connect.cursor()
        q = f'select first_name, last_name from staff where id={id};'

        cursor.execute(q)

        res = cursor.fetchone()
        if type(res) is type(None):
            return '0'
        else:
            return res

    def set_user_telegram_id(self, user_id):
        """
        Method adding users telegram id to table staff
        :param user_id: user telegram id
        """

        cursor = self.connect.cursor()

        q = f'INSERT INTO five_star_db.staff (id, current_rating, general_rating,' \
            f' events_done, rate) VALUES ({user_id}, 0, 0, 0, ' \
            f'{config.START_RATE})'

        cursor.execute(q)
        self.connect.commit()

    def set_user_first_name(self, user_id, name):
        """
        Method updates staff account with first name
        :param user_id: user telegram id
        :param name: first name of user
        """

        cursor = self.connect.cursor()
        q = f"UPDATE five_star_db.staff SET first_name = '{name}' WHERE (id = '{user_id}');"

        cursor.execute(q)

        self.connect.commit()

    def set_user_middle_name(self, user_id, m_name):
        """
        Method updates staff account with middle name
        :param user_id: user telegram id
        :param m_name: user middle name
        """

        cursor = self.connect.cursor()
        q = f"UPDATE five_star_db.staff SET middle_name = '{m_name}' WHERE (id = '{user_id}');"

        cursor.execute(q)

        self.connect.commit()

    def set_user_last_name(self, user_id, l_name):
        """
        Method updates staff account with last name
        :param user_id: user telegram id
        :param l_name: last name
        """

        cursor = self.connect.cursor()
        q = f"UPDATE five_star_db.staff SET last_name = '{l_name}' WHERE (id = '{user_id}');"

        cursor.execute(q)

        self.connect.commit()

    def set_user_role(self, user_id, role_id):
        """
        Inserts role into users account
        :param user_id: user telegram id
        :param role_id: id of role
        :return:
        """
        cursor = self.connect.cursor()

        q = f"UPDATE five_star_db.staff SET staff_role = {role_id} WHERE (id ={user_id});"
        cursor.execute(q)

        self.connect.commit()

    def set_user_qualification(self, user_id, role_quali):
        """
        Updates user qualification
        :param user_id: user telegram id
        :param role_quali: qualification code
        :return: None
        """
        cursor = self.connect.cursor()
        q = f'UPDATE five_star_db.staff SET qualification = {role_quali} WHERE (id = {user_id});'
        cursor.execute(q)
        self.connect.commit()

    def get_roles_list(self):
        cursor = self.connect.cursor()
        q = "select * from roles where name_role != 'не підтверджено';"
        cursor.execute(q)
        res = cursor.fetchall()

        return res

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
