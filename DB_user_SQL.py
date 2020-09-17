import json

import binary as binary
import psycopg2 as pg

from Search import SearchUsersVK
from User import UserVK, TOKEN

with pg.connect(database='test_DB_user', user='postgres', password='tvoug13777T', host='localhost', port='5432') as conn:
    cur = conn.cursor()

search_for_user = SearchUsersVK()
search_for_user._get_user(UserVK(TOKEN))

db_name = 'str'
for us in search_for_user._user:
        db_name = us.__dict__['user_name'] + '_id_' + str(us.__dict__['user_id'])

print(f'Поиск для пользователя VK {db_name}')


def create_db():
    cur.execute('''
        create table if not exists Users(
        id integer primary key, name varchar(100) not null, link varchar(100) not null);
        ''')

    cur.execute('''
        create table if not exists Photos(
        id integer primary key, link_photo text not null);
        ''')

    cur.execute('''
        create table if not exists User_Photo(
        id serial primary key,
        Users_id integer references Users(id),
        Photos_id integer references Photos(id));
        ''')
    pass

#['id']['first_name']['last_name']['link']['top_3_photo']:[{[{
def add_users_from_list():
    list_us = search_for_user.get_users_with_foto()
    for user in list_us:
        if user['id'] == '':
            print('Что-то пошло не так, пользователи не выбраны')
        else:
            cur.execute('''
                insert into Users(id, name, link) values (%s, %s, %s);
                ''', (user['id'], user['first_name'] + '_' + user['last_name'], user['link']))
    pass

def add_photo_from_list():
    list_us = search_for_user.get_users_with_foto()
    for user in list_us:
        if user['id'] == '':
            print('Что-то пошло не так, пользователи не выбраны')
        else:
            for photo in user['top_3_photo']:
                for key, value in photo.items():
                    link = []
                    for val in value:
                        if val['type'] == 'w' or val['type'] == 'z' or val['type'] == 'y' or val['type'] == 'x':
                            link = val['url']
                    cur.execute('''
                        insert into Photos(id, link_photo) values (%s, %s);
                        ''', (key, link))
    pass

def add_connect_user_photo():
    list_us = search_for_user.get_users_with_foto()
    for user in list_us:
        if user['id'] == '':
            print('Что-то пошло не так, пользователи не выбраны')
        else:
            for photo in user['top_3_photo']:
                for key in photo.keys():
                    cur.execute('''
                        insert into User_Photo(Users_id, Photos_id) values (%s, %s)
                        ''', (user['id'], key))
    pass

def get_users(request_number):
    if request_number == 1:
        cur.execute('''
        select * from Users LIMIT 10;
        ''')
    elif request_number >= 2:
        cur.execute('''
        select * from Users LIMIT 10 OFFSET 10;
        ''')
    for u in cur.fetchall():
        print(u)

def get_photo():
    cur.execute('''
    select * from Photos;
    ''')
    for p in cur.fetchall():
        print(p)

def get_user_whith_photo(request_number):
    if request_number == 1:
        cur.execute('''
        select u.id, u.name, u.link, p.id, p.link_photo from User_Photo up
        join Users u on u.id = up.Users_id
        join Photos p on p.id = up.Photos_id LIMIT 30
        ''')
    else:
        cur.execute('''
        select u.id, u.name, u.link, p.id, p.link_photo from User_Photo up
        join Users u on u.id = up.Users_id
        join Photos p on p.id = up.Photos_id LIMIT 30 OFFSET 30
        ''')
    db_users = cur.fetchall()
    #for up in cur.fetchall():
        #print(up)
    return db_users

if __name__ == '__main__':
    create_db()
    add_users_from_list()
    #get_users(2)
    add_photo_from_list()
    #get_photo()
    add_connect_user_photo()
    ten_users = get_user_whith_photo(1)
    with open(db_name, 'w', encoding='utf-8') as f:
        for user in ten_users:
            json.dump(user, f, ensure_ascii=False, indent=2)
