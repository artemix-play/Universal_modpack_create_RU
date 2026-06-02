from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas
import requests

def start(Search_base: str, mod_name:str):

    Search_base = 'https://minecraft-inside.ru/mods/?q={}'

    url = Search_base.format(mod_name)

    site = requests.get(url)
    if site.status_code != 200:
        print('Ошибка стайта: {}'.format(site.status_code))
        exit()

    soup = BeautifulSoup(site.content.decode('utf-8'), 'html.parser')



    title = soup.find('title').text
    mods = soup.find_all('h2', class_="box__title")
    mods_ = []

    site_base = urlparse(Search_base)
    site_base = f'{site_base.scheme}://{site_base.netloc}'

    for mod in mods:
        mod = mod.find('a')
        name = mod.get_text()
        mod_url = mod.get('href')
        mods_.append({'url': site_base+mod_url, 'name': name})

    mods = pandas.DataFrame(mods_)


    print(title)
    print('Доступные моды по запросу: {}'.format(mod_name))
    for index, row in mods.iterrows():
        print(f'{index}. {row.get("name")}')

    try:
        in_user = int(input('> '))
        if 0 < in_user <= 9:
            print('Ошибка радиуса')
            exit()

        mod = mods.loc[in_user]

        print(f'Открытие {mod.get("name")}...')

    except Exception as e:
        print(f"Ошибка: {e}")
        exit()