import requests
import time
from User import UserVK, TOKEN


class SearchUsersVK():

    def __init__(self) -> None:
        self._user = []


    def _get_user(self, user) -> list:
        user.get_user_info()
        user.get_id_user_country()
        user.get_id_user_city()
        user.get_bdate_user()
        user.get_age_user()
        user.get_sex_user()
        user.get_user_id()
        user.get_user_name()
        self._user.append(user)


    def get_params_for_search(self) -> dict:
        city_id = 0
        country_id = 0
        age_user = 0
        sex_user = 0
        for user in self._user:
            city_id = user.city_id
            country_id = user.country_id
            age_user = user.age_user
            if user.sex_user == 2:
                sex_user = 1
            elif user.sex_user == 1:
                sex_user = 2
            #print(user.__dict__)
        return {
            'access_token': TOKEN,
            'v': 5.89,
            'sort': 0,
            'fields': 'photo_max_orig',
            'country': country_id,
            'city': city_id,
            'status': [1, 6, 5],
            'age_from': age_user - 3,
            'age_to': age_user + 3,
            'sex': sex_user
        }

    def search_users(self) -> dict:
        respons = requests.get(
        'https://api.vk.com/method/users.search',
        self.get_params_for_search()
        )
        time.sleep(0.34)
        return respons.json()

    def get_selected_users(self) -> list:
        data = self.search_users()['response']['items']
        list_found_users = []
        for user in data:
            if user['is_closed'] == False:
                #if len(list_found_users) < 5:
                list_found_users.append(user)
        for us in list_found_users:
            us['link'] = 'https://vk.com/id'+str(us['id'])
            #print(us)
        return list_found_users

    def get_users_with_foto(self) -> list:
        data = self.get_selected_users()
        users_with_foto = []
        for user in data:
            dict_photo = {}
            par = self.get_params_for_search()
            params = {
                'access_token': par['access_token'],
                'v': par['v'],
                'owner_id': user['id'],
                'album_id': 'profile',
                'extended': 1
            }
            respons = requests.get(
                'https://api.vk.com/method/photos.get',
                params
            )
            time.sleep(0.34)
            respons = respons.json()['response']['items']
            list_id_photo = self.get_3_photo(respons)
            #print(list_id_photo)
            for resp in respons:
                for value in list_id_photo:
                    if resp['id'] == value:
                        dict_photo[resp['id']] = resp['sizes']
                        #for val in resp['sizes']:
                            #if val['type'] == 'y':
                                #print(val['type'], val['url'])
            user['top_3_photo'] = []
            user['top_3_photo'].append(dict_photo)

        for user in data:
            if len(user['top_3_photo'][0]) == 3:
                users_with_foto.append(user)
        #print(users_with_foto)
        #for user in users_with_foto:
            #for us in user['top_3_photo']:
                #for key, value in us.items():
                    #for val in value:
                        #print(val)
        return users_with_foto


    def get_3_photo(self, respons) -> list:
        data = respons
        dict ={}
        list_id_photo = []
        for resp in data:
            #print(resp)
            dict.setdefault(resp['id'], (resp['likes']['count'] + resp['comments']['count']))
        #print(dict)
        sort_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        #print(sort_dict)
        if len(sort_dict) >= 3:
            for id in sort_dict[0:3]:
                list_id_photo.append(id[0])
        #print(list_id_foto)
        return list_id_photo

            #print(resp['id'], resp['sizes'], (resp['likes']['count'] + resp['comments']['count']))


if __name__ == '__main__':
    search_for_user = SearchUsersVK()
    search_for_user._get_user(UserVK(TOKEN))
    #search_for_user.get_params_for_search()
    #print(search_for_user.search_users())
    #search_for_user.get_selected_users()
    search_for_user.get_users_with_foto()
    #search_for_user.get_3_foto()
    #for us in search_for_user._user:
        #print(us.__dict__)
#{'token': '10b2e6b1a90a01875cfaa0d2dd307b7a73a15ceb1acf0c0f2a9e9c586f3b597815652e5c28ed8a1baf13c', 'country_id': 1,
# 'city_id': 106, 'age_user': 29, 'sex_user': 2, 'bdate_user': '15.5.1991', 'user_id': 552934290,
# 'user_name': 'Михаил_Афанасьевич'}
