import requests


class DateUtil():
    def __init__(self, country):
        self.country = country

    def is_leap_year(self, year):
        """
        source: https://en.wikipedia.org/wiki/Leap_year#Algorithm
        :param year: year of interest
        :return: True if Leap Year, False if not
        """
        if year % 4 != 0:
            return False
        elif year % 100 != 0:
            return True
        elif year % 400 != 0:
            return False
        else:
            True

    def get_holidays(self):
        return

    def is_holiday(self, date):
        """
        finds if day is a holiday
        :param country: Country code in 2 character string ex) Korea -> KR, Canada -> CA
        :param date: Date in form of tuple (YYYY, MM, DD)
        :return:
        """
