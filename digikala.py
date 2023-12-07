import json
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from random import randrange
import re
import requests

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
        'cookie': 'tracker_glob_new=5t2cSBF; tracker_session=eYR6v29; TS01c77ebf=010231059112aa9c3e9e6c0d3da3f0fdc79ee31473561e5d555e0cedfe100fb189fafce90adfd6b201ba37abfedfe96ba543afa38567ef7ab8a116ff6de1b0fb7aac891a412be571af4d6cff7cec8a61a8957f98b6; _sp_ses.13cb=*; _ga=GA1.1.1004100182.1701017178; _hp2_ses_props.1726062826=%7B%22ts%22%3A1701017178786%2C%22d%22%3A%22www.digikala.com%22%2C%22h%22%3A%22%2F%22%7D; Digikala:User:Token:new=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1NzE4OTExNCwiZXhwaXJlX3RpbWUiOjE3MDM2MDkyMzMsInBheWxvYWQiOltdLCJwYXNzd29yZF92ZXJzaW9uIjoxLCJ0eXBlIjoidG9rZW4ifQ.bmGz6bkWWDqHmgrW5NL4y3UwConiJpCSMzP3DSPW--c; TS01b6ea4d=0102310591bd88635ae2494943b11807e4c0c87174561e5d555e0cedfe100fb189fafce90adfd6b201ba37abfedfe96ba543afa38567ef7ab8a116ff6de1b0fb7aac891a4197cd88b6e48ead11f43aabc2be6f6fa7fd1287ef3546943d17b367a08c25ea28; _ga_QQKVTD5TG8=GS1.1.1701017178.1.1.1701017262.0.0.0; _hp2_id.1726062826=%7B%22userId%22%3A%227010554305406023%22%2C%22pageviewId%22%3A%22879974437120005%22%2C%22sessionId%22%3A%226984774110833332%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _sp_id.13cb=f8fe9170-e5e8-41bb-af98-275f7eb45818.1701017177.1.1701017263..283e38e7-6ba3-4906-a742-34546d138094..bb801b76-c5c7-4344-8a23-0c3cbee02340.1701017177441.38',
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
fromPage = 1
toPage = 16
base_url = "https://api.digikala.com/v1/categories/baby-clothing/search/?seo_url=&page={0}"
products_id = []


def get_headers():
    return headers[randrange(0, 2)]


def main(from_page, to_page):
    executor = ThreadPoolExecutor(max_workers=20)
    for i in range(from_page, to_page):
        executor.submit(download_primary_pages, i, )
    # time.sleep(60)
    executor.shutdown(wait=True)
    time.sleep(1)


def download_primary_pages(i):
    print(f"Downloading {i}")
    response = requests.get(base_url.format(i), headers=get_headers(), timeout=10)
    main_link = response.json()
    url = main_link["data"]['products']
    for uri in url:
        download_product_page(uri['id'])


def get_number_images(image_link):
    number_image = (re.findall('_([^"]+).jpg', image_link))
    if len(number_image) != 0:
        return int(number_image[0])
    else:
        number_image = (re.findall('s/([^"]+).jpg', image_link))
        return int(number_image[0])


last_images_links = list()
def download_product_page(id):
    url = f'https://api.digikala.com/v2/product/{id}/'
    response = requests.get(url, headers=get_headers(), timeout=10)
    page = response.json()
    image_links = page['data']['product']['images']['list']
    link_name = dict()
    for url in image_links:
        link_image = url['url'][0]
        link_name[link_image] = get_number_images(link_image)
    last_image = max(link_name, key=link_name.get)
    with open(f'images/product/fe/{id}.json', 'w') as f:
        json.dump(link_name, f)
    save_image(last_image, id)


def save_image(image_link, name_image):
    res = requests.get(image_link, headers=get_headers(), stream=True)
    file_name = f'images2/{name_image}.jpg'
    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image successfully Downloaded: ', file_name)
    else:
        print('Image Could not be retrieved')


if __name__ == '__main__':
    for i in range(0, 11):
        main(fromPage, toPage)  # i for save images in separate folders
        fromPage += 15
        toPage += 15
        time.sleep(5)
        products_id.clear()
        last_images_links.clear()
