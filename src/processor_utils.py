import numpy as np
import re

GAMEPLAY_FEATURES = ['id', 'name', 'layout', 'mana_cost', 'cmc', 
                     'type_line','oracle_text','colors', 'card_faces',
                     'rarity', 'power', 'toughness', 'loyalty', 
                     'image_uris']
    
CARD_FACE_FEATURES = ['image_uris', 'loyalty','mana_cost',
                      'colors','power','name','toughness','type_line',
                      'defense', 'oracle_text']

RELEVANT_TYPES =['Snow','Legendary','Instant','Creature',
                        'Battle','Enchantment','Artifact','Land','Sorcery',
                        'Planeswalker']

TYPE_MAP = { r_type: 'is_'+r_type.lower() for r_type in RELEVANT_TYPES}

COLOR_MAP = {
        'W': 'is_white',
        'U': 'is_blue',
        'B': 'is_black',
        'R': 'is_red',
        'G': 'is_green',
        'colorless': 'is_colorless'
    }

def set_face_order(row):
    
    face_map = {
        0: 'front_face',
        1: 'back_face'}
    
    row['face_type'] = []
    
    if not (row['layout'] == 'transform' or row['layout'] == 'modal_dfc'):
        row['card_faces'] = [None]
        row['face_type'].append('front_face')
        return row
    
    for i, face in enumerate(row['card_faces']):
        row['face_type'].append(face_map[i])
    
    return row

def extract_card_face_features(row , features):
    
    if row['layout'] == 'transform' or row['layout'] == 'modal_dfc':
        for feature in features:
            try:
                row[feature] = row['card_faces'][feature]
            except KeyError:
                row[feature] = np.nan
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
    
    for segment in type_line:
        
        if re.match(r'[^a-zA-Z]', segment):
            continue
        
        if segment in type_map.keys():
            row[type_map[segment]] = 1
    
    return row

def parse_colors(row, color_map):
    
    #Check the color column
    colors = row['colors']
    
    row['n_colors'] = len(colors)
    
    if not colors:
        row['colors'] = 'colorless'
        row['is_colorless'] = 1
        return row
    
    row['colors'] = ''.join(colors)
    
    for color in colors:
        row[color_map[color]] = 1
    
    return row

