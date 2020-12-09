import requests
from bs4 import BeautifulSoup
import re

weight_re = re.compile(r'\d+.\d+')
pokemon_dict = {}

def get_name(soup):
    name = soup.find(id='mw-content-text').find(class_='roundy').find('b').text
    return name

def get_type(soup):
    # get_abilities() and get_weight() are set to sort through all six possible entiries, this function right now only
    # looks for the first type pairing and will need to be updated for alternate forms
    types_table = soup.find('a', title='Type').parent.find_next('table', style='margin:auto; background:none;')
    types = types_table.find_all('td', {'style': lambda x: x != ('display: none; width:50%;' or 'display: none;')})
    return [typ.find('span').text for typ in types]

def get_abilities(soup):
    abilities_table = soup.find('a', title='Ability').parent.find_next('table')
    abilities = abilities_table.find_all('td', {'style': lambda x: x != 'display: none'})
    return [ability.find('span').text for ability in abilities]

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

current_URL = 'https://bulbapedia.bulbagarden.net/wiki/Bulbasaur_(Pok%C3%A9mon)'

# TO DO: Make a way for it to stop at the last pokemon and not loop.
# Maybe use a named tuple instead?
for x in range(898):
    try:
        page = requests.get(current_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        pokemon_dict[get_name(soup)] = get_type(soup), get_abilities(soup), get_weight(soup), get_base_stats(soup)
        print(f'{get_name(soup)}: {pokemon_dict[get_name(soup)]}')
        current_URL = 'https://bulbapedia.bulbagarden.net' + get_next_pokemon(soup)

    except:
        continue