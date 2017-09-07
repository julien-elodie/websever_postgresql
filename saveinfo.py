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
    # get date
    date = item.get('createdDate')
    date = time.localtime(date / 1000)
    date = time.strftime("%Y-%m-%d %H:%M:%S", date)
    # get imgurl
    imgurl = item.get('imageHref')
    # get username
    username = item.get('user').get('nickname')
    # get poi
    if not item.get('poi').get('poiName'):
        poi = '地球某处'
    else:
        poi = item.get('poi').get('poiName')

    '''
    save data
    '''
    conn = psycopg2.connect(host='127.0.0.1', port=5432, user='julien-elodie', password='wyq2644756656', database='videoinfodb')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("insert into videobaseinfo(id, name, date, username, poi, imgurl) values(%s, %s, %s, %s, %s, %s);", (id, name, date, username, poi, imgurl))
    conn.commit()
    conn.close()
    print '成功写入数据～'
