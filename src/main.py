import ctypes
import sys
import os
import selenium.webdriver
import requests
import datetime
from util import *

SK_APPDATA = 'APPDATA'
SK_APPSETTINGS = 'APPSETTINGS'
STORAGEKEY_FILENAME_MAP = {
    SK_APPDATA: 'appdata.json',
    SK_APPSETTINGS: 'settings.json',
}


def load_storage():
    # global STORAGEKEY_FILENAME_MAP
    # for storagekey, filename in STORAGEKEY_FILENAME_MAP:
        # localStorage.setItem(storagekey, load_json(f'./{filename}'))
    root = './src'
    localStorage.setItem(SK_APPDATA, load_json(f'{root}/appdata.json'))
    localStorage.setItem(SK_APPSETTINGS, load_json(f'{root}/settings.json'))
def save_storage():
    # global STORAGEKEY_FILENAME_MAP
    # for storagekey, filename in STORAGEKEY_FILENAME_MAP:
        # dump_json(f'./{filename}', localStorage.getItem(storagekey))
    root = './src'
    dump_json(f'{root}/appdata.json', localStorage.getItem(SK_APPDATA))
    dump_json(f'{root}settings.json', localStorage.getItem(SK_APPSETTINGS))

def set_storage_object(id, key, value):
    obj = localStorage.getItem(id)
    obj[key] = value
    localStorage.setItem(id, obj)

def record_latest_img_url(url):
    set_storage_object(SK_APPDATA, 'latest_url', {
        'url': url,
        'timestamp': datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    })


'''
    Returns a string of a url to the latest image on Unsplash's 'wallpapers' topic
'''
def get_latest_img_url():
    latest_img_url = None
    with selenium.webdriver.Edge('msedgedriver.exe') as web_driver:
        web_driver.get('https://unsplash.com/t/wallpapers')
        el_latest_img = web_driver.find_element_by_css_selector('#app > div > div:nth-child(4) > div._3UDio._2sCnE.PrOBO._1CR66 > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(1) > figure > div > div > a > div > img')
        latest_img_url = el_latest_img.get_attribute('src')
    
    return latest_img_url

def download_image_from_url(url, **options):
    OUT_DIR = options['outDir'] if 'outDir' in options else '.'
    FILE_EXT = options['fileExt'] if 'fileExt' in options else '.jpg'
    path = os.path.join(OUT_DIR, parse_filename_from_url(url, file_ext=FILE_EXT))
    with open(path, 'wb') as f:
        f.write(requests.get(url).content)

def main():
    load_storage()
    latest_img_url = get_latest_img_url()
    download_image_from_url(latest_img_url)
    save_storage()

if __name__ == "__main__":
    main()