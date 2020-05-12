import mysql.connector
import config
from datetime import datetime
import sys


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
            database='five_star',
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
                    database='five_star',
                    auth_plugin='mysql_native_password'
                )
                self.curs = self.connect.cursor(buffered=True)
                self.session_time_alive = datetime.now()
            try:
                if args.__len__() == 0:
                    return func(self)
                else:
                    return func(self, args)
            except Exception as err:
                meth_name = sys._getframe().f_code.co_name
                raise Exception(f'database exception in method {meth_name} - {err}')
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
        q = f'select first_name, last_name from staff where staff_id={id};'

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
        user_id, rate = args[0]
        q = f'INSERT INTO staff (staff_id, rating,' \
            f' events_done, rate) VALUES ({user_id}, 0, 0, ' \
            f'{rate})'

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
        q = f"UPDATE staff SET first_name = '{name}' WHERE (staff_id = '{user_id}');"

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
        q = f"UPDATE five_star.staff SET middle_name = '{m_name}' WHERE (staff_id = '{user_id}');"

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
        q = f"UPDATE staff SET last_name = '{l_name}' WHERE (staff_id = '{user_id}');"

        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def update_staff_rate(self, *args):
        id, rate = args[0]
        q = f'update staff set rate={rate} where staff_id ={id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_roles_list(self):
        """
        Returns list of roles
        :return:  set of roles
        """
        q = "select * from role where role_name != 'Не підтверджено';"
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
        q = f'select * from role where role_id = {role_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_qualification_by_id(self, *args):
        """
        Returns qualification by its id
        :param args: id of qualification
        :return: qualification instance
        """
        id = args[0][0]

        q = f'select * from qualification where qualification_id={id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_staff_role_by_id(self, *args):
        staff_id = args[0][0]

        q = f'select confirmed ' \
            f'from (staff left join role_confirmation rc on staff.role_confirmation_id = rc.role_confirmation_id) ' \
            f'left join role rl on rl.role_id = rc.role_id ' \
            f'where staff_id={staff_id};'
        self.curs.execute(q)

        is_confirmed = bool(self.curs.fetchone()[0])

        if is_confirmed:
            q = f'select rl.role_id, rl.role_name ' \
                f'from (staff left join role_confirmation rc on staff.role_confirmation_id = rc.role_confirmation_id) ' \
                f'left join role rl on rl.role_id = rc.role_id ' \
                f'where staff_id={staff_id};'
        else:
            q = f"select * from role where role_name = 'Не підтверджено'"

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_staff_qualification_by_id(self, *args):
        """
        Returns staff qualification by staff id
        :param args: staff telegram id
        :return: qualification instance
        """
        user_id = args[0][0]

        q = f'select confirmed ' \
            f'from (staff left join qualification_confirmation qc on staff.qualification_confirmation_id = qc.qualification_confirmation_id) ' \
            f'left join qualification ql on ql.qualification_id = qc.qualification_id ' \
            f'where staff_id={user_id};'
        self.curs.execute(q)

        is_confirmed = bool(self.curs.fetchone()[0])

        if is_confirmed:
            q = f'select ql.qualification_id, ql.qualification_name ' \
                f'from (staff left join qualification_confirmation qc on staff.qualification_confirmation_id = qc.qualification_confirmation_id) ' \
                f'left join qualification ql on ql.qualification_id = qc.qualification_id ' \
                f'where staff_id={user_id};'
        else:
            q = f"select * from qualification where qualification_name = 'Не підтверджено'"

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_not_set_role(self):
        """
        Returns id of 'not set' role
        :return: role id
        """
        cursor = self.connect.cursor()
        q = "select role_id from role where role_name = 'Не підтверджено';"
        cursor.execute(q)
        res = cursor.fetchone()

        return res[0]

    @check_session_time_alive
    def left_role_approving_request(self, *args):
        """
        Creates role request
        :param user_id: user telegram id who left request
        :param role_id: id of role, needed to approve
        :return: None
        """
        user_id, role_id = args[0]
        date = datetime.now()
        mysql_date = f'{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}'

        q = f"INSERT INTO role_confirmation (role_id, date_placed, confirmed) " \
            f"VALUES ({role_id}, '{mysql_date}', 0);"

        self.curs.execute(q)
        self.connect.commit()

        q = f'select last_insert_id();'

        self.curs.execute(q)
        role_confirmation_id = self.curs.fetchone()[0]

        q = f'update staff set role_confirmation_id ={role_confirmation_id} where staff_id={user_id};'
        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_qualifications_list(self):
        """
        Returns id's of qualifications, except 'not set'
        :return: id of qualifications
        """
        cursor = self.connect.cursor()
        q = "select * from qualification where qualification_name != 'Не підтверджено';"
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
        q = "select qualification_id from qualification where qualification_name = 'Не підтверджено';"
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
        date = datetime.now()
        mysql_date = f'{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}'

        q = f"INSERT INTO qualification_confirmation (qualification_id, date_placed, confirmed) " \
            f"VALUES ({quali_id}, '{mysql_date}', 0);"

        self.curs.execute(q)
        self.connect.commit()

        q = f'select last_insert_id();'

        self.curs.execute(q)
        quali_confirmation_id = self.curs.fetchone()[0]

        q = f'update staff set qualification_confirmation_id ={quali_confirmation_id} where staff_id={user_id};'
        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_user_role_by_id(self, *args):
        """
        Returns information about user role
        :param user_id: user telegram id
        :return: set of role id and role name
        """
        self.connect.commit()
        user_id = args[0][0]

        q = f'select confirmed ' \
            f'from (staff left join role_confirmation rc on staff.role_confirmation_id = rc.role_confirmation_id) ' \
            f'left join role rl on rl.role_id = rc.role_id ' \
            f'where staff_id={user_id};'
        self.curs.execute(q)

        is_confirmed = bool(self.curs.fetchone()[0])

        if is_confirmed:
            q = f'select rl.role_id, rl.role_name ' \
                f'from (staff left join role_confirmation rc on staff.role_confirmation_id = rc.role_confirmation_id) ' \
                f'left join role rl on rl.role_id = rc.role_id ' \
                f'where staff_id={user_id};'
        else:
            q = f"select * from role where role_name = 'Не підтверджено'"

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_unaccepted_role_requests(self):
        """
        Returns unaccepted role requests
        :return: unaccepted requests
        """
        self.connect.commit()
        q = 'select rc.role_confirmation_id, st.staff_id, rc.role_id, rc.date_placed, rc.date_approved, rc.confirmed ' \
            'from role_confirmation rc left join staff st on st.role_confirmation_id=rc.role_confirmation_id ' \
            'where confirmed = 0'

        self.curs.execute(q)
        return self.curs.fetchall()

    @check_session_time_alive
    def get_unaccepted_qualification_requests(self):
        """
        Returns unaccepted qualification requests
        :return: unaccepted qualification requests
        """
        self.connect.commit()
        q = 'select qc.qualification_confirmation_id, s.staff_id, qc.qualification_id, qc.date_placed, qc.date_approved, qc.confirmed ' \
            'from qualification_confirmation qc left join staff s on qc.qualification_confirmation_id = s.qualification_confirmation_id ' \
            'where confirmed = 0'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_role_request_status(self, *args):
        """
        Returns user's role request status
        :param user_id: staff telegram id
        :return: status of request
        """
        user_id = args[0][0]
        self.connect.commit()
        q = f'select confirmed ' \
            f'from staff st left join role_confirmation rc on st.role_confirmation_id=rc.role_confirmation_id ' \
            f'where st.staff_id = {user_id};'

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
        q = f'select confirmed ' \
            f'from staff st left join qualification_confirmation qc on st.qualification_confirmation_id = qc.qualification_confirmation_id ' \
            f'where st.staff_id = {user_id}'

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
        q = f'select first_name, middle_name, last_name from staff where staff_id={user_id};'

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
        request_id, date = args[0]
        q = f"update role_confirmation set date_approved = '{date}', confirmed = 1 " \
            f"where role_confirmation_id = {request_id};"

        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def get_role_id_from_role_request(self, *args):
        """
        Returns role id, requested by user
        :param staff_id: staff telegram id
        :return: role id
        """
        staff_id = args[0][0]
        q = f'select role_id ' \
            f'from role_confirmation rc left join staff st on rc.role_confirmation_id = st.role_confirmation_id ' \
            f'where staff_id = {staff_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def modify_role_request(self, *args):
        """
        Updates user requested role for applying for another role
        :param args: request id, role id
        :return: None
        """
        request_id, role_id = args[0]
        q = f'update role_confirmation set role_id = {role_id} where role_confirmation_id = {request_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_qualification_id_from_qualification_request(self, *args):
        """
        Returns id of requested qualification from request
        :param args: id of request
        :return: qualification id
        """
        staff_id = args[0][0]
        q = f'select qualification_id ' \
            f'from qualification_confirmation qc left join staff st on qc.qualification_confirmation_id=st.qualification_confirmation_id ' \
            f'where staff_id = {staff_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def accept_qualification_request(self, *args):
        """
        Updates qualification request as confirmed
        :param args: request id, admin telegram id, formatted date
        :return: None
        """
        req_id, date = args[0]

        q = f"update qualification_confirmation set date_approved='{date}', confirmed = 1" \
            f" where qualification_confirmation_id = {req_id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def modify_qualification_request(self, *args):
        """
        Modifies qualification request details
        :param args: qualification request id, id of needed qualification
        :return: None
        """
        req_id, qual_id = args[0]

        q = f'update qualification_confirmation set qualification_id={qual_id} ' \
            f'where qualification_confirmation_id={req_id};'
        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def get_staff_count_by_role(self, *args):
        """
        Returns count of staff by specified role id
        :param: args: id of role
        :return: count of staff by role
        """
        role_id = args[0][0]
        q = f'select count(*) ' \
            f'from staff st left join role_confirmation rc on st.role_confirmation_id=rc.role_confirmation_id ' \
            f'where role_id={role_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_session_duration(self):
        """
        Returns session duration
        :return: session duration(seconds)
        """
        return (datetime.now() - self.session_time_alive).seconds

    @check_session_time_alive
    def get_unaccepted_events_list(self, *args):
        """
        Returns list of unaccepted event requests.
        there's processed status check about '-2' value, cuz it supposed to be check if
        request currently processing, but it's not implemented (yet)
        :return: list of unaccepted event requests
        """
        staff_id = args[0][0]

        q = f'select * ' \
            f'from event_request ' \
            f'where processed = 0 or (processed=-2 and staff_processed={staff_id});'

        self.curs.execute(q)
        return self.curs.fetchall()

    @check_session_time_alive
    def get_event_request(self):
        q = 'select * from event_request where processed = 0 limit 1'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_event_request_extended_info(self):
        """
        Return extended data about event request
        :return:event request id, event id, client id, location of event,
                date starts, date ends, number of guests, id of type of event,
                id of event class, number of needed staff
        """
        self.connect.commit()

        q = 'select er.event_request_id, e.event_id, client_id, e.title, e.location, ' \
            'date_starts, date_ends, number_of_guests, ' \
            'event_type_id, event_class_id, staff_needed  ' \
            'from event_request er left join event e on er.event_request_id = e.event_request_id ' \
            'where processed = 0'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_client_by_id(self, *args):
        client_id = args[0][0]

        q = f'select * from client where client_id = {client_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_event_type_by_id(self, *args):
        id = args[0][0]

        q = f'select * from event_type where event_type_id={id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_event_class_by_id(self, *args):
        id = args[0][0]

        q = f'select * from event_class where event_class_id={id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_event_location(self, *args):
        id, location = args[0]

        q = f"update event set location='{location}' where event_id={id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def update_event_title(self, *args):
        id, title = args[0]

        q = f"update event set title='{title}' where event_id={id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def update_event_type(self, *args):
        id, type_of_event = args[0]

        q = f"update event set event_type_id='{type_of_event}' where event_id={id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def update_event_class(self, *args):
        id, class_of_event = args[0]

        q = f"update event set event_class_id='{class_of_event}' where event_id={id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_event_types(self):
        q = 'select * from event_type;'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_event_classes(self):
        q = 'select * from event_class;'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_event_request_extended_info_by_id(self, *args):
        event_id = args[0][0]

        q = f'select er.event_request_id, e.event_id, client_id, e.title, location, date_starts, date_ends, number_of_guests, ' \
            f'event_type_id, event_class_id, staff_needed  ' \
            f'from event_request er left join event e on er.event_request_id = e.event_request_id ' \
            f'where e.event_id = {event_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_event_request_id_by_event_id(self, *args):
        event_id = args[0][0]

        q = f'select event_request_id from event where event_id={event_id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_event_request_accepted(self, *args):
        """
        :param args: event request id, staf telegram id (manager)
        :return: None
        """
        event_request_id, staff_processed = args[0]

        q = f'update event_request set staff_processed={staff_processed}, processed=1 ' \
            f'where event_request_id={event_request_id};'

        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def update_event_price_and_staff(self, *args):
        """
        :param args: event id, price, curency id, staff needed
        :return:
        """
        event_id, price, staff_needed = args[0]

        q = f'update event set price={price}, staff_needed={staff_needed} ' \
            f'where event_id={event_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def create_shift(self, *args):
        """
        :param args: event id, number of professionals, middles and beginners
        :return: None
        """
        event_id, pro, mid, beg = args[0]

        q = f'insert into shift(event_id, professionals_number, middles_number, beginers_number)' \
            f'values ({event_id}, {pro}, {mid}, {beg});'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_upcoming_events(self):
        """
        Returns all events which didnt start yet
        :return: list of events
        """
        date = datetime.now()
        mysql_date = f'{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:00'
        q = f"select * from event where date_starts > '{mysql_date}'"

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_upcoming_shifts(self):
        """
        :return:list of shifts which is yet to start
        """
        date = datetime.now()
        mysql_date = f'{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:00'
        q = f"select s.shift_id, s.event_id, s.professionals_number, s.middles_number, s.beginers_number, s.supervisor " \
            f"from shift s left join event e on s.event_id = e.event_id " \
            f"where e.date_starts > '{mysql_date}'"

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_event_request_by_id(self, *args):
        event_req = args[0][0]

        q = f'select * from event_request where event_request_id={event_req};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def delete_event_by_id(self, *args):
        event_id = args[0][0]

        q = f'delete from event where event_id={event_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_shift_id_by_event_id(self, *args):
        event_id = args[0][0]

        q = f'select shift_id from shift where event_id={event_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_shift_by_id(self, *args):
        shift_id, pro, mid, beg = args[0]

        q = f'update shift set professionals_number={pro}, middles_number={mid}, beginers_number={beg} ' \
            f'where shift_id={shift_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def is_event_processed(self, *args):
        event_id = args[0][0]

        q = f'select processed from event_request er left join event e on er.event_request_id = e.event_request_id ' \
            f'where e.event_id = {event_id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_shift_extended_info_by_id(self, *args):
        shift_id = args[0][0]

        q = f'select sh.shift_id, e.event_id, professionals_number, middles_number, beginers_number, supervisor,' \
            f'title, location, date_starts, date_ends, number_of_guests, event_type_id, event_class_id, staff_needed, price' \
            f' from shift sh left join event e on sh.event_id = e.event_id ' \
            f'where sh.shift_id={shift_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_registered_to_shift(self, *args):
        shift_id = args[0][0]

        q = f'select * from shift_registration where shift_id={shift_id} and registered=1;'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_staff_by_id(self, *args):
        staff_id = args[0][0]

        q = f'select * from staff where staff_id={staff_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_shift_supervisor(self, *args):
        shift_id, staff_id = args[0]

        q = f'update shift set supervisor={staff_id} where shift_id={shift_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_staff_shift_registrations(self, *args):
        staff_id = args[0][0]

        q = f'select * from shift_registration where staff_id={staff_id};'

        self.curs.execute(q)
        return self.curs.fetchall()

    @check_session_time_alive
    def get_staff_id_registered_to_shift_by_id(self, *args):
        shift_id = args[0][0]

        q = f'select s.staff_id ' \
            f'from shift_registration sr left join staff s on sr.staff_id = s.staff_id ' \
            f'where shift_id={shift_id} and registered=1;'

        self.curs.execute(q)
        return self.curs.fetchall()

    @check_session_time_alive
    def register_staff_to_shift(self, *args):
        shift_id, staff_id, time = args[0]

        q = f"insert into shift_registration (shift_id, staff_id, date_registered ,registered) " \
            f"values ({shift_id}, {staff_id}, '{time}', 1);"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def reregister_staff_to_shift(self, *args):
        shift_id, staff_id, time = args[0]

        q = f"update shift_registration set registered=1, date_registered='{time}' " \
            f"where staff_id={staff_id} and shift_id={shift_id}"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_staff_registered_shifts_by_id(self, *args):
        staff_id = args[0][0]

        q = f'select title, date_starts, date_ends ' \
            f'from (shift_registration left join shift s on shift_registration.shift_id = s.shift_id) ' \
            f'left join event e on e.event_id = s.event_id where staff_id={staff_id} and registered=1 and e.date_ends > now();'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_staffs_shift_registrations(self, *args):
        staff_id = args[0][0]

        q = f'select * from shift_registration where staff_id={staff_id}'
        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_staff_registered_shifts_by_id_extended(self, *args):
        staff_id = args[0][0]

        q = f'select shift_registration.shift_registration_id, title, date_starts, date_ends, check_in, check_out, rating, payment ' \
            f'from (shift_registration left join shift s on shift_registration.shift_id = s.shift_id) ' \
            f'left join event e on e.event_id = s.event_id ' \
            f'where staff_id={staff_id} and registered=1 and check_out is null;'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_staff_registered_shifts_by_shift_registration_id_extended(self, *args):
        shift_registration_id, staff_id = args[0]

        q = f'select shift_registration.shift_registration_id, title, date_starts, date_ends, date_registered, check_in, check_out, rating, payment ' \
            f'from (shift_registration left join shift s on shift_registration.shift_id = s.shift_id) ' \
            f'left join event e on e.event_id = s.event_id where shift_registration.shift_registration_id={shift_registration_id} and staff_id={staff_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def cancel_shift_registration_for_user(self, *args):
        shift_reg_id, staff_id, date = args[0]

        q = f"update shift_registration set registered=0, date_registered='{date}' " \
            f"where shift_registration_id={shift_reg_id} and staff_id={staff_id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_shift_registration_by_staff_id_and_shift_id(self, *args):
        staff_id, shift_id = args[0]

        q = f'select * from shift_registration ' \
            f'where staff_id={staff_id} and shift_id={shift_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_event_date_by_shift_registration_id_and_staff_id(self, *args):
        """
        Gets information about event dates by shift registration id and staff id
        :param args: shift registration id, staff id
        :return: event id, shift id, date starts, date ends
        """
        shift_reg_id, staff = args[0]

        q = f'select e.event_id, s.shift_id, e.date_starts, e.date_ends ' \
            f'from (shift_registration sr left join shift s on sr.shift_id = s.shift_id) ' \
            f'left join event e on s.event_id = e.event_id ' \
            f'where sr.shift_registration_id = {shift_reg_id} and sr.staff_id={staff};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def check_in_to_shift(self, *args):
        """
        Updates information about shift registration with check in
        :param args: date of check in, shift registration id
        :return: None
        """
        date, shift_reg_id = args[0]

        q = f"update shift_registration set check_in='{date}' " \
            f"where shift_registration_id={shift_reg_id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def check_out_off_shift(self, *args):
        shift_reg_id, time = args[0]

        q = f"update shift_registration set check_out='{time}' " \
            f"where shift_registration_id={shift_reg_id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def update_shift_status(self, *args):
        shift_id = args[0][0]

        q = f'update shift set ended=1 where shift_id={shift_id};'
        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_staff_on_shift(self, *args):
        shift_id = args[0][0]

        q = f'select s.staff_id, first_name, middle_name, last_name, q.qualification_name, s.rating, events_done ' \
            f'from ((shift_registration sr left join staff s on sr.staff_id = s.staff_id) ' \
            f'left join qualification_confirmation qc on s.qualification_confirmation_id=qc.qualification_confirmation_id) ' \
            f'left join qualification q on qc.qualification_id=q.qualification_id ' \
            f'where shift_id={shift_id}'

        self.curs.execute(q)

        return  self.curs.fetchall()

    @check_session_time_alive
    def get_supervisor_on_shift(self, *args):
        shift_id = args[0][0]

        q = f'select supervisor from shift where shift_id={shift_id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_staff_event_number(self, *args):
        staff_id = args[0][0]

        q = f'select events_done from staff where staff_id={staff_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_staff_rating_and_events_count(self, *args):
        staff_id, rating, events = args[0]

        q = f'update staff set events_done={events}, rating={rating} where staff_id={staff_id}'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_staff_rating_for_shift(self, *args):
        staff_id, shift_id = args[0]

        q = f'select rating from shift_registration where staff_id={staff_id} and shift_id={shift_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def set_staff_rating_for_shift(self, *args):
        staff_id, shift_id, rating = args[0]

        q = f'update shift_registration set rating={rating} where shift_id={shift_id} and staff_id={staff_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def set_payment_for_shift(self, *args):
        shift_id, staff_id, payment = args[0]

        q = f'update shift_registration set payment={payment} ' \
            f'where staff_id={staff_id} and shift_id={shift_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_staff_shift_ratings(self, *args):
        staff_id = args[0][0]

        q = f'select * from shift_registration ' \
            f'where staff_id={staff_id} and registered = 1 and rating is not null;'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_shift_registration_by_shift_reg_id(self, *args):
        shift_reg_id = args[0][0]

        q = f'select * from shift_registration ' \
            f'where shift_registration_id={shift_reg_id};'
        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_staff_on_shift_for_rating(self, *args):
        shift_id = args[0][0]

        q = f'select * from shift_registration where registered=1 and shift_id={shift_id};'

        self.curs.execute(q)
        return self.curs.fetchall()

    @check_session_time_alive
    def get_staff_on_shift_for_closing(self, *args):
        shift_id = args[0][0]

        q = f'select staff_id, check_out, rating from shift_registration where shift_id={shift_id};'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_ended_staff_shifts(self, *args):
        staff_id = args[0][0]

        q = f'select sr.shift_registration_id, sh.shift_id, date_registered, check_in, check_out, e.title ' \
            f'from (shift_registration sr left join shift sh on sr.shift_id = sh.shift_id) ' \
            f'left join event e on sh.event_id = e.event_id ' \
            f'where staff_id={staff_id} and check_out is not null'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_all_ended_shifts(self):
        q = f'select shift.shift_id, title, e.date_starts, e.date_ends ' \
            f'from shift left join event e on shift.event_id = e.event_id ' \
            f'where ended = 1 ' \
            f'order by date_ends desc'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_shift_general_info_for_archive(self, *args):
        shift_id = args[0][0]

        q = f'select title, date_starts, date_ends, number_of_guests, et.event_type_name, ec.event_class_name ' \
            f'from ((shift sh left join event e on sh.event_id = e.event_id) ' \
            f'left join event_type et on et.event_type_id = e.event_type_id)' \
            f'left join event_class ec on ec.event_class_id = e.event_class_id ' \
            f'where sh.shift_id={shift_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_waiter_personal_info_from_shift_registration(self, *args):
        sh_reg_id = args[0][0]

        q = f'select check_in, check_out, rating, payment' \
            f' from shift_registration ' \
            f'where shift_registration_id={sh_reg_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_shift_info_for_manager(self, *args):
        shift_id = args[0][0]

        q = f'select * from shift where shift_id={shift_id};'

    @check_session_time_alive
    def get_shift_registrations_by_shift_id(self, *args):
        shift_id = args[0][0]

        q = f'select * from shift_registration ' \
            f'where shift_id={shift_id} and registered=1;'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_staff_shift_registrations_ended(self, *args):
        staff_id = args[0][0]

        q = f'select * ' \
            f'from shift_registration ' \
            f'where staff_id={staff_id} and registered=1 and check_out is not null ' \
            f'order by check_out desc '

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_shift_registrations_for_period(self, *args):
        staff_id, date_from, date_to = args[0]

        q = f"select sr.shift_registration_id, sh.shift_id, e.title, check_in, check_out, rating, payment " \
            f"from (shift_registration sr left join shift sh on sr.shift_id = sh.shift_id) " \
            f"left join event e on e.event_id = sh.event_id " \
            f"where staff_id={staff_id} and registered=1 and check_out is not null and " \
            f"check_in >='{date_from}' and check_in <= '{date_to}'" \
            f"order by check_in desc;"

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_ended_shift_registrations(self):
        q = f'select * from shift_registration where check_out is not null ' \
            f'order by check_out desc;'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_ended_shift_ids_in_period(self, *args):
        date_from, date_to = args[0]

        q = f"select shift_id from shift_registration " \
            f"where registered=1 and check_out is not null and " \
            f"check_in >='{date_from}' and check_in <= '{date_to}' " \
            f"group by shift_id;"

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_ended_registrations_by_shift_id(self, *args):
        shift_id = args[0][0]

        q = f'select shift_registration_id, staff_id, date_registered, check_in, check_out, rating, payment ' \
            f'from shift_registration ' \
            f'where shift_id={shift_id};'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_staff_ever_worked(self):
        q = f'select st.staff_id, last_name, first_name, middle_name, rl.role_name, q.qualification_name ' \
            f'from ((((shift_registration sh left join staff st on st.staff_id = sh.staff_id) ' \
            f'left join role_confirmation rc on st.role_confirmation_id = rc.role_confirmation_id) ' \
            f'left join role rl on rc.role_id = rl.role_id)' \
            f'left join qualification_confirmation qc on st.qualification_confirmation_id) ' \
            f'left join qualification q on q.qualification_id=qc.qualification_id ' \
            f'where check_out is not null ' \
            f'group by st.staff_id, last_name, first_name, middle_name, rl.role_name, q.qualification_name'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_upcoming_shifts_for_notifier(self):
        q = f'select staff_id, s.shift_id, e.event_id, e.date_starts, e.title ' \
            f'from (shift_registration sr left join shift s on sr.shift_id = s.shift_id) ' \
            f'left join event e on s.event_id = e.event_id ' \
            f'where sr.check_in is null  and e.date_starts > now();'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_staff_main_menu_msg_id(self, *args):
        staff_id = args[0][0]

        q = f'select * from staff_last_message_to_edit where staff_id={staff_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_staff_main_menu_msg_id(self, *args):
        staff_id, msg_id = args[0]

        q = f'update staff_last_message_to_edit set message_id={msg_id} where staff_id={staff_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def insert_staff_main_menu_msg_id(self, *args):
        staff_id, msg_id = args[0]

        q = f'insert into staff_last_message_to_edit values ({staff_id}, {msg_id});'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_all_staff_by_role_id(self, *args):
        role_id = args[0][0]

        q = f'select * ' \
            f'from staff left join role_confirmation rc on staff.role_confirmation_id = rc.role_confirmation_id ' \
            f'where rc.role_id={role_id} and confirmed=1;'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_config_value(self, *args):
        key = args[0][0]

        q = f"select _value from config where _key='{key}';"

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_manager_with_least_processed_events(self):

        # in rc.role_id = 2, 2 is manager role id

        q = f"select staff_id, count(staff_processed) as 'count_processed' " \
            f"from (event_request er right join staff st on er.staff_processed=st.staff_id) " \
            f"left join role_confirmation rc on rc.role_confirmation_id=st.role_confirmation_id " \
            f"where rc.role_id=2 " \
            f"group by staff_id " \
            f"order by count_processed asc "

        self.curs.execute(q)
        return self.curs.fetchall()

    @check_session_time_alive
    def update_event_request_status_in_process_of_accepting(self, *args):
        staff, ev_req_id = args[0][0]

        q = f'update event_request set processed=-2, staff_processed={staff} where event_request_id={ev_req_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_client_id_by_event_id(self, *args):
        event_id = args[0][0]

        q = f'select cl.client_id ' \
            f'from (client cl left join event_request er on cl.client_id = er.client_id) ' \
            f'left join event ev on ev.event_request_id=er.event_request_id ' \
            f'where ev.event_id = {event_id}'

        self.curs.execute(q)
        return self.curs.fetchone()

