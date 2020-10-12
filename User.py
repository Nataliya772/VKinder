import requests
import time
from datetime import datetime

from Get_token import get_token

TOKEN = '10b2e6b1a90a01875cfaa0d2dd307b7a73a15ceb1acf0c0f2a9e9c586f3b597815652e5c28ed8a1baf13c'
#TOKEN = get_token()


class UserVK():
#KeyError: если не корректный ключ

    def __init__(self, token: str) -> None:
        self.token = token
        self.params = {'access_token': TOKEN, 'v': 5.89,}
        self.user = requests.get(
            'https://api.vk.com/method/account.getProfileInfo',
            self.params).json()['response']
        self.country_id = 0
        self.city_id = 0
        self.age_user = 0
        self.sex_user = 0
        self.bdate_user = 'str'
        self.user_id = 'int'
        self.user_name = 'str'


    def get_user_id(self) -> int:
        self.user_id = self.user['id']
        return self.user_id

    def get_user_name(self) -> str:
        self.user_name = self.user['first_name'] + '_' + self.user['last_name']
        return self.user_name

    def get_all_countries(self) -> list:
        params = self.params
        params['need_all'] = 1
        try:
            respons = requests.get(
                'https://api.vk.com/method/database.getCountries',
                params
            )
            time.sleep(0.34)
            return respons.json()['response']['items']
        except KeyError as e:
            print(f'Проблема с параметром access_token или подключение прервано, исключение {e}')


    def get_id_user_country(self) -> int:
        try:
            if self.user['country']['id'] > 0:
                self.country_id = self.user['country']['id']
            else:
                us_country = input('Укажите страну проживания: ')
                for country in self.get_all_countries():
                    if us_country == country['title']:
                        self.country_id = country['id']
                        break
                else:
                    print('Такой страны нет в списке, проверьте корректность указанного названия')
            return self.country_id
        except KeyError as e:
            print(f'Проблема с параметром access_token или подключение прервано, исключение {e}')
            return None


    def get_all_cities(self) -> list:
        params = self.params
        params['country_id'] = self.country_id
        respons = requests.get(
        'https://api.vk.com/method/database.getCities',
        params
        )
        time.sleep(0.34)
        return respons.json()['response']['items']

    def get_id_user_city(self) -> int:
        if self.user['city']['id'] > 0:
            self.city_id = self.user['city']['id']
        else:
            us_city = input('Укажите город проживания: ')
            for cities in self.get_all_cities():
                if us_city == cities['title']:
                    self.self.city_id = cities['id']
                    break
            else:
                print('Такого города нет в списке, проверьте корректность указанного названия')
        return self.city_id

    def get_bdate_user(self) -> str:
        try:
            if  self.user['bdate'] == '0.0.0':
                self.bdate_user = input('Укажите дату вашего рождения строго в формате день.месяц.год (01.01.1990): ')
            else:
                self.bdate_user = self.user['bdate']
            return self.bdate_user
        except TypeError or ValueError as e:
            print(f'Проверьте корректность формата указанной даты, должен быть 00.00.0000 - {e}')
            return None
#ValueError: time data '09-10-1981' does not match format '%d.%m.%Y'

    def get_age_user(self) -> int:
        try:
            dob = datetime.strptime(self.bdate_user, '%d.%m.%Y')
            today = datetime.now()
            self.age_user = today.year - dob.year
            if (today.month == dob.month == 2 and
                    today.day == 28 and dob.day == 29):
                pass
            elif today.month < dob.month or \
                    (today.month == dob.month and today.day < dob.day):
                self.age_user -= 1
            return self.age_user
        except ValueError or TypeError as e:
            return f'Проверьте корректность формата указанной даты, должен быть 00.00.0000 - {e}'

    def get_sex_user(self) -> int:
        self.sex_user = self.user['sex']
        return self.sex_user


if __name__ == '__main__':
    User_1 = UserVK(TOKEN)
    #print(User_1.get_user_info())
    #print(User_1.get_user_id())
    #print(User_1.get_user_name())
    print(User_1.get_id_user_country())
    #print(User_1.get_id_user_city())
    #print(User_1.get_all_countries())
    print(User_1.get_all_cities())
    #print(User_1.city_id)
    #print(User_1.get_bdate_user())
    #print(User_1.get_age_user())
    #print(User_1.get_sex_user())
    print(User_1.user)
