import requests
from bs4 import BeautifulSoup
import re

URL = 'https://bulbapedia.bulbagarden.net/wiki/Bulbasaur_(Pok%C3%A9mon)'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='mw-content-text')
elems = results.find_all('table', class_='roundy')
weight_re = re.compile(r'\d+.\d+')

def get_name():
    pass

def get_type():
    # get_abilities() and get_weight() are set to sort through all six possible entiries, this function right now only
    # looks for the first type pairing and will need to be updated for alternate forms
    types_table = soup.find('a', title='Type').parent.find_next('table', style='margin:auto; background:none;')
    types = types_table.find_all('td', {'style': lambda x: x != ('display: none; width:50%;' or 'display: none;')})
    return [typ.find('span').text for typ in types]

def get_abilities():
    abilities_table = soup.find('a', title='Ability').parent.find_next('table')
    abilities = abilities_table.find_all('td', {'style': lambda x: x != 'display: none'})
    return [ability.find('span').text for ability in abilities]

def get_weight():
    weights_table = soup.find('a', title='Weight').parent.find_next('table')
    weights = weights_table.find_all('tr', {'style': lambda x: x != 'display:none;'})
    return [weight_re.findall(weight.text) for weight in weights]

def get_base_stats():
    hp = soup.find('tr', style='background: #FF5959; text-align:center').find('div', style='float:right').string
    attack = soup.find('tr', style='background: #F5AC78; text-align:center').find('div', style='float:right').string
    defense = soup.find('tr', style='background: #FAE078; text-align:center').find('div', style='float:right').string
    sp_attack = soup.find('tr', style='background: #9DB7F5; text-align:center').find('div', style='float:right').string
    sp_def = soup.find('tr', style='background: #A7DB8D; text-align:center').find('div', style='float:right').string
    speed = soup.find('tr', style='background: #FA92B2; text-align:center').find('div', style='float:right').string

    print(hp, attack, defense, sp_attack, sp_def, speed)

print(get_type())
print(get_abilities())
print(get_weight())
get_base_stats()