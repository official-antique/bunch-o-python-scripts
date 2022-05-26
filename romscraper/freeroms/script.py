import argparse
import concurrent.futures
import os
import re
import requests_cache
import sys
import wget

argument = sys.argv[1:][0].lower()
cached_session = requests_cache.CachedSession('roms_cache')

def get_all_endpoints(letter):
    try:
        page = cached_session.get(f'https://www.freeroms.com/{argument}_roms_{letter}.htm')
        return re.findall(f'(?:\/roms\/{argument}\/.*.htm)', page.text)
    except requests_cache.requests.RequestException as error:
        print('[!]: ', error)

def get_download_link(endpoint):
    try:
        page = cached_session.get(f'https://www.freeroms.com{endpoint}')
        return re.search(f'((?!=")http:\/\/download.freeroms.com.*(?="))', page.text)
    except requests_cache.requests.RequestException as error:
        print('[!]: ', error)

def download(endpoint):
    download_link = get_download_link(endpoint)
    _, file_name = download_link.rstrip('/').rsplit('/', 1)

    wget.download(download_link, out=f'{os.getcwd()}\\{argument}\\{file_name}')


if len(argument) > 0:
    for letter in list('#ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        endpoints = get_all_endpoints(letter)
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
            executor.map(download, endpoints)
else:
    print('Please provide a system available on freeroms.com as an argument.')