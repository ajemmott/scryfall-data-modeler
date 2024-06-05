# Scryfall Card Data ETL Tool

This is a tool to perform card data queries via the scryfall API for MTG gameplay relevant features from the command line, structuring the response to store it locally as a resource for data analysis. 

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
## Whats next for this project

I plan to keep improving the functionality and implementation of this tool with time but i'm not on a strict timeline to do so. 

I'd love to recieve any sort of feedback or attend any reasonable request about the software, so feel free to reach out. 
