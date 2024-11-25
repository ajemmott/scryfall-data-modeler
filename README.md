# Scryfall Card Data Modeler

## Table of Contents
1. Introduction
2. Features  
2.2. Processed Card Layouts 
2.1. Encoded Categorical Variables  
3. Usage

## 1. Introduction

Magic: The Gathering (MTG) is a massively popular tabletop and digital trading card game with more than thirty years of history and development. As such, its designers are pushed to create paradigm-shifting gamepieces and mechanics that keep the game fresh and interesting for it's playerbase. This has lead to an expansive pool of gamepieces from which players can creatively choose to put together and play. The thing is, with so many gamepieces available, it is increasingly challenging and time-consuming to try to analyze and compare the properties of large batches of cards. Even with software tools, there so much diversity in how cards are designed that for at least every couple of months (past or future) a slightly different program might need to be coded to account for a given mechanic or card type.

With this tool I provide a **rough framework**, based on the observer design pattern, that uses events in order to flexibly coordinate how a set of software modules need to handle card data (obtained from a request to Scryfall's API) to attain the relevant features for a given use case while keeping a detailed log of the process. 

## 2. Project Structure

This project is composed of three **worker modules** and four **listener modules**. The worker modules are the ones that oversee general tasks and their steps to completion while triggering the events for listener modules, which in turn attend specific simple tasks in a as coordinated by workers. In addition to that there a small status object that keeps track of details acrosss details for any future reference if needed.

### 2.1. Listener Modules

* **worker listener (worker_module.py)**: It handles the transition between the stages of working with a given request (configuration, extraction, transformation, and load stages).

* **log listener (log_module.py)**: It handles all the front-side interface communication using the loguru logging package.

* **pandas listener (pandas_module.py)**: It handles all data transformation tasks using pandas.

* **io listener (io_module.py)**: It handles tasks that require user input like prompting and interpreting their response using regex when it comes to any deviation from what was initially requested.

### 2.2. Worker Modules

* **task_configurator**: It is in charge of the configuration of the argument parser (argparse) to enable the command-line interface. It can trigger events in the log and io modules.

* **api_client**: It is in charge of performing the api request, and evaluating its response accordingly. It can trigger events in the log and io modules.

* **data_processor**: It is in charge of coordinating a series of data transformations depending on what has been found in the api response. It can trigger events in the log and pandas modules.

## 3. How is Data Processed?
When modeling the data obtained via Scryfall's api there are two main ways in which the data is expected to be transformed. These are **layout-based model adaptations** for cards with non-standard layouts, and the **encoding of nomimal features** for categorical data.

### 3.1. Layout-based modeling



### 3.2. Encoded categorical features

Categorical features that take a reasonable number of nominal values are to be One-Hot Encoded to enable its use in ML algorithms.

#### Card Color

Given the five base colors in MTG: white (W), blue (U), black (B), red (R), and green (G); cards can be identified as being monocolored, multicolored or colorless. 

![](/readme-assets/card-color-intro.jpg)

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

## 3. Usage

Too make use of this tool you must run main.py as a script from the command line passing the appropiate arguments.

```
$ python <path-to-main.py> [QUERY_STRING] [OUTPUT_FILE]
```

For example, if you wanted to see all the cards from Strixhaven excluding the alchemy format rebalances and store it in a .csv file called `paper-stx.csv` then the command would look something like this:

```
$ python /path/to/script/main.py "set:stx -is:rebalanced" /output/path/paper-stx.csv
```

Check the -h option for a more detailed explanation.

Additional functionality is provided by adding the -r option which enables the option to store the response data as given by the api (without any structuring by my script other than aggregating the pages of the response) in a json file in the given path. 
