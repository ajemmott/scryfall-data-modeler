import numpy as np
import re

GAMEPLAY_FEATURES = ['id', 'name', 'layout', 'mana_cost', 'cmc', 
                     'type_line','oracle_text','colors', 'card_faces',
                     'rarity', 'power', 'toughness', 'loyalty', 
                     'image_uris']
    
CARD_FACE_FEATURES = ['image_uris', 'loyalty','mana_cost',
                      'colors','power','name','toughness','type_line',
                      'defense', 'oracle_text']

RELEVANT_TYPES = ['Snow','Legendary','Instant','Creature',
                        'Battle','Enchantment','Artifact','Land','Sorcery',
                        'Planeswalker']

MODAL_LAYOUTS = ['modal_dfc', 'adventure']

CONDITIONAL_LAYOUTS = ['transform', 'meld']

# A list of the relevant existing supertypes and card types
TYPE_MAP = { r_type: 'is_'+r_type.lower() for r_type in RELEVANT_TYPES}

COLOR_MAP = {
        'W': 'is_white',
        'U': 'is_blue',
        'B': 'is_black',
        'R': 'is_red',
        'G': 'is_green',
    }

def set_face_order(row):

    row['is_castable_face'] = []
    row['is_front_face'] = []
    
    # handle single face cards
    if row['layout'] not in ['transform', 'adventure', 'modal_dfc']:
        row['card_faces'] = [np.nan]
        row['is_castable_face'].append(True)
        row['is_front_face'].append(True)
        return row
    
    # handle modal dfcs
    if row['layout'] not in ['transform', 'meld']:
        for i, face in enumerate(row['card_faces']):
            row['is_castable_face'].append(True)
            row['is_front_face'].append(0 == i)
        return row
    
    # handle transforming dfcs
    for i, face in enumerate(row['card_faces']):
        row['is_castable_face'].append(0 == i)
        row['is_front_face'].append(0 == i)
    return row

def extract_card_face_features(row , features):
    
    if row['layout'] in (MODAL_LAYOUTS + CONDITIONAL_LAYOUTS):
        for feature in features:

            row_value = row['card_faces'].get(feature)

            if row_value:
                row[feature] = row_value
                continue

            row[feature] = np.nan

        return row

    return row

def get_cmc(mana_cost):

    mana_cost_pips = re.findall('{.+?}', mana_cost)
    
    cmc = 0
    for pip in mana_cost_pips:
        mana = pip.strip('{}').split('/')
        
        possible_costs = [eval_mana(symbol) for symbol in mana]
        cmc += max(possible_costs)
            
        
    return cmc

def eval_mana(symbol):
    if re.match('[0-9]+', symbol):
        return int(symbol)
    
    if re.match('[Xx]', symbol):
        return 0
    
    if re.match('[WUBRGPCSwubrgpcs]', symbol):
        return 1
    
    raise Exception

def set_mdfc_cmc(row):
    if row['layout'] == 'modal_dfc':
        row['cmc'] = get_cmc(row['mana_cost'])
    
    return row

# Defining a function to extract normal image uris
def extract_image_uris(row):
    for k, v in row['image_uris'].items():
        row[f'{k}_image_uri'] = v
    return row

# Defining a function to parse the type data from the type_line column
def parse_type_line(row, type_map):
    
    type_line = row['type_line'].split(' ')
    
    for type_name, type_flag in type_map.items():
        
            row[type_flag] = int(type_name in type_line)
    
    return row

def parse_colors(row, color_map):
    
    colors = row['colors']
    
    
    if not colors:
        row['n_colors'] = 0
        row['colors'] = 'colorless'
        row['is_colorless'] = 1

        for color, col_name in COLOR_MAP.items():
            row[col_name] = 0
            
        return row
    
    row['n_colors'] = len(colors)

    for color, col_name in COLOR_MAP.items():
        row[col_name] = int(color in colors)
    
    row['colors'] = ''.join(colors)
    row['is_colorless'] = 0

    return row
