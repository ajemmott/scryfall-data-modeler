# Scryfall Card Data Modeler

Magic: The Gathering (MTG) is a massively popular tabletop and digital trading card game with more than thirty years of history and development. As such, its designers are pushed to create paradigm-shifting gamepieces and mechanics that keep the game fresh and interesting for it's playerbase. This has lead to an expansive pool of gamepieces from which players can creatively choose to put together and play. The thing is, with so many gamepieces available, it is increasingly challenging and time-consuming to try to analyze and compare the properties of large batches of cards. Even with software tools, there so much diversity in how cards are designed that for at least every couple of months (past or future) a slightly different program might need to be coded to account for a given mechanic or card type.

With this tool I provide a **rough framework**, based on the observer design pattern, that uses events in order to flexibly coordinate how a set of software modules need to handle card data (obtained from a request to Scryfall's API) to attain the relevant features for a given use case while keeping a detailed log of the process. 

## Usage

Too make use of this tool you must run main.py as a script from the command line passing the appropiate arguments.

```
$ python <path-to-main.py> [QUERY_STRING] [OUTPUT_FILE]
```

For example, if you wanted to see all the cards from Strixhaven excluding the alchemy format rebalances and store it in a file called `paper-stx.csv` then the command would look something like this:

```
$ python /path/to/script/main.py "set:stx -is:rebalanced" /output/path/paper-stx.csv
```

Currently the output file will be created as a csv file where every card face is treated as a separate row and all the image_uris have a separate column. Separate columns will be created for supertypes (legendary, basic, or snow) and types( creature, artifact, planeswalker, battle, etc.) Separate columns will also be created for card colors (i.e. `is_white` of `is_blue`).

Additional functionality is provided by adding the -r option which enables the option to store the response data as given by the api (without any structuring by my script other than aggregating the pages of the response) in a json file in the given path. 

Check the -h option for a more detailed explanation.