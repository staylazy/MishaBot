from datetime import datetime
import os
import time
import vk
import webbrowser
from post_date import PostDate

PICS_PER_DAY = 10

class ApiUser:
    def __init__(self, user_id, public_id, album, offset, count):
        self._id = int(user_id)
        self._public = -int(public_id)
        self._album = str(album).replace('\n', '')
        self._offset = int(offset) - 1
        self._count = int(count)

    def next_offset(self):
        self._offset += PICS_PER_DAY


class Bot:
    def __init__(self, token: str):
        self.__api = vk.API(vk.Session(access_token=token))
        open('log.txt', 'w').close()
        print(self.__api)

    def __data(self, user_id, offset, album):
        time.sleep(2)
        return self.__api.photos.get(owner_id=user_id, album_id=album,
                          rev=0, offset=offset, count=PICS_PER_DAY, v=5.131) 

    def __log(self, id, date, message):
        log = f"picture id: {id} | Date & time: {date} Attachments: {message}"
        print(log)
        with open('log.txt', 'a') as output:
            output.write(log + '\n')

    def __wall_post(self, public, picture, message, post_time, sid='', captcha=''):
        post = {} 
        tries = 0
        while (not post):
            if (0 < tries < 6):
                print(f"Failed to post. Retrying {tries}...")
            elif (tries > 6): 
                print("Failed to post. Check that the number of pending images is", 
                "less than 150 or that the image has already been uploaded and try again...")
                break
            tries += 1
            time.sleep(0.5)
            try:
                post = self.__api.wall.post(owner_id=public, attachments=picture, from_group=1,
                                 message=str(message) + '/10850', publish_date=post_time, v=5.131)
            except Exception as exc:
                if exc.code == 14:
                    webbrowser.open(exc.captcha_img)
                    sid = exc.captcha_sid
                    captcha = input("Captcha: ")
                    post = self.__api.wall.post(owner_id=public, attachments=picture, from_group=1,
                                     message=str(message) + '/10850', publish_date=post_time, 
                                     captcha_sid=sid, captcha_key=captcha, v=5.131)

    def post(self, user: ApiUser, day, month, year):
        mes = user._offset + 1
        date = PostDate(day=day, month=month, year=year)
        for _ in range(user._count // PICS_PER_DAY):
            post_timestamps = date.get_post_timestamps()
            data = self.__data(user._id, user._offset, user._album)['items']
            for i in range(PICS_PER_DAY):
                picture = data[i]
                post_time = post_timestamps[i]
                self.__log(id=picture.get('id'), date=datetime.fromtimestamp(post_time), message=mes)
                picture = f"photo{str(user._id)}_{picture.get('id')}"
                self.__wall_post(user._public, picture, mes, post_time)
                mes += 1
            user.next_offset()
            date.next_day()            
            print()


def main(): 
    info = []   
    with open('info.txt', 'r') as file:
        for line in file:
            info.append(line)
    info.append(line)
    token = info[2].replace('\n', '')
    user = ApiUser(user_id=info[0], public_id=info[1], album=info[3], offset=info[4], count=info[5])
    bot = Bot(token)
    bot.post(user, day=int(info[6]), month=int(info[7]), year=int(info[8]))

if __name__ == '__main__':
    main()
    os.system("pause")
