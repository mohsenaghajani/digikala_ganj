import json
import time
from concurrent.futures import ThreadPoolExecutor
from random import randrange
import requests
import glob
import re

headers = [
    {
        'authority': 'api.digikala.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie':'_sp_id.a330=09018744-65ad-4f05-9fca-b1a945818c33.1646510284.1.1646510733.1646510284.07b3cca0-150f-4542-a4c0-a16404fd5137; _ga_4S04WR965Q=GS1.1.1681873192.13.1.1681873954.0.0.0; _ga_LR50FG4ELJ=GS1.1.1681873192.13.1.1681873954.43.0.0; _ga=GA1.1.2031839200.1647496214; _hp2_id.1726062826=%7B%22userId%22%3A%223036804276007515%22%2C%22pageviewId%22%3A%221487584836170438%22%2C%22sessionId%22%3A%22458271072423937%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga_50CEWK5GC9=GS1.1.1695990541.1.1.1695990591.0.0.0; _sp_ses.13cb=*; DETECTOR_UID=DnQB-lJms-rDqg-Bd4F; TS0134ad67=010231059194224a340e754eba8ce50117e5d3ba340cf82a331279d7b02109d4e63ec1c597f5cee609d00c5d2a28369dc7f0ab3966; Digikala:User:Token:new=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1NzE4OTExNCwiZXhwaXJlX3RpbWUiOjE3MDM2NzU5MjUsInBheWxvYWQiOltdLCJwYXNzd29yZF92ZXJzaW9uIjoxLCJ0eXBlIjoidG9rZW4ifQ.yzL6WlcPydCstVSj86qDnzACOxEIS3d3-iKN7jQyXUQ; TS01b6ea4d=010231059158b0d425bf7d0286685d50852f942518125f1ae94e23bba55c939ead70d5324bf4f9a61dc2a78b24e7c87c8c90a22c3028b560206e9b4d60039cfe65804e7eba57ad4bf9fc0229337e742546e99e45fd489ea23f74f1d0bfdec5fcb2b446e42a; _sp_id.13cb=9bf2e797-cd21-4461-83ec-e4c2fa892832.1654350914.12.1701083925.1695990579.ca7d98e7-d85a-4bb8-a823-6a686c05915e.f98bb4d9-ebee-4c01-8c00-592892681580.a96f0081-1786-4329-9e2b-0a3dfd29f30b.1701083896674.25'
    },
    {
        'authority': 'api.digikala.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'cookie': '_hjSessionUser_2754176=eyJpZCI6IjE0MjIzNzIwLWMwNzYtNTM0MS05MTg4LTg2ZWY5MGQ2NDgwZiIsImNyZWF0ZWQiOjE2NDc0OTYyMTU3MDMsImV4aXN0aW5nIjp0cnVlfQ==; _ga_4S04WR965Q=GS1.1.1681873192.13.1.1681873954.0.0.0; _ga_LR50FG4ELJ=GS1.1.1681873192.13.1.1681873954.43.0.0; _ga=GA1.1.2031839200.1647496214; _ga_50CEWK5GC9=GS1.1.1695990541.1.1.1695990591.0.0.0; Digikala:User:Token:new=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0MzY1Mzc1MywiZXhwaXJlX3RpbWUiOjE3MDMxNDI1OTMsInBheWxvYWQiOltdLCJwYXNzd29yZF92ZXJzaW9uIjoxLCJ0eXBlIjoidG9rZW4ifQ.3vjRSsND_HxtJW1p0W9AOOp29aVxG4c47XlkouH84Qw; tracker_glob_new=a7ykFY4; tracker_session=5PQ4a33; TS01c77ebf=01023105919b90bb73fe350f0e6088c02e26a40a16bf68ea1a09d392c2941f3d19104962884078d09f21d7cc36618ef821e579a8e5dbf10ce90720d2f738fac1d2acc45ae96831eb5fb9180d3d334b01bd0d8eb0e3; _sp_ses.13cb=*; _hp2_ses_props.1726062826=%7B%22ts%22%3A1701016895865%2C%22d%22%3A%22www.digikala.com%22%2C%22h%22%3A%22%2F%22%7D; _sp_id.13cb=9bf2e797-cd21-4461-83ec-e4c2fa892832.1654350914.48.1701016969.1701004894.579d7070-2ff0-4716-9edf-303d158e6ca4.911f11bb-43f7-4f1b-bd2f-686eb97f874d.ed047310-813c-48a0-8c7c-0636e5298ffa.1701016892891.15; _ga_QQKVTD5TG8=GS1.1.1701016894.35.1.1701017015.0.0.0; _hp2_id.1726062826=%7B%22userId%22%3A%223036804276007515%22%2C%22pageviewId%22%3A%222644239490918273%22%2C%22sessionId%22%3A%222121783767735216%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D',
    }
    ]

# base_url = "https://api.digikala.com/v1/categories/home-appliance/search/?sort={sort}&seo_url=%2Fcategory-home-appliance%2F%3Fsort%3D{sort}&page={page}"
sort_list = [7, 1]


def get_headers():
    return headers[randrange(0, 2)]


def get_link_for_start():
    while True:
        response = requests.get('https://api.digikala.com/v1/treasure-hunt/', headers=get_headers(), timeout=10)
        link_map = response.json()
        link_map = link_map['data']['active_treasure']['treasure_map']['products_url']
        if link_map is not None:
            category = re.findall('category_([^"]+)/', link_map[0])
            start(category)
        print('does not start')


def start(category):
    for sort in sort_list:
        fromPage = 1
        toPage = 16
        for i in range(0, 7):
            main(fromPage, toPage, sort, category)
            fromPage += 15
            toPage += 15
            time.sleep(5)


def main(from_page, to_page, sort, category):
    executor = ThreadPoolExecutor(max_workers=20)
    for i in range(from_page, to_page):
        executor.submit(download_primary_pages, i, sort, category)
    # time.sleep(60)
    executor.shutdown(wait=True)
    time.sleep(1)


def download_primary_pages(page, sort, category):
    print(f"Downloading {page}")
    response = requests.get(f'https://api.digikala.com/v1/categories/{category}/search/?sort={sort}&page={page}', headers=get_headers(), timeout=1)
    main_link = response.json()
    url = main_link["data"]['products']
    for uri in url:
        download_product_page(uri['id'], sort, page)
        # products_id.append(uri['id'])


def download_product_page(id, sort, pages):
    print(id)
    url = f'https://api.digikala.com/v2/product/{id}/'
    response = requests.get(url, headers=get_headers(), timeout=10)
    page = response.json()
    image_links = page['data']['product']['images']['list']
    link_name = list()
    for url in image_links:
        link_image = url['url'][0]
        link_name.append(link_image)
    with open(f'images/product/test/{id}_{sort}_{pages}.json', 'w') as f:
        json.dump(link_name, f)


if __name__ == '__main__':
    get_link_for_start()



