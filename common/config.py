import redis

r = redis.Redis()
cache_time = 3600 * 4  # 4 hours
default_encoding = 'windows-1251'
url = 'http://194.44.112.6/cgi-bin/timetable.cgi?n=700'
endpoints = {
    'groups': 'http://194.44.112.6/cgi-bin/timetable_export.cgi?req_type=obj_list&req_mode=group&OBJ_ID=&OBJ_name=&dep_name=&begin_date=&end_date=&req_format=html&coding_mode=UTF8&bs=ok',
    'teachers': 'http://194.44.112.6/cgi-bin/timetable_export.cgi?req_type=obj_list&req_mode=teacher&req_format=html&coding_mode=UTF8&bs=ok'
}
template = {
    "swagger": "3.0",
    "info": {
        "title": "Schedule API",
        "description": "API for IFNTUNG data",
        "contact": {
            "responsibleDeveloper": "Pavel Durmanov",
            "email": "flower.moor@gmail.com",
            "url": "https://ru.stackoverflow.com/users/236727/Павел-Дурманов?tab=profile",
        },
        "version": "0.0.1"
    },
}
