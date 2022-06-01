import datetime

class PostDate:
    def __init__(self, day, month, year):
        self.__day = day
        self.__month = month
        self.__year = year
        self.__date = datetime.datetime(day=self.__day, month=self.__month, year=self.__year, hour=0)  
        print('Date: ', self.__date)

    def next_day(self):
        self.__date += datetime.timedelta(days=1)
        self.__date = self.__date.replace(hour=0)

    def get_post_timestamps(self):
        times = [8, 10, 11, 13, 15, 18, 20, 21, 22, 23]
        result_dates = []
        for hour in times:
            self.__date = self.__date.replace(hour=hour)
            result_dates.append(self.__date.timestamp())
        return result_dates
