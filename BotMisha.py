import vk
import time
import os

user_id = int(input('ID страницы: '))
pabl_id = int(input('ID группы: ')) * -1
token = input('token: ')

session = vk.Session(access_token=token)

api = vk.API(session)

album = input('ID альбома: ')
if album.isdigit():
    album = int(album)
offset_pic = int(input('Offset картинка: ')) - 1
value = int(input('Количество: '))
while(value % 6 != 0):
    value = int(input('Количество: '))

mes = offset_pic + 1
mes = str(mes)
frequency = 10800
date = int(time.time()) + 30
str_date = time.strftime('%d%m%Y%H%M%S', time.localtime(date))


def new_month(month, list_date):
    month += 1
    list_date[2] = str(month // 10)
    list_date[3] = str(month % 10)
    list_date[0] = '0'
    list_date[1] = '1'


for i in range(value // 6):
    data = api.photos.get(owner_id=user_id, album_id=album,
                          rev=0, offset=offset_pic, count=6, v=5.77)
    offset_pic += 6
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
        api.wall.post(owner_id=pabl_id, attachments=picture, from_group=1,
                      message=str(mes) + '/10850', publish_date=date, v=5.77)
        date += frequency
        mes = int(mes) + 1
        mes = str(mes)
os.system("pause")
