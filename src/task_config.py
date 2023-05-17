import argparse
from pathlib import Path

class TaskConfig:

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=("request, process, and store the results of "
                         "card data queries to scryfall's API"))

        self.parser.add_argument(
            "QUERY_STRING",
            help=("A string containing the keywords to filter card "
                  "data by. For search reference syntax see "
                  "https://scryfall.com/docs/syntax."))

        self.parser.add_argument(
            "PROCESSED_DATA_DESITNATION",
            type=Path,
            help=("The path to the csv file containing the data "
                  "obtained after processing the query response"))

        self.parser.add_argument(
            '-r','--raw-output',
            type=Path,
            default=None,
            help=("The path to the json file containing the "
                  "raw data in the query response"))
        
    def load_config(self):
        args = self.parser.parse_args()
        
        self.query_string = args.QUERY_STRING
        self.processed_dest_path = args.PROCESSED_DATA_DESITNATION.resolve()
        self.raw_dest_path = args.raw_output.resolve()
