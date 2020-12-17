import requests
from bs4 import BeautifulSoup
from unicodedata import normalize
import re

pokemon_dict = {}

def get_names(soup):
    """Retreives the name of the pokemon and additional forms (regional variants, mega, gigantamax, etc.) from the current page."""
    # TO DO: Charizard returns two Gigantamax Charizard. Need to get rid of duplicates. Mega Charizard has hex decimal characters.
    # TO DO: Remove Gigantamax names from list. Gigantamax pokemon don't have unique types or abilities.
    html_block = soup.find(id='mw-content-text').find('table', class_='roundy', style='background:#FFF;')
    names_html = html_block.find_all(class_=('image'))
    return [name['title'] for name in names_html]

def get_types(soup):
    type_list = []

    html_block = soup.find('a', title='Type').parent.find_next('table').find('tr')
    types_html = html_block.find_all('td', {'style': lambda x: x != 'display: none;'}, recursive=False)
    for type_ in types_html:
        type_list.append(type_.find('tr').find('b').text)
        type_list.append(type_.find('tr').find('b').find_next('b').text)
    return type_list

def get_abilities(soup):
    # TO DO: Check to make sure abilities match up with different forms. Slowbro comes to mind.
    html_block = soup.find('a', title='Ability').parent.find_next('table')
    abilities_html = html_block.find_all('td', {'style': lambda x: x != 'display: none'}).td
    return [ability.find('span').text for ability in abilities_html]

def get_weights(soup):
    weight_list = []

    html_block = soup.find('a', title='Weight').parent.find_next('table')
    weights = html_block.find_all('tr', {'style': lambda x: x != 'display:none;'})
    for weight in weights:
        text = weight.find('td').text
        try:
            re_result = re.findall('[0-9]+.[0-9]+', text)
            if len(re_result) == 0:
                continue
            else:
                weight_list.append(re_result[0])
        except:
            continue
    return weight_list

def get_base_stats(soup):

    hp_html = soup.find_all('tr', style='background: #FF5959; text-align:center')
    attack_html = soup.find_all('tr', style='background: #F5AC78; text-align:center')
    defense_html = soup.find_all('tr', style='background: #FAE078; text-align:center')
    sp_attack_html = soup.find_all('tr', style='background: #9DB7F5; text-align:center')
    sp_def_html = soup.find_all('tr', style='background: #A7DB8D; text-align:center')
    speed_html = soup.find_all('tr', style='background: #FA92B2; text-align:center')

    stats_list = []
    print(stats_list)

    # print(hp_html)
    # for n in range(len(hp_html)):
    hp = hp_html.find('div', style='float:right').string
    attack = attack_html.find('div', style='float:right').string      
    defense = defense_html.find('div', style='float:right').string
    sp_attack = sp_attack_html.find('div', style='float:right').string
    sp_def = sp_def_html.find('div', style='float:right').string
    speed = speed_html.find('div', style='float:right').string
    
    stats_list[n].append((hp, attack, defense, sp_attack, sp_def, speed))

    # hp_html = soup.find_all('tr', style='background: #FF5959; text-align:center')
    # for hp in hp_html:
    #     stats_list[0].append(hp.find('div', style='float:right').string)
    #     counter += 1
    # attack_html = soup.find_all('tr', style='background: #F5AC78; text-align:center')
    # for attack in attack_html:
    #     stats_list[1].append(attack.find('div', style='float:right').string)
    # defense_html = soup.find_all('tr', style='background: #FAE078; text-align:center')
    # for defense in defense_html:
    #     stats_list[2].append(defense.find('div', style='float:right').string)
    # sp_attack_html = soup.find_all('tr', style='background: #9DB7F5; text-align:center')
    # for sp_attack in sp_attack_html:
    #     stats_list[3].append(sp_attack.find('div', style='float:right').string)
    # sp_def_html = soup.find_all('tr', style='background: #A7DB8D; text-align:center')
    # for sp_def in sp_def_html:
    #     stats_list[4].append(sp_def.find('div', style='float:right').string)
    # speed_html = soup.find_all('tr', style='background: #FA92B2; text-align:center')
    # for speed in speed_html:
    #     stats_list[5].append(speed.find('div', style='float:right').string)

    # for n in stats_list[0]:
    #     print(n)
        # stats.append(int(stats_list[0][n]))
        # , stats_list[1][n], stats_list[2][n], stats_list[3][n], stats_list[4][n], stats_list[5][n])
    return stats_list

def get_next_pokemon(soup):
    next_pokemon = soup.find(id='mw-content-text').find(style='text-align: left').a['href']
    return next_pokemon

current_URL = 'https://bulbapedia.bulbagarden.net/wiki/Charizard_(Pokémon)'
page = requests.get(current_URL)
soup = BeautifulSoup(page.content, 'html.parser')
print(get_base_stats(soup))
# pokemon_dict[get_name(soup)] = get_type(soup), get_abilities(soup), get_weight(soup), get_base_stats(soup)
# print(f'{get_name(soup)}: {pokemon_dict[get_name(soup)]}')

# TO DO: Make a way for it to stop at the last pokemon and not loop.
# Maybe use a named tuple instead?
# for x in range(898):
#     try:
#         page = requests.get(current_URL)
#         soup = BeautifulSoup(page.content, 'html.parser')
#         pokemon_dict[get_name(soup)] = get_type(soup), get_abilities(soup), get_weight(soup), get_base_stats(soup)
#         print(f'{get_name(soup)}: {pokemon_dict[get_name(soup)]}')
#         current_URL = 'https://bulbapedia.bulbagarden.net' + get_next_pokemon(soup)

#     except:
#         continue