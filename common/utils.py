import json
from collections import namedtuple
from functools import wraps

import requests
from bs4 import BeautifulSoup
from webargs import ValidationError

from common.config import *

base_lesson = namedtuple('Base', ['date', 'verb', 'lessons'])
lesson = namedtuple('Lesson', ['number', 'start', 'stop', 'description'])


def validate_kind(kind, obj):
    if obj.upper() in [x[kind[:-1]].upper() for x in get_full(kind)]:
        return True
    raise ValidationError(f'{kind[:-1]} does not exists')


def lists_cached(func):
    @wraps(func)
    def wrapper(kind):
        from_cache = r.get(kind)
        if not from_cache:
            results = func(kind)
            r.set(kind, json.dumps(results), ex=cache_time)
            return results
        return json.loads(from_cache)
    return wrapper


@lists_cached
def get_full(kind):
    results = []
    endpoint = endpoints[kind]
    content = requests.get(endpoint).text
    soup = BeautifulSoup(content, 'lxml').find_all('tr')
    for dep in soup[1:]:
        data = dep.find_all('td')
        results.append({'department': data[0].text,
                        kind[:-1]: data[1].text})
    return results


def get_raw_content(s_date, e_date, entity):
    payload = {
        'edate': e_date,
        'sdate': s_date
    }
    payload.update(entity)
    response = requests.post(url, data=payload)
    response.encoding = default_encoding
    return response.text


def serialize(data):
    return [
        {'date': base.date, 'verbose': base.verb, 'lessons': [
            {'number': single.number, 'from': single.start,
             'to': single.stop, 'description': single.description}
            for single in base.lessons
        ]}
        for base in data
    ]


def collect(containers, chair):
    result = []
    for container in containers:
        lessons = []
        date = container.h4.text.split()
        for each_tr in container.find_all('tr'):
            row = each_tr.find_all('td')
            if row[-1].get_text(strip=True):
                description = row[2].text.replace('\xa0', ' ')
                if not chair:
                    if description.strip() == chair_desc:
                        continue
                    description = description.replace(chair_desc, '')
                lesson_time = row[1].text[:5], row[1].text[5:]
                lessons.append(lesson(row[0].text, *lesson_time, description))
        result.append(base_lesson(*date, lessons))
    return serialize(result)


def parse(entity, from_date, to_date, chair):
    content = get_raw_content(from_date, to_date, entity)
    soup = BeautifulSoup(content, 'lxml').find_all('div', class_='container')
    containers = soup[1].find_all('div', class_='col-md-6')
    if not containers:
        return False
    return collect(containers, chair)
