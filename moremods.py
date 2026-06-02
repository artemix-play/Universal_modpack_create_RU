from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas
import requests
import os
import re

def start(mods_list:list, version:str):
    version = version.lower()

    print(f"VERSION:{version}")

    Search_base = 'https://minecraft-inside.ru/mods/?q={}'

    global_mods = []

    site_base = urlparse(Search_base)
    site_base = f'{site_base.scheme}://{site_base.netloc}'
    
    site_base_ = requests.get(site_base)
    if site_base_.status_code != 200:
        print('Ошибка стайта: {}'.format(site_base_.status_code))
        exit()


    for mod_name in mods_list:

        url = Search_base.format(mod_name)

        site = requests.get(url)

        soup = BeautifulSoup(site.content.decode('utf-8'), 'html.parser')

        mods = soup.find_all('h2', class_="box__title")
        mods_ = []

        
        for mod in mods:
            mod = mod.find('a')
            name = mod.get_text()
            mod_url = mod.get('href')
            mods_.append({'url': site_base+mod_url, 'name': name})

        mods = pandas.DataFrame(mods_)


        print('Доступные моды по запросу: {}'.format(mod_name))
        for index, row in mods.iterrows():
            print(f'{index}. {row.get("name")}')
        print('10. Нету необходимого')

        try:
            in_user = int(input('> '))
            if in_user < 0 or in_user > 10:
                print('Ошибка радиуса')
                exit()

            if in_user == 10:
                print('Успешно')
                os.system('cls')
                continue

            mod = mods.loc[in_user]

            global_mods.append(mod)
            print('Успешно')
            os.system('cls')

        except Exception as e:
            print(f"Ошибка: {e}")
            exit()
    
    global_mods = pandas.DataFrame(global_mods).reset_index(drop=True)
    
    download_mods(global_mods, version)
    
def download_mods(list_mods:pandas.DataFrame, version:str):
    print('Скачивание модов...')
    os.makedirs('mods', exist_ok=True)
    for index, mod in list_mods.iterrows():
        site = requests.get(mod.get('url'))
        soup = BeautifulSoup(site.content.decode('utf-8'), 'html.parser')
        infos = soup.find_all('td', class_="dl__info")
        for info in infos:
            a_data = info.find('span', 'dl__name').get_text().replace('/quilt', "").replace('quilt', '').replace('Для', '')

            result = [
                    ' '.join([part for part in re.sub(r'\s*\([^)]*\)\s*', ' ', line).strip().split(' ') if part][:2])
                    for line in a_data.split('\n')][0]

            find = False

            if result == version:
                find = True
                break
            
        if find == True:
            link = info.find('span', 'dl__link').get_text()
            match_ = re.match(r'^\S+', mod.get('name'))
            filename = match_.group() if match_ else ''
            ref_link = get_full_url(link)

            path = os.path.join('mods', filename+'.jar')

            print(f'{path}...', end='\r')
            download_mod(link, ref_link, path)

        else:
            print(f'Для мода {mod.get("name")} не найдено подходящей версии...')

def get_full_url(short_url):
    response = requests.head(short_url)
    if response.status_code == 302:  # Если URL сокращён и происходит редирект
        headers = response.headers
        return headers["location"]
    return None

def download_mod(download_url, referer_url, output_filename=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": referer_url
    }
    session = requests.Session()
    session.headers.update(headers)

    resp = session.get(download_url, stream=True)
    if resp.status_code != 200:
        raise Exception(f"HTTP {resp.status_code}")

    content_type = resp.headers.get('content-type', '')
    if 'text/html' in content_type:
        raise Exception("Сервер вернул HTML, а не файл. Возможно, неверный Referer или нужна авторизация.")

    if not output_filename:
        # Пробуем вытащить имя из Content-Disposition
        cd = resp.headers.get('content-disposition')
        if cd and 'filename=' in cd:
            output_filename = cd.split('filename=')[1].strip('"')
        else:
            output_filename = download_url.split('/')[-1] or 'mod_file.jar'

    with open(output_filename, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"OK: {output_filename}")
