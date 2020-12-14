import requests
from bs4 import BeautifulSoup
from unicodedata import normalize
import re


weight_re = re.compile(r'\d+.\d+')
pokemon_dict = {}

def get_names(soup):
    """Retreives the name of the pokemon and additional forms (regional variants, mega, gigantamax, etc.) from the current page."""
    # TO DO: Charizard returns two Gigantamax Charizard. Need to get rid of duplicates. Mega Charizard has hex decimal characters.
    # TO DO: Remove Gigantamax names from list. Gigantamax pokemon don't have unique types or abilities.
    html_block = soup.find(id='mw-content-text').find('table', class_='roundy', style='background:#FFF;')
    names_html = html_block.find_all(class_=('image'))
    return [name['title'] for name in names_html]

def get_types(soup):

    html_block = soup.find('a', title='Type').parent.find_next('table').find('tr')
    types_html = html_block.find_all('td', {'style': lambda x: x != 'display: none;'}, recursive=False)
    print(types_html[0].find('b').text)
    return [type_.find('b').text for type_ in types_html]

def get_abilities(soup):

    html_block = soup.find('a', title='Ability').parent.find_next('table')
    abilities_html = html_block.find_all('td', {'style': lambda x: x != 'display: none'}).td
    return [ability.find('span').text for ability in abilities_html]

def get_weight(soup):

    weights_table = soup.find('a', title='Weight').parent.find_next('table')
    weights = weights_table.find_all('tr', {'style': lambda x: x != 'display:none;'})
    return [weight_re.findall(weight.text) for weight in weights]

def get_base_stats(soup):
    # There might be issues when a Pokemon has multiple forms with different stats.
    hp = soup.find('tr', style='background: #FF5959; text-align:center').find('div', style='float:right').string
    attack = soup.find('tr', style='background: #F5AC78; text-align:center').find('div', style='float:right').string
    defense = soup.find('tr', style='background: #FAE078; text-align:center').find('div', style='float:right').string
    sp_attack = soup.find('tr', style='background: #9DB7F5; text-align:center').find('div', style='float:right').string
    sp_def = soup.find('tr', style='background: #A7DB8D; text-align:center').find('div', style='float:right').string
    speed = soup.find('tr', style='background: #FA92B2; text-align:center').find('div', style='float:right').string

    return (hp, attack, defense, sp_attack, sp_def, speed)

def get_next_pokemon(soup):
    next_pokemon = soup.find(id='mw-content-text').find(style='text-align: left').a['href']
    return next_pokemon

current_URL = 'https://bulbapedia.bulbagarden.net/wiki/Charizard_(Pokémon)'
page = requests.get(current_URL)
soup = BeautifulSoup(page.content, 'html.parser')
print(get_types(soup))
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