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
    stats_table = soup.find('a', title="Statistic").find_parent('table')
    stats = stats_table.find_all('div style="float:right"', {'sytle': lambda x: x != 'float:left'})
    print(stats)
    return [stat.text for stat in stats]

print(get_type())
print(get_abilities())
print(get_weight())
print(get_base_stats())