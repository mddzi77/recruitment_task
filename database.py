import datetime as dt
import os.path
import sqlite3 as sql
from sqlite3 import Error as sqlError


class Database:

    def __init__(self):

        new_instance = not os.path.exists('reservations.db')

        # connecting to the database
        self.conn = None
        try:
            self.conn = sql.connect('reservations.db')
            self.cur = self.conn.cursor()
            if new_instance:
                self.new_file()
        except sqlError as err:
            print(err)

    def new_file(self):
        """
        Create necessary tables in database when there were no .db file
        """

        create_table_reservations = '''
        CREATE TABLE reservations (
        id integer PRIMARY KEY,
        name text,
        surname text,
        r_start datetime,
        r_end datetime
        );
        '''

        try:
            self.cur.execute(create_table_reservations)
        except sqlError as err:
            print(err)

    def add_reservation(self, name: str, surname: str, r_start: dt.datetime, r_length: int):
        """
        Add reservation to database
        :param name: client's name
        :param surname: client's surname
        :param r_start: start time of the reservation
        :param r_length: length of the reservation in minutes
        """

        insert = f'''
        INSERT INTO reservations(name, surname, r_start, r_end) VALUES(?,?,?,?);
        '''
        params = (name, surname, r_start, r_start + dt.timedelta(minutes=r_length))

        try:
            self.cur.execute(insert, params)
            self.conn.commit()
        except sqlError as err:
            print(err)

    def get_interfering(self, start: dt.datetime, end=None):
        """
        Gets the reservations from selected time interval and which could interfere with given interval
        :param start: start of time interval
        :param end: end of time interval
        :return: list of reservations
        """

        select = 'SELECT r_start, r_end FROM reservations WHERE '
        if end is None:
            select += f'''r_start>'{start}' '''
        else:
            select += f'''(r_start<'{end-dt.timedelta(minutes=1)}' AND r_start>='{start}') '''
            select += f'''OR (r_end>'{start}' AND r_end<='{end}') '''
            select += f'''OR (r_start>='{start}' AND r_end<='{end}') '''
            select += f'''OR (r_start<'{start-dt.timedelta(minutes=1)}' AND r_end>'{end}') '''
        select += 'ORDER BY r_start ASC'

        try:
            self.cur.execute(select)
            return self.cur.fetchall()
        except sqlError as err:
            print(err)

    def get_schedule(self, start: dt.datetime, end: dt.datetime):
        """
        Get all reservations that fits in selected period
        :param start: start of provided range
        :param end: end of provided range
        :return: list reservations
        """

        select = f'''SELECT * FROM reservations WHERE r_start>='{start}' '''
        # to include reservations at end date add one day more to the ending point
        select += f'''AND r_start<'{end+dt.timedelta(days=1)}' '''
        select += 'ORDER BY r_start ASC'

        try:
            self.cur.execute(select)
            return self.cur.fetchall()
        except sqlError as err:
            print(err)

    def get_week(self, week: str, name=None, surname=None):
        """
        Gets all reservations from provided week of the year
        :param week: week of the year
        :param name: client's name for narrowing output
        :param surname: client's surname for narrowing output
        :return:
        """

        select = f'''SELECT * FROM reservations WHERE strftime('%W', r_start)='{week}' '''

        if (name and surname) is not None:
            select += f'''AND name='{name}' AND surname='{surname}' '''

        try:
            self.cur.execute(select)
            return self.cur.fetchall()
        except sqlError as err:
            print(err)

    def find_date(self, name: str, surname: str, r_start: dt.datetime):

        select = f'''SELECT * FROM reservations WHERE r_start='{r_start}' AND name='{name}' AND surname='{surname}' '''

        try:
            self.cur.execute(select)
            return self.cur.fetchall()
        except sqlError as err:
            print(err)

    def delete_reservation(self, name: str, surname: str, r_start: dt.datetime):

        delete = f'''DELETE FROM reservations WHERE r_start='{r_start}' AND name='{name}' AND surname='{surname}' '''

        try:
            self.cur.execute(delete)
            self.conn.commit()
        except sqlError as err:
            print(err)
