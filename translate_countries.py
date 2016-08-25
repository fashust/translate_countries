# -*- coding: utf-8 -*-

import asyncio
import json

import aiohttp


DATA_URL = (
    'https://gist.githubusercontent.com/'
    'fashust/b12f7469f481a1bc29f0e5bfb559e9d0/raw/'
    'f9fb4251ff9cc14a9d366cc85de612cea6d9692c/countries.json'
)
API_KEY = ('https://tech.yandex.ru/keys/')
BASE_API_URL = (
    'https://translate.yandex.net/api/v1.5/tr.json/translate?key={api_key}'
    '&text={origin_text}'
    '&lang={lang}'
)


async def get_origin_data(loop):
    session = aiohttp.ClientSession(loop=loop)
    async with session.get(DATA_URL) as response:
        response_data = await response.read()
    session.close()
    return json.loads(response_data.decode('utf-8'))


async def translate_data(data, loop):
    session = aiohttp.ClientSession(loop=loop)
    for key, val in data.items():
        url_data = {
            'api_key': API_KEY
        }
        if val.get('name_en'):
            url_data.update({
                'lang': 'en-uk',
                'origin_text': val['name_en']
            })
        elif not val.get('name_en') and val.get('name_ru'):
            url_data.update({
                'lang': 'ru-uk',
                'origin_text': val['name_ru']
            })
        else:
            continue
        url = BASE_API_URL.format(**url_data)
        async with session.post(url) as response:
            response_data = await response.read()
        json_response = json.loads(response_data.decode('utf-8'))
        translation = json_response['text'][0]
        val.update({'name_uk': translation})
    session.close()
    return data


def store_translated_data(data):
    with open('ru_en_uk_countries.json', 'w') as out:
        out.write(json.dumps(data, indent=4))



def main():
    loop = asyncio.get_event_loop()
    origin_data = loop.run_until_complete(get_origin_data(loop))
    translated_data =  loop.run_until_complete(
        translate_data(origin_data, loop)
    )
    store_translated_data(translated_data)


if __name__ == '__main__':
    main()
