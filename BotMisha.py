import vk
import time
import os
import webbrowser

from datetime import datetime


try:
    info_file = open('info.txt', 'r')
except FileNotFoundError:
    print("Info file not found")
    time.sleep(100)

info = []

for line in info_file:
    info.append(line)

user_id = int(info[0])
pabl_id = int(info[1]) * -1
token = info[2]
album = info[3]
offset_pic = int(info[4]) - 1
value = int(info[5])

session = vk.Session(access_token=token)
print(session)
api = vk.API(session)

mes = offset_pic + 1
mes = str(mes)
# 8, 10, 11, 13, 15, 18, 20, 21, 22, 23
# 2 1 3 
one_hour = 3600
two_hours = 3600 * 2
three_hours = 3600 * 3

date = int(time.time()) + 30
str_date = time.strftime('%d%m%Y%H%M%S', time.localtime(date))


def new_month(month, list_date):
    month += 1
    list_date[2] = str(month // 10)
    list_date[3] = str(month % 10)
    list_date[0] = '0'
    list_date[1] = '1'


for i in range(value // 10):
    data = api.photos.get(owner_id=user_id, album_id=album,
                          rev=0, offset=offset_pic, count=10, v=5.131)
    offset_pic += 10
    list_date = list(str_date)
    list_date[8] = '0'
    list_date[9] = '8'
    list_date[10] = list_date[11] = list_date[12] = list_date[13] = '0'
    day = int(list_date[0]) * 10 + int(list_date[1])
    # print(day)
    month = int(list_date[2]) * 10 + int(list_date[3])
    year = int(list_date[4]) * 1000 + int(list_date[5]) * \
        100 + int(list_date[6]) * 10 + int(list_date[7])
    if month == 12 and day == 31:
        month = 1
        list_date[0] = '0'
        list_date[1] = '1'
        list_date[2] = str(month // 10)
        list_date[3] = str(month % 10)
        year += 1
        list_date[4] = str(year // 1000)
        list_date[5] = str((year // 100) % 10)
        list_date[6] = str((year // 10) % 10)
        list_date[7] = str(year % 10)
    elif month % 2 == 1 and day == 30:
        new_month(month, list_date)
    elif month % 2 == 0 and day == 31:
        new_month(month, list_date)
    elif month == 1 and day == 31:
        new_month(month, list_date)
    elif (month == 2 and day == 28 and
        (year % 4 != 0 or (year % 100 == 0 and year % 400 != 0))):
        new_month(month, list_date)
    elif (month == 2 and day == 29 and not
        (year % 4 != 0 or (year % 100 == 0 and year % 400 != 0))):
        new_month(month, list_date)
    else:
        day += 1
        list_date[0] = str(day // 10)
        list_date[1] = str(day % 10)
    str_date = ''.join(list_date)
    # print(str_date)
    date = int(time.mktime(time.strptime(str_date, '%d%m%Y%H%M%S')))
    time.sleep(2)
    print()
    for item in data['items']:
        print('id картинки: ', item.get('id'), "|", "Дата и время репоста: ",
              time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(date)),
              "|", "Attachments: ", mes)
        picture_id = item.get('id')
        picture = 'photo' + str(user_id) + '_'
        picture += str(picture_id)
        try:
            api.wall.post(owner_id=pabl_id, attachments=picture, from_group=1,
                        message=str(mes) + '/10850', publish_date=date, v=5.131)
        except Exception as exc:
            if exc.code == 14:
                webbrowser.open(exc.captcha_img)
                sid = exc.captcha_sid
                captcha = input("Требуется ввод капчи: ")
                api.wall.post(owner_id=pabl_id, attachments=picture, from_group=1,
                        message=str(mes) + '/10850', publish_date=date, captcha_sid=sid, captcha_key=captcha, v=5.131)
        # 8, 10, 11, 13, 15, 18, 20, 21, 22, 23
        # date += frequency
        unix_date_hour = int(datetime.fromtimestamp(date).hour)
        # 8-10 11-13 13-15 18-20 ----- 2
        # 10-11 20-21 21-22 22-23 ----- 1
        # 15-18 ----- 3
        if unix_date_hour == 8 or unix_date_hour == 11 or \
           unix_date_hour == 13 or unix_date_hour == 18:
            date += two_hours
        elif unix_date_hour == 10 or unix_date_hour == 20 or \
             unix_date_hour == 21 or unix_date_hour == 22:
            date += one_hour
        elif unix_date_hour == 15:
            date += three_hours
        mes = int(mes) + 1
        mes = str(mes)
os.system("pause")
