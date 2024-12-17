# Scryfall Card Data Modeler

## Table of Contents
1. Introduction
2. Project Structure  
    2.1. Listener Modules  
    2.2. Worker Modules  
3. How is Data Processed    
    3.1. Layout Based Modeling   
    3.2. Encoded Nomimal Features  
4. Usage

## 1. Introduction

Magic: The Gathering (MTG) is a massively popular tabletop and digital trading card game with more than thirty years of history and development. As such, its designers are pushed to create paradigm-shifting gamepieces and mechanics that keep the game fresh and interesting for it's playerbase. This has lead to an expansive pool of gamepieces from which players can creatively choose to put together and play. The thing is, with so many gamepieces available, it is increasingly challenging and time-consuming to try to analyze and compare the properties of large batches of cards. Even with software tools, there so much diversity in how cards are designed that for at least every couple of months (past or future) a slightly different program might need to be coded to account for a given mechanic or card type.

With this tool I provide a **rough framework**, based on the observer design pattern, that uses events in order to flexibly coordinate how a set of software modules need to operate around card data (obtained from a request to Scryfall's API) to attain the relevant features for a given use case while keeping a detailed log of the process. 

## 2. Project Structure

This project is composed of three **worker modules** and four **listener modules**. The worker modules are the ones that oversee general tasks and their steps to completion while triggering the events for listener modules, which in turn attend specific simple tasks as coordinated by workers. In addition to that there a status module that keeps track of details acrosss modules for any future reference if needed.

### 2.1. Listener Modules

* **worker listener (worker_module.py)**: It handles the transition between the stages while working with a given request (configuration, extraction, transformation, and load stages).

* **log listener (log_module.py)**: It handles all the front-side interface communication using the loguru logging package.

* **pandas listener (pandas_module.py)**: It handles all data transformation tasks using pandas.

* **io listener (io_module.py)**: It handles tasks that require user input like prompting and interpreting their response using regex like when handling unexpected errors during data transformations

### 2.2. Worker Modules

* **task_configurator**: It is in charge of the configuration of the argument parser (argparse) to enable the command-line interface. It can trigger events in the log and io modules.

* **api_client**: It is in charge of performing the api request for card data, and evaluating its response accordingly. It can trigger events in the log and io modules.

* **data_processor**: It is in charge of coordinating a series of data transformations depending on what has been found in the api response. It can trigger events in the log and pandas modules.

## 3. How is Data Processed?
When modeling the data obtained via Scryfall's api there are two main ways in which the data is expected to be transformed. These are **layout-based model adaptations** for cards with non-standard layouts, and the **encoding of nomimal features** for categorical data represented with strings.

### 3.1. Layout-based modeling

Usually any variation of the traditional card layout suggests a different play pattern and thus a slightly different way of modeling its data in order to keep a uniform schema that allows for comparison with other gamepieces. The most common examples of alternate layouts are multiface cards, which can be presented with a transform, modal, adventure, and meld layouts among others. 

In order to maintain a homogenous representation of multiface cards and single face cards we shift our attention form card objects to card faces. In other words, each face of a multiface card is observed independently in the data and the `is_castable_face` and `is_front_face` features are added to describe the nature of each independent face. `is_castable_face` is True when the labeled face can be played independently of it's other face when in hand. and `is_front_face` is True when the labeled face is the front face of the card, as this can be relevant for certain in-game interactions.


### 3.2. Encoded nominal features

Categorical features that take a reasonable number of nominal values are to be One-Hot Encoded to enable its use in ML algorithms.

#### Card Color

Given the five base colors in MTG: white (W), blue (U), black (B), red (R), and green (G); cards can be identified as being monocolored, multicolored or colorless. 

These colors are represented in the data with a string that contains the letter that represents each color (or none if colorless).

```
COLOR_MAP = {
        'W': 'is_white',
        'U': 'is_blue',
        'B': 'is_black',
        'R': 'is_red',
        'G': 'is_green',
    }
```

a function is to be applied to every row of the data in order to encode the `card_color` feature.

```
def parse_colors(row, color_map):
    
    colors = row['colors']
    
    row['n_colors'] = len(colors)
    
    if not colors:
        row['colors'] = 'colorless'
        row['is_colorless'] = 1

        for color, col_name in COLOR_MAP.items():
            row[col_name] = 0
            
        return row
    

    for color, col_name in COLOR_MAP.items():
        row[col_name] = int(color in colors)
    
    row['colors'] = ''.join(colors)
    row['is_colorless'] = 0

    return row
```

#### Type Line

Cards in MTG usually have any number of supertypes, types, and subtypes. These are presented as a line of text below the card art that starts with the supertypes if any, then  lists the card types (at least one is mandatory but there can be more), and if there are any subtypes this will be placed at the end after an Em Dash (—).

With a defined list of the existing supertypes and types this can be easily encoded into boolean features. Subtypes in the other hand can take too many different values (about 300) to be worth fully encoding.

```
# A list of the relevant existing supertypes and card types
RELEVANT_TYPES = [
    'Snow',
    'Legendary',
    'Instant',
    'Creature',
    'Battle',
    'Enchantment',
    'Artifact',
    'Land',
    'Sorcery',
    'Planeswalker'
    ]

TYPE_MAP = { r_type: 'is_'+r_type.lower() for r_type in RELEVANT_TYPES}
```
`Snow` and `Legendary` are supertypes, the rest are card types. 

The type line is also evaluated applying a function to every row of data.

```
def parse_type_line(row, type_map):
    
    type_line = row['type_line'].split(' ')
    
    for type_name, type_flag in type_map.items():
        
            row[type_flag] = int(type_name in type_line)
    
    return row

```
## 4. Usage

To make use of this tool you must run main.py as a script from the command line passing the appropiate arguments.

```
$ python <path-to-main.py> [QUERY_STRING] [OUTPUT_FILE]
```

For example, if you wanted to see all the cards from Strixhaven excluding the alchemy format rebalances and store it in a .csv file called `paper-stx.csv` then the command would look something like this:

```
$ python /path/to/script/main.py "set:stx -is:rebalanced" /output/path/paper-stx.csv
```

Check the -h option for a more detailed explanation.

Additional functionality is provided by adding the -r option which enables the option to store the response data as given by the api (without any structuring by my script other than aggregating the pages of the response) in a json file in the given path. 



