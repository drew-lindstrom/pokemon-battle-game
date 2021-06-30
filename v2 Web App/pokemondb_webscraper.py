import requests
import pprint
from bs4 import BeautifulSoup


def get_pokemon_dict(pokemon_dict):
    url = 'https://pokemondb.net/pokedex/all'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    html_block = soup.find('table', id='pokedex').find('tbody').find_all('tr')

    for tr in html_block:
        stats_list = []

        td_list = tr.find_all('td')
        for td in td_list:
            if td['class'] == ['cell-num', 'cell-fixed']:
                continue

            elif td['class'][0] == 'cell-name':
                try:
                    name = td.find('small', class_='text-muted').text
                    if name.startswith('Mega') or name.startswith('Alolan') or name.startswith('Galarian') or name.endswith('Necrozma'):
                        pass
                    else:
                        main_name = td.find('a', class_='ent-name').text
                        name = main_name + ' - ' + name
                except Exception:
                    name = td.find('a', class_='ent-name').text

            elif td['class'][0] == 'cell-icon':
                type_1 = td.find('a').text
                try:
                    type_2 = td.find('a').find_next_sibling('a').text
                except:
                    type_2 = None

            elif td['class'][0] == 'cell-num':
                stats_list.append(td.text)

        stats_tuple = tuple(stats_list)
        pokemon_dict[name] = (type_1, type_2), stats_tuple

    return None


def get_moves_dict(moves_dict):
    url = 'https://pokemondb.net/move/all'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    html_block = soup.find('table', id='moves').find('tbody').find_all('tr')

    for tr in html_block:
        moves_list = []

        td_list = tr.find_all('td')
        for td in td_list:
            try:
                moves_list.append(td.span['title'])
            except:
                if td.text == '—':
                    moves_list.append(None)
                else:
                    moves_list.append(td.text)
        del moves_list[6]
        # Currently not printing the effect names and probability of effect happening.
        moves_dict[moves_list[0]] = tuple(moves_list[1:6])
    return None


pokemon_dict = {}
moves_dict = {}

get_pokemon_dict(pokemon_dict)
get_moves_dict(moves_dict)

with open('pokemon_list.txt', 'w') as f:
    pprint.pprint(pokemon_dict, f)
with open('moves_list.txt', 'w') as f:
    pprint.pprint(moves_dict, f)
