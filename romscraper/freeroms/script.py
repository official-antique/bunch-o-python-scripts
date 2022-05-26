import concurrent.futures, os, re, requests_cache, sys, wget

cached_session = requests_cache.CachedSession('roms_cache', expire_after=7)

def get_all_endpoints(system, letter):
    try:
        page = cached_session.get(f'https://www.freeroms.com/{system}_roms_{letter}.htm')
        return re.findall(f'((?!=")\/roms\/{system}\/.*.htm(?="))', page.text)
    except requests_cache.requests.RequestException as error:
        print('[FAIL]:', error)

def get_download_link(endpoint):
    try:
        page = cached_session.get(f'https://www.freeroms.com{endpoint}')
        return re.search(f'((?!=")http:\/\/download.freeroms.com.*(?="))', page.text).group()
    except requests_cache.requests.RequestException as error:
        print('[FAIL]:', error)

def download(endpoint):
    download_link = get_download_link(endpoint)
    _, file_name = download_link.rstrip('/').rsplit('/', 1)
    path = f'{os.getcwd()}\\{system}\\{file_name}'
    
    if not os.path.exists(path):
        if wget.download(download_link, out=path, bar=None):
            print(f'[SUCCESS]: {file_name} downloaded successfully')
        else:
            print(f'[FAIL]: {file_name} failed to download.')
    else:
        print(f'[FAIL]: {file_name} already exists.')


def main(system):
    endpoints = []
    for letter in list('#ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        endpoints.extend(get_all_endpoints(system, letter))
        print('[SUCCESS]: Obtaining all rom page endpoints for', letter)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(download, endpoints)
    

global system
if __name__ == '__main__':
    arguments = sys.argv[1:]
    systems = [
        'amiga', 'amstrad_cpc', 'atari', 'atari_jaguar',
        'atari_lynx', 'colecovision', 'cps2', 'game_gear',
        'genesis', 'gameboy_color', 'gba', 'intellivision',
        'mame', 'neogeo', 'neogeo_pocket', 'nes',
        'n64', 'nds', 'nintendo_gamecube', 'psx',
        'psp', 'raine', 'sega_cd', 'sega_dreamcast',
        'sega_master_system', 'sega_genesis_32x', 'snes', 'tg16',
        'wonderswan'
    ]
    
    if len(arguments) == 1:
        argsystem = arguments[0]
        if argsystem in systems:
            system = argsystem

            print('[SUCCESS]: Found valid system for freeroms.com.')
            system_path = f'{os.getcwd()}\\{system}'
            if not os.path.exists(system_path):
                print('[SUCCESS]: Creating directory for', system)
                os.makedirs(system_path)
            main(system)
        else:
            print('[FAIL]: Invalid system found.')
    else:
        print('[FAIL]: No system argument found.')