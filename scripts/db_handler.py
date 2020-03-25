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
            try:
                if args.__len__() == 0:
                    return func(self)
                else:
                    return func(self, args)
            except Exception as err:
                meth_name = sys._getframe().f_code.co_name

                print(f'exception in method {meth_name} - {err}')

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
            f'{config.NEW_RATE})'

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
    def update_staff_rate(self, *args):
        id, rate = args[0]
        q = f'update staff set rate={rate} where id={id};'

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
    def get_qualification_by_id(self, *args):
        """
        Returns qualification by its id
        :param args: id of qualification
        :return: qualification instance
        """
        id = args[0][0]
        q = f'select * from qualification where id = {id};'

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
        self.connect.commit()
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

    @check_session_time_alive
    def modify_role_request(self, *args):
        """
        Updates user requested role for applying for another role
        :param args: request id, role id
        :return: None
        """
        request_id, role_id = args[0]
        q = f'update role_confirmation set requested_role = {role_id} where id = {request_id};'

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
        q = f'select requested_qualification from qualification_confirmation where staff_id = {staff_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def accept_qualification_request(self, *args):
        """
        Updates qualification request as confirmed
        :param args: request id, admin telegram id, formatted date
        :return: None
        """
        req_id, admin_id, date = args[0]

        q = f"update qualification_confirmation set date_confirmed = '{date}', confirmed_by = {admin_id}, confirmed = 1 where id = {req_id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def update_staff_qualification(self, *args):
        """
        Updates staff information about his qualification
        :param args: user telegram id, id of qualification
        :return: None
        """
        user_id, quali_id = args[0]

        q = f'update staff set qualification = {quali_id} where id = {user_id}'
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

        q = f'update qualification_confirmation set requested_qualification={qual_id} where id={req_id};'
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
        q = f'select count(*) from staff where staff_role={role_id};'

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
    def get_unaccepted_events_list(self):
        """
        Returns list of unaccepted event requests
        :return: list of unaccepted event requests
        """
        q = 'select * from event_request where processed = 0;'

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

        q = 'select er.id, e.id, client_id, e.title, location, date_starts, date_ends, guests, ' \
            'type_of_event, event_class, staff_needed  ' \
            'from event_request er left join events e on er.id = e.event_request_id ' \
            'where processed = 0'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_client_by_id(self, *args):
        client_id = args[0][0]

        q = f'select * from clients where id = {client_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_event_type_by_id(self, *args):
        id = args[0][0]

        q = f'select * from event_types where id={id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_event_class_by_id(self, *args):
        id = args[0][0]

        q = f'select * from event_class where id={id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_event_location(self, *args):
        id, location = args[0]

        q = f"update events set location='{location}' where id={id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def update_event_title(self, *args):
        id, title = args[0]

        q = f"update events set title='{title}' where id={id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def update_event_type(self, *args):
        id, type_of_event = args[0]

        q = f"update events set type_of_event='{type_of_event}' where id={id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def update_event_class(self, *args):
        id, class_of_event = args[0]

        q = f"update events set event_class='{class_of_event}' where id={id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_event_types(self):
        q = 'select * from event_types;'

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

        q = f'select er.id, e.id, client_id, e.title, location, date_starts, date_ends, guests, ' \
            f'type_of_event, event_class, staff_needed  ' \
            f'from event_request er left join events e on er.id = e.event_request_id ' \
            f'where e.id = {event_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_event_request_id_by_event_id(self, *args):
        event_id = args[0][0]

        q = f'select event_request_id from events where id={event_id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_event_request_accepted(self, *args):
        """
        :param args: event request id, staf telegram id (manager)
        :return: None
        """
        event_request_id, staff_processed = args[0]

        q = f'update event_request set staff_processed={staff_processed}, processed=1 where id={event_request_id};'

        self.curs.execute(q)

        self.connect.commit()

    @check_session_time_alive
    def get_currencies(self):
        q = 'select * from curency;'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def update_event_price_and_staff(self, *args):
        """
        :param args: event id, price, curency id, staff needed
        :return:
        """
        event_id, price, currency_id, staff_needed = args[0]

        q = f'update events set price={price}, staff_needed={staff_needed}, curency={currency_id} where id={event_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def create_shift(self, *args):
        """
        :param args: event id, number of professionals, middles and beginners
        :return: None
        """
        event_id, pro, mid, beg = args[0]

        q = f'insert into shift(event_id, profesionals_number, middles_number, beginers_number)' \
            f'values ({event_id}, {pro}, {mid}, {beg});'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_upcoming_events(self):
        """
        Returns all events which didnt start yet
        :return: list of events
        """
        q = 'select * from events where date_starts > now()'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_upcoming_shifts(self):
        """
        :return:list of shifts which is yet to start
        """
        date = datetime.now()
        mysql_date = f'{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:00'
        q = f"select s.id, s.event_id, s.profesionals_number, s.middles_number, s.beginers_number, s.supervisor " \
            f"from shift s left join events e on s.event_id = e.id " \
            f"where e.date_starts > '{mysql_date}'"

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_event_request_by_id(self, *args):
        event_req = args[0][0]

        q = f'select * from event_request where id={event_req};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def delete_event_by_id(self, *args):
        event_id = args[0][0]

        q = f'delete from events where id={event_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_event_id_from_shift(self, *args):
        event_id = args[0][0]

        q = f'select id from shift where event_id={event_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_shift_by_id(self, *args):
        shift_id, pro, mid, beg = args[0]

        q = f'update shift set profesionals_number={pro}, middles_number={mid}, beginers_number={beg} where id={shift_id};'

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def is_event_processed(self, *args):
        event_id = args[0][0]

        q = f'select processed from event_request er left join events e on er.id = e.event_request_id where e.id = {event_id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_shift_extended_info_by_id(self, *args):
        shift_id = args[0][0]

        q = f'select sh.id, e.id, profesionals_number, middles_number, beginers_number, supervisor,' \
            f'title, location, date_starts, date_ends, guests, type_of_event, event_class, staff_needed, price, curency' \
            f' from shift sh left join events e on sh.event_id = e.id ' \
            f'where sh.id={shift_id};'

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

        q = f'select * from staff where id={staff_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_shift_supervisor(self, *args):
        shift_id, staff_id = args[0]

        q = f'update shift set supervisor={staff_id} where id={shift_id};'

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

        q = f'select staff_id from shift_registration sr left join staff s on sr.staff_id = s.id where shift_id={shift_id} and registered=1;'

        self.curs.execute(q)
        return self.curs.fetchall()

    @check_session_time_alive
    def register_staff_to_shift(self, *args):
        shift_id, staff_id, time = args[0]

        q = f"insert into shift_registration (shift_id, staff_id, date_registered ,registered) values ({shift_id}, {staff_id}, '{time}', 1);"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def reregister_staff_to_shift(self, *args):
        shift_id, staff_id, time = args[0]

        q = f"update shift_registration set registered=1, date_registered='{time}' where staff_id={staff_id} and shift_id={shift_id}"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_staff_registered_shifts_by_id(self, *args):
        staff_id = args[0][0]

        q = f'select title, date_starts, date_ends ' \
            f'from (shift_registration left join shift s on shift_registration.shift_id = s.id) ' \
            f'left join events e on e.id = s.event_id where staff_id={staff_id} and registered=1 and e.date_ends > now();'

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

        q = f'select shift_registration.id, title, date_starts, date_ends, check_in, check_out, rating, payment ' \
            f'from (shift_registration left join shift s on shift_registration.shift_id = s.id) ' \
            f'left join events e on e.id = s.event_id ' \
            f'where staff_id={staff_id} and registered=1 and check_out is null;'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_staff_registered_shifts_by_shift_registration_id_extended(self, *args):
        shift_registration_id, staff_id = args[0]

        q = f'select shift_registration.id, title, date_starts, date_ends, date_registered, check_in, check_out, rating, payment ' \
            f'from (shift_registration left join shift s on shift_registration.shift_id = s.id) ' \
            f'left join events e on e.id = s.event_id where shift_registration.id={shift_registration_id} and staff_id={staff_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def cancel_shift_registration_for_user(self, *args):
        shift_reg_id, staff_id, date = args[0]

        q = f"update shift_registration set registered=0, date_registered='{date}' where id={shift_reg_id} and staff_id={staff_id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def get_shift_registration_by_staff_id_and_shift_id(self, *args):
        staff_id, shift_id = args[0]

        q = f'select * from shift_registration where staff_id={staff_id} and shift_id={shift_id};'

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

        q = f'select s.id, e.id, e.date_starts, e.date_ends from (shift_registration sr left join shift s on sr.shift_id = s.id) ' \
            f'left join events e on s.event_id = e.id where sr.id = {shift_reg_id} and sr.staff_id={staff};'

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

        q = f"update shift_registration set check_in='{date}' where id={shift_reg_id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def check_out_off_shift(self, *args):
        shift_reg_id, time = args[0]

        q = f"update shift_registration set check_out='{time}' where id={shift_reg_id};"

        self.curs.execute(q)
        self.connect.commit()

    @check_session_time_alive
    def update_shift_status(self, *args):
        shift_id = args[0][0]

        q = f'update shift set ended=1 where id={shift_id};'
        self.connect.commit()

    @check_session_time_alive
    def get_staff_on_shift(self, *args):
        shift_id = args[0][0]

        q = f'select s.id, first_name, middle_name, last_name, q.degree, current_rating, events_done ' \
            f'from (shift_registration sr left join staff s on sr.staff_id = s.id) ' \
            f'left join qualification q on s.qualification=q.id ' \
            f'where shift_id={shift_id}'

        self.curs.execute(q)

        return  self.curs.fetchall()

    @check_session_time_alive
    def get_supervisor_on_shift(self, *args):
        shift_id = args[0][0]

        q = f'select supervisor from shift where id={shift_id}'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_staff_event_number(self, *args):
        staff_id = args[0][0]

        q = f'select events_done from staff where id={staff_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def update_staff_rating_and_events_count(self, *args):
        staff_id, rating, events = args[0]

        q = f'update staff set events_done={events}, current_rating={rating} where id={staff_id}'

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

        q = f'select * from shift_registration where id={shift_reg_id};'
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

        q = f'select sr.id, sh.id, date_registered, check_in, check_out, e.title ' \
            f'from (shift_registration sr left join shift sh on sr.shift_id = sh.id) ' \
            f'left join events e on sh.event_id = e.id ' \
            f'where staff_id={staff_id} and check_out is not null'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_all_ended_shifts(self):
        q = f'select shift.id, title, events.date_starts, events.date_ends ' \
            f'from shift left join events on shift.event_id = events.id ' \
            f'where ended = 1 ' \
            f'order by date_ends desc'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_shift_general_info_for_archive(self, *args):
        shift_id = args[0][0]

        q = f'select title, date_starts, date_ends, guests, et.name_of_event, ec.class ' \
            f'from ((shift sh left join events e on sh.event_id = e.id) left join event_types et on et.id = e.type_of_event)' \
            f'left join event_class ec on ec.id = e.event_class where sh.id={shift_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_waiter_personal_info_from_shift_registration(self, *args):
        sh_reg_id = args[0][0]

        q = f'select check_in, check_out, rating, payment' \
            f' from shift_registration where id={sh_reg_id};'

        self.curs.execute(q)

        return self.curs.fetchone()

    @check_session_time_alive
    def get_shift_info_for_manager(self, *args):
        shift_id = args[0][0]

        q = f'select * from shift where id={shift_id};'

    @check_session_time_alive
    def get_shift_registrations_by_shift_id(self, *args):
        shift_id = args[0][0]

        q = f'select * from shift_registration where shift_id={shift_id} and registered=1;'

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

        q = f"select sr.id, sh.id, title, check_in, check_out, rating, payment " \
            f"from (shift_registration sr left join shift sh on sr.shift_id = sh.id) " \
            f"left join events e on e.id = sh.event_id " \
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

        q = f'select id, staff_id, date_registered, check_in, check_out, rating, payment ' \
            f'from shift_registration ' \
            f'where shift_id={shift_id};'

        self.curs.execute(q)

        return self.curs.fetchall()

    @check_session_time_alive
    def get_staff_ever_worked(self):
        q = f'select staff_id, last_name, first_name, middle_name, rl.name_role, ql.degree ' \
            f'from ((shift_registration sh left join staff st on st.id = sh.staff_id) ' \
            f'left join roles rl on st.staff_role = rl.id_role) ' \
            f'left join qualification ql on ql.id = st.qualification ' \
            f'where check_out is not null ' \
            f'group by staff_id'

        self.curs.execute(q)

        return self.curs.fetchall()


