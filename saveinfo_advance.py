#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
import psycopg2
import psycopg2.extras

url = 'http://api.lvshiv.com/lvshiv/travelVideos/hotVideos'

headers = {
    'cache-control': "no-cache",
    'postman-token': "1c426f2a-86ed-5f17-2098-597dbcdab9c3"
    }

res = requests.get(url, headers=headers)

Json = json.loads(res.text)

for item in Json.get('content'):
    '''
    get info
    '''
    # get id
    id = item.get('id')
    # get name
    if item.get('name'):
        name = item.get('name')
    elif item.get('summary'):
        name = item.get('summary')
    else:
        name = ''
    # get videourl
    videourl = item.get('videoHref')
    # get username
    username = item.get('user').get('nickname')
    # get userimgurl
    if item.get('user').get('imageHref'):
        userimgurl = item.get('user').get('imageHref')
    else:
        userimgurl = '../images/person.png'
    # get intro
    intro = item.get('intro')

    '''
    save data
    '''
    conn = psycopg2.connect(host='127.0.0.1', port=5432, user='julien-elodie', password='wyq2644756656', database='videoinfodb')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("insert into videoadvanceinfo(id, name, videourl, username, userimgurl, intro) values(%s, %s, %s, %s, %s, %s);", (id, name, videourl, username, userimgurl, intro))
    conn.commit()
    conn.close()
    print '成功写入数据～'
