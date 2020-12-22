import re
from unicodedata import normalize

import requests
from bs4 import BeautifulSoup


def get_names(soup):
    """Retreives the name of the pokemon and additional forms (regional variants, megas, etc.) from the current page.
    Gigantamax pokemon are excluded because they don't have altered stats, abilities, or types."""
    # TO DO: Charizard returns two Gigantamax Charizard. Need to get rid of duplicates. Mega Charizard has hex decimal characters.

    names_list = []
    names_list_no_dups = []

    html_block = soup.find(id='mw-content-text').find('table',
                                                      class_='roundy', style='background:#FFF;')
    names_html = html_block.find_all(class_=('image'))

    for name in names_html:
        if name['title'].startswith('Gigantamax'):
            pass
        else:
            names_list.append(name['title'])

    for x in names_list:
        if x not in names_list_no_dups:
            names_list_no_dups.append(x)

    return names_list_no_dups


def get_types(soup):

    types_dict = {}

    html_block = soup.find(
        'a', title='Type').parent.find_next('table').find('tr')
    types_html = html_block.find_all(
        'td', {'style': lambda x: x != 'display: none;'}, recursive=False)

    for type_ in types_html:
        try:
            name = type_.find('small').text
        except Exception:
            name = soup.find(
                'a', href='/wiki/Pok%C3%A9mon_category').parent.find('b').text

        type1 = type_.find('tr').find('b').text
        type2 = type_.find('tr').find('b').find_next('b').text

        types_dict[name] = [type1]

        match = re.search('Unknown', type2)
        if match:
            types_dict[name].append(None)
        else:
            types_dict[name].append(type2)

    return types_dict


def get_abilities(soup):

    abilities_dict = {}

    html_block = soup.find('a', title='Ability').parent.find_next('table')
    abilities_html = html_block.find_all(
        'td', {'style': lambda x: x != 'display: none'})

    for ability_html in abilities_html:
        try:
            name = ability_html.find('small').text
        except Exception:
            name = soup.find(
                'a', href='/wiki/Pok%C3%A9mon_category').parent.find('b').text
        match = re.search('Hidden Ability', name)
        # HTML divides abilities by each form of a pokemon if alternate forms exist. The HTML considers hidden abilities
        # as their own form but is always listed after the forms that can have said hidden ability.
        if match:
            pass
        else:
            abilities_dict[name] = []

        abilities = ability_html.find_all('a')

        for ability in abilities:
            ability_name = ability.find('span').text
            if match:
                for previous_form in abilities_dict:
                    abilities_dict[previous_form].append(ability_name)
            else:
                abilities_dict[name].append(ability_name)

    return abilities_dict


def get_weights(soup):

    weights_dict = {}

    html_block = soup.find('a', title='Weight').parent.find_next('table')
    weights = html_block.find_all(
        'tr', {'style': lambda x: x != 'display:none;'})

    for weight in weights:
        try:
            name = weight.find_next_sibling('tr').find('td').text
        except:
            name = soup.find(
                'a', href='/wiki/Pok%C3%A9mon_category').parent.find('b').text

        w = weight.find('td').text
        try:
            re_result = re.findall('[0-9]+.[0-9]+', w)
            if len(re_result) == 0:
                continue
            else:
                weights_dict[name] = [re_result[0]]
        except:
            continue

    return weights_dict


def get_base_stats(soup):

    stats_dict = {}
    names_list = []
    name_counter = 0

    name_html = soup.find('a', href='/wiki/Pok%C3%A9mon_category').find_parent('tr').find_parent(
        'tr').find_next_sibling('tr')
    name_html = name_html.find_all('a', class_='image')
    print(name_html)
    for name in name_html:
        names_list.append(name.title)
        print(name.title)
    html_blocks = soup.find_all('a', href='/wiki/Statistic', title='Statistic')

    for html_block in html_blocks:

        html_block = html_block.parent.parent.parent

        # try:
        #     # name = html_block.find_previous_parent('h5').find('span').text
        #     name = html_block.find_previous_parent('table').find('span').text
        #     print(name)
        # except Exception:

        hp = html_block.find(
            'tr', style='background: #FF5959; text-align:center').find('div', style='float:right').string
        attack = html_block.find(
            'tr', style='background: #F5AC78; text-align:center').find('div', style='float:right').string
        defense = html_block.find(
            'tr', style='background: #FAE078; text-align:center').find('div', style='float:right').string
        sp_attack = html_block.find(
            'tr', style='background: #9DB7F5; text-align:center').find('div', style='float:right').string
        sp_def = html_block.find(
            'tr', style='background: #A7DB8D; text-align:center').find('div', style='float:right').string
        speed = html_block.find(
            'tr', style='background: #FA92B2; text-align:center').find('div', style='float:right').string
        stats_dict[names_list[name_counter]] = (
            hp, attack, defense, sp_attack, sp_def, speed)
        name_counter += 1

    return stats_dict


def get_next_pokemon(soup):

    next_pokemon = soup.find(
        id='mw-content-text').find(style='text-align: left').a['href']

    return next_pokemon


pokemon_dict = {}

current_URL = 'https://bulbapedia.bulbagarden.net/wiki/Bulbasaur_(Pokémon)'

for x in range(898):
    # try:
    page = requests.get(current_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    names = get_names(soup)
    for name in names:
        pokemon_dict[name] = get_types(soup).get(name), get_abilities(soup).get(
            name), get_weights(soup).get(name), get_base_stats(soup).get(name)
        print(name, pokemon_dict[name])
    current_URL = 'https://bulbapedia.bulbagarden.net' + get_next_pokemon(soup)

    # except:
    #     continue

# for name in names_list:

#     types_list = get_types(soup)
#     abilities_list = get_abilities(soup)
#     weights_list = get_weights(soup)
#     base_stats_list = get_base_stats(soup)

#     print(len(abilities_list)-len(names_list)+1)

#     try:
#         if counter == 0:
#             pokemon_dict[name] = types_list[type_counter:type_counter+2], abilities_list[0:len(
#                 abilities_list)-len(names_list)+1], weights_list[counter], base_stats_list[counter]
#         else:
#             pokemon_dict[name] = types_list[type_counter:type_counter +
#                                             2], abilities_list[counter], weights_list[counter], base_stats_list[counter]
#     except Exception:
#         continue
#     finally:
#         counter += 1
#         type_counter += 2

# print(pokemon_dict)
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
