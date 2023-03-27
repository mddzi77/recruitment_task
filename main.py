import csv
import json
import datetime as dt
import os
from database import Database


class GoBackException(Exception):
    """Raised to goback to main menu"""
    pass



class App:

    def __init__(self):
        self.db = Database()

    @staticmethod
    def input_name():
        """
        Process of inputting the name
        :return: return to main menu flag, list[name, surname]
        """

        print('What\'s your name?')
        # input loop
        while True:

            comm = input('-> ').lower()

            # go back to main menu
            if comm in ['b', 'back']:
                os.system('CLS')  # reset output to default opening view
                raise GoBackException
            # exit program
            elif comm in ['q', 'quit']:
                exit()
            # split input to name and surname and check if input is correct
            else:
                name_surname = comm.split(' ')
                if len(name_surname) < 2:
                    print('Please give your full name and surname separated by space')
                elif len(name_surname) > 2:
                    print('Please give only full name and surname separated by space')
                else:
                    return name_surname

    @staticmethod
    def input_filename(file_format: str):
        """
        Gets name of the file to which schedule will be saved and checks if file already exists
        :return: full filename with format of the file
        """

        file_exist_flag = False  # flag to select conditions for the process
        print('Enter a file name')
        # input loop
        while True:

            comm = input('-> ').lower()

            if not file_exist_flag:
                try:
                    filename = comm + file_format  # connect file name and format

                    # checking if selected filename already exists
                    for f in os.scandir():
                        if filename == f.name:
                            raise FileExistsError

                    return filename
                except FileExistsError:
                    print(filename, 'file already exists, dou want to overwrite this file? (yes/no)')
                    file_exist_flag = True
            elif comm == 'yes' and file_exist_flag:
                return filename
            elif comm == 'no' and file_exist_flag:
                print('Enter a file name')
                file_exist_flag = False
            else:
                print('Unknown answer please write yes or no')

    def input_date_new(self, name_surname: list[str]):
        """
        Process of inputting date and time of reservation
        :param name_surname: previously provided name and surname of the client
        :return:  return to main menu flag, selected date as datetime object
        """

        print('When would you like to book? (DD.MM.YYYY HH:MM)')
        already_res_flag = False   # flag to select conditions for the process
        # input loop
        while True:

            comm = input('-> ').lower()

            # go back to main menu
            if comm in ['b', 'back']:
                os.system('CLS')  # reset output to default opening view
                print('Welcome to tennis court reservation')
                raise GoBackException
            # exit program
            elif comm in ['q', 'quit']:
                exit()
            # processing of answer to the proposal of the nearest available time
            elif comm == 'yes' and already_res_flag:
                return date_time
            elif comm == 'no' and already_res_flag:
                already_res_flag = False  # reset flag
                print('When would you like to book? (DD.MM.YYYY HH:MM)')
            elif comm not in ['yes', 'no'] and already_res_flag:
                print('Unknown answer please write yes or no')
            # processing of provided date and time
            else:
                try:
                    date_time = dt.datetime.strptime(comm, '%d.%m.%Y %H:%M')
                    time_now = dt.datetime.now()

                    # when provided data passed already
                    if date_time < time_now:
                        print('The date you selected has already expired, please select another date')
                    # when provided date is less than hour from now
                    elif date_time - time_now < dt.timedelta(hours=1):
                        print('Given time is less then hour from now, please choose another time')
                    # when provided date is already reserved
                    elif self.check_occupy(date_time) is not None:
                        date_time = self.check_occupy(date_time)
                        print('The time you chose is unavailable, would you like to make a reservation for',
                              f'''{date_time.strftime('%H:%M %d.%m.%Y')} instead? (yes/no)''')
                        already_res_flag = True
                    # when client has already more than two reservations in a week
                    elif len(self.db.get_week(date_time.strftime('%W'), name_surname[0], name_surname[1])) > 2:
                        print('You have more than 2 reservations this week, please choose another date')
                    else:
                        return date_time
                except ValueError:
                    print('Wrong format of date and time or values provide, please use DD.MM.YYYY HH:MM')

    def input_date_cancel(self, name_surname):
        """
        Process of inputting date and time of reservation
        :param name_surname: previously provided name and surname of the client
        :return:  return to main menu flag, selected date as datetime object
        """

        print('What was the time of the reservation? (DD.MM.YYYY HH:MM)')
        # input loop
        while True:

            comm = input('-> ').lower()

            # go back to main menu
            if comm in ['b', 'back']:
                os.system('CLS')  # reset output to default opening view
                raise GoBackException
            # exit program
            elif comm in ['q', 'quit']:
                exit()
            # processing of provided date and time
            else:
                try:
                    date_time = dt.datetime.strptime(comm, '%d.%m.%Y %H:%M')
                    time_now = dt.datetime.now()

                    # when provided data passed already
                    if date_time < time_now:
                        print('The date you selected has already expired, please select another date')
                    # when provided date is less than hour from now
                    elif date_time - time_now < dt.timedelta(hours=1):
                        print('Given time is less then hour from now, please choose another time')
                    # when given reservation doesn't exist
                    elif len(self.db.find_date(name_surname[0], name_surname[1], date_time)) == 0:
                        print('There is no reservation at given date, please give a proper date')
                    else:
                        return date_time
                except ValueError:
                    print('Wrong format of date and time or values provided, please use DD.MM.YYYY HH:MM')

    def input_length(self, date_time: dt.datetime, name_surname: list[str]):
        """
        Process of inputting date and time of reservation
        :param date_time: previously provided date of reservations
        :param name_surname: previously provided name and surname of the client
        :return:  selected length of reservation and date and time
        """

        already_res_flag = False  # flag to select conditions for the process

        print('How long would you like to book court?')
        if date_time.hour < 17:
            print('1) 30 Minutes\n2) 60 Minutes\n3) 90 Minutes')
        else:
            print('1) 30 Minutes\n2) 60 Minutes')

        # input loop
        while True:

            comm = input('-> ').lower()
            # remove characters that appeared in showed options
            comm = comm.replace(' ', '').replace(')', '').replace('minutes', '')

            # go back to main menu
            if comm in ['b', 'back']:
                os.system('CLS')  # reset output to default opening view
                raise GoBackException
            # exit program
            elif comm in ['q', 'quit']:
                exit()
            # when correct option is selected and length is not yet checked
            elif comm in ['1', '2', '3', '30', '60', '90'] and not already_res_flag:
                try:
                    length = int(comm)

                    # in case of selection number of an option change it to length in minutes
                    if length in [1, 2, 3]:
                        length = length * 30

                    # check if selected reservation length is available
                    # if not provide possible options
                    if self.check_occupy(date_time, length) is not None:

                        # check possible longest duration of reservation for selected date and time
                        for t in [60, 30]:
                            if self.check_occupy(date_time, t) is None:
                                by_date = t
                                break

                        # check the soonest possible time of reservation for selected length
                        by_length = self.check_occupy(date_time, length)
                        print('Your selected length of reservation is interfering with another reservation,'
                              'please choose one of below:')
                        print(f'1) Make reservation for {by_date} minutes at', date_time.strftime('%d.%m.%Y %H:%M'))
                        print(f'2) Make reservation for {length} minutes at', by_length.strftime('%d.%m.%Y %H:%M'))
                        print('3) Choose another date')
                        already_res_flag = True
                    else:
                        return length, date_time
                except ValueError:
                    print("Wrong value, please provide only one of the options showed below")
            # when selected length interfere with another reservation process answer to proposal options
            elif comm == '1' and already_res_flag:
                return by_date, date_time
            elif comm == '2' and already_res_flag:
                return length, by_length
            elif comm == '3' and already_res_flag:
                date_time = self.input_date_new(name_surname)

                print('How long would you like to book court?')
                already_res_flag = False  # reset flag
                if date_time.hour < 17:
                    print('1) 30 Minutes\n2) 60 Minutes\n3) 90 Minutes')
                else:
                    print('1) 30 Minutes\n2) 60 Minutes\n3) 90 Minutes')
            else:
                print("Wrong value, please provide only one of the options showed below")

    def new_reservation(self):
        """
        Add new reservation to database and schedule
        """

        os.system('CLS')  # clean output for clarity

        try:
            name_surname = self.input_name()  # client's name input
            date_time = self.input_date_new(name_surname)  # date and time of reservation
            length, date_time = self.input_length(date_time, name_surname)  # length of reservation
            # when all necessary data are collected
            self.db.add_reservation(name_surname[0], name_surname[1], date_time, length)
            print(f'''You successfulyy booked a court for {date_time.strftime('%d.%m.%Y %H:%M')}\n''')
        except GoBackException:
            # return to main menu
            pass

    def check_occupy(self, date_time: dt.datetime, length=30):
        """
        Checks occupancy of given time, if true then finds the soonest free time
        :param date_time: selected time of reservation
        :param length: length of reservation
        :return: None if given time is empty, the soonest time if selected time is already reserved
        """

        starting_point = date_time  # set start time to look for reservation
        ending_point = date_time + dt.timedelta(minutes=length)  # set end time to look for reservation

        # check if there are reservations in next 30 minutes
        if len(self.db.get_interfering(starting_point, ending_point)) >= 1:

            # find the closest free time of minimum 30 min
            res = self.db.get_interfering(starting_point)  # get list of reservations
            if len(res) == 1:
                return dt.datetime.fromisoformat(res[0][1])
            for i in range(1, len(res)):
                # time difference between current reservation and previous one
                diff = dt.datetime.fromisoformat(res[i][0]) - dt.datetime.fromisoformat(res[i - 1][1])
                if diff >= dt.timedelta(minutes=length):
                    return dt.datetime.fromisoformat(res[i - 1][1])
                # if its end of reservations list return end time of last reservation
                elif i == len(res):
                    return dt.datetime.fromisoformat(res[i][1])
        else:
            return None

    def cancel_reservation(self):
        """
        Cancel reservation and remove it from database and schedule
        """

        os.system('CLS')  # clean output for clarity

        try:
            name_surname = self.input_name()  # name input
            date_time = self.input_date_cancel(name_surname)  # date and time input
            self.db.delete_reservation(name_surname[0], name_surname[1], date_time)
            print('You cancelled your reservation\n')
        except GoBackException:
            pass

    def print_schedule(self):
        """
        Print a schedule in a given time period
        """

        os.system('CLS')  # clean output for clarity

        try:
            schedule, period = self.input_interval()
            today = dt.date.today()
            # get number of days in provided period of time
            days = period[1].date() - period[0].date()
            days = days.days

            os.system('CLS')  # clean output for clarity

            for d in range(days + 1):
                current_d = period[0] + dt.timedelta(days=d)
                current_d = current_d.date()
                # change printed date according to weekday
                if current_d == today:
                    print('Today:')
                elif current_d == today + dt.timedelta(days=1):
                    print('Tomorrow:')
                elif current_d == today - dt.timedelta(days=1):
                    print('Yesterday:')
                elif current_d.strftime('%W') == today.strftime('%W'):
                    print(current_d.strftime('%A:'))
                else:
                    print(current_d.strftime('%d.%m.%Y:'))
                counter = 0
                for r in schedule:
                    if current_d == dt.datetime.fromisoformat(r[3]).date():
                        print(f'\t{r[1]} {r[2]}',
                              f'''{dt.datetime.fromisoformat(r[3]).time().strftime('%H:%M')}''',
                              f'''- {dt.datetime.fromisoformat(r[4]).time().strftime('%H:%M')}''')
                        counter += 1
                if counter == 0:
                    print('\tNo reservations')
        except GoBackException:
            pass

    def save_schedule(self):
        """
        Save a schedule in a given time period
        """

        os.system('CLS')  # clean output for clarity

        try:
            schedule, period = self.input_interval()
            print('Choose file format (csv or json)')

            # select filename input loop
            while True:

                comm = input('-> ').lower().replace('.', '')

                # go back to main menu
                if comm in ['b', 'back']:
                    os.system('CLS')  # reset output to default opening view
                    raise GoBackException
                # exit program
                elif comm in ['q', 'quit']:
                    exit()
                # save to csv file
                elif comm == 'csv':
                    filename = self.input_filename('.csv')  # get filename
                    # prepare output
                    output = [['name', 'start_time', 'end_time']]
                    for r in schedule:
                        output.append([
                            f'{r[1]} {r[2]}',
                            dt.datetime.fromisoformat(r[3]).time().strftime('%H:%M'),
                            dt.datetime.fromisoformat(r[4]).time().strftime('%H:%M')
                        ])

                    with open(filename, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerows(output)
                    print('File saved succesfully!\n')
                    break
                # save to json file
                elif comm == 'json':
                    filename = self.input_filename('.json')  # get filename
                    days = period[1].date() - period[0].date()
                    days = days.days
                    output = {}

                    # save schedule to dictionary
                    for d in range(days + 1):
                        current_d = period[0] + dt.timedelta(days=d)
                        current_d = current_d.date()
                        output[current_d.strftime('%d.%m.%Y')] = []
                        for r in schedule:
                            row = {}
                            if current_d == dt.datetime.fromisoformat(r[3]).date():
                                row['name'] = f'{r[1]} {r[2]}'
                                row['start_time'] = dt.datetime.fromisoformat(r[3]).time().strftime('%H:%M')
                                row['end_time'] = dt.datetime.fromisoformat(r[4]).time().strftime('%H:%M')

                                output[current_d.strftime('%d.%m.%Y')].append(row)

                    with open(filename, 'w', newline='') as f:
                        output = json.dumps(output, indent='\t')
                        f.write(output)
                    print('File saved succesfully!\n')
                    break
        except GoBackException:
            pass

    def input_interval(self):
        """
        Get range of dates, process input and get reservations from selected period
        :return: list of reservations from given period, period
        """

        print('Please enter start and end for period for which You want to get schedule (DD.MM.YYYY-DD.MM.YYYY)')

        # input loop
        while True:

            comm = input('-> ').lower().replace(' ', '')

            # go back to main menu
            if comm in ['b', 'back']:
                os.system('CLS')  # reset output to default opening view
                raise GoBackException
            # exit program
            elif comm in ['q', 'quit']:
                self.db.conn.close()
                exit()
            try:
                period = comm.split('-')
                period = [dt.datetime.strptime(period[i], '%d.%m.%Y') for i in range(len(period))]
                if len(period) != 2:
                    print('Wrong period format, please use DD.MM.YYYY-DD.MM.YYYY')
                else:
                    # get start and end of a range from input
                    start = period[0] if period[0] < period[1] else period[1]
                    end = period[0] if period[0] > period[1] else period[1]
                    # to datetime
                    schedule = self.db.get_schedule(start, end)
                    return schedule, [start, end]
            except ValueError:
                print('Wrong format of date and time or values provided, please use DD.MM.YYYY-DD.MM.YYYY')

    def run(self):

        print('Welcome to tennis court reservation')

        while True:

            comm = input('-> ').lower()

            # quit program
            if comm in ['q', 'quit']:
                self.db.conn.close()
                break
            # make new reservation
            elif comm == 'make a reservation':
                self.new_reservation()
                print('Welcome to tennis court reservation')
            # cancel reservation
            elif comm == 'cancel a reservation':
                self.cancel_reservation()
                print('Welcome to tennis court reservation')
            # printing schedule
            elif comm == 'print schedule':
                self.print_schedule()
                print('\nWelcome to tennis court reservation')
            # save schedule to file
            elif comm == 'save schedule':
                self.save_schedule()
                print('Welcome to tennis court reservation')
            # help
            elif comm in ['h', 'help']:
                print('\nCommands list:')
                print('h or help            - print list of available commands')
                print('q or quit            - exit program (will not work while entering file name)')
                print('b or back            - go back to main menu (will not work while entering file name)')
                print('Make a reservation   - with given name and time of reservation adds it to schedule')
                print('Cancel a reservation - will delete your reservation from schedule')
                print('Print schedule       - will print all reservations from given period of time')
                print('Save schedule        - save schedule from given period of time to file')
                print('                       of your\'s selected file format and name')
                print('*commands are not case sensitive*\n')
                input('\nPress Enter to continue\n')
            # in case of unknown command
            else:
                print('Unknown command, type h or help to a list of possible commands')


if __name__ == '__main__':
    App().run()
