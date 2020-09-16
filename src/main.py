import ctypes
import sys
import os
import selenium.webdriver
import requests
import datetime
from util import *
import argparse

SK_APPDATA = 'APPDATA'
SK_APPSETTINGS = 'APPSETTINGS'
STORAGEKEY_FILENAME_MAP = {
    SK_APPDATA: 'appdata.json',
    SK_APPSETTINGS: 'settings.json',
}

'''
retrives 
'''
def load_storage():
    # global STORAGEKEY_FILENAME_MAP
    # for storagekey, filename in STORAGEKEY_FILENAME_MAP:
        # localStorage.setItem(storagekey, load_json(f'./{filename}'))
    root = './src'
    localStorage.setItem(SK_APPDATA, load_json(f'{root}/appdata.json'))
    localStorage.setItem(SK_APPSETTINGS, load_json(f'{root}/settings.json'))
'''
writes
'''
def save_storage():
    # global STORAGEKEY_FILENAME_MAP
    # for storagekey, filename in STORAGEKEY_FILENAME_MAP:
        # dump_json(f'./{filename}', localStorage.getItem(storagekey))
    root = './src'
    dump_json(f'{root}/appdata.json', localStorage.getItem(SK_APPDATA))
    dump_json(f'{root}settings.json', localStorage.getItem(SK_APPSETTINGS))

def set_storage(id, key, value):
    obj = localStorage.getItem(id)
    obj[key] = value
    localStorage.setItem(id, obj)
def update_storage(id, key, default, callback):
    obj = localStorage.getItem(id)
    prev = obj[key] if key in obj else default
    obj[key] = callback(prev)
    localStorage.setItem(id, obj)

'''
updates localStorage with the latest pull info
'''
def record_latest_img_url(url):
    data = {
        'url': url,
        'timestamp': datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    }
    set_storage(SK_APPDATA, 'latest_url', data)
    def merge_history(prev):
        if prev[0]['url'] != data['url']:
            prev.insert(0, data)
        # else: print('already up-to-date')
        return prev
    update_storage(SK_APPDATA, 'history', [], merge_history)


'''
    Returns a string of a url to the latest image on Unsplash's 'wallpapers' topic
    url pattern: https://images.unsplash.com/photo-[0-9]*-[a-z0-9]
'''
def get_latest_img_url():
    latest_img_url = None
    with selenium.webdriver.Edge('msedgedriver.exe') as web_driver:
        web_driver.get('https://unsplash.com/t/wallpapers')
        el_latest_img = web_driver.find_element_by_css_selector('#app > div > div:nth-child(4) > div._3UDio._2sCnE.PrOBO._1CR66 > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(1) > figure > div > div > a > div > img')
        latest_img_url = el_latest_img.get_attribute('src')
        latest_img_url = latest_img_url[:latest_img_url.index('?')]
    record_latest_img_url(latest_img_url)
    return latest_img_url

'''
    downloads an image from a url
'''
def download_image_from_url(url, **options):
    OUT_DIR = options['outDir'] if 'outDir' in options else '.'
    FILE_EXT = options['fileExt'] if 'fileExt' in options else '.jpg'
    path = os.path.join(OUT_DIR, parse_filename_from_url(url, file_ext=FILE_EXT))
    with open(path, 'wb') as f:
        f.write(requests.get(url).content)

'''
usage:
    - ...
'''
def main():
    parser = argparse.ArgumentParser(
        prog='unsplashdaily',
        description='Sets a fresh new picture as your desktop wallpaper, from the motherload of course :)'
    )
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                     help='an integer for the accumulator')
    parser.add_argument('--output-dir', dest='output_dir', default='.',
                        help='specify an output directory')

    args = parser.parse_args()
    load_storage()
    latest_img_url = get_latest_img_url()
    download_image_from_url(latest_img_url)
    save_storage()

if __name__ == "__main__":
    main()