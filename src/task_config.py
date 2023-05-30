import argparse
from pathlib import Path

class TaskConfig:

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=("Request, process, and store the results of "
                         "card data queries to scryfall's API."))

        self.parser.add_argument(
            "QUERY_STRING",
            help=("A string containing the keywords to filter card "
                  "data by. For search reference syntax see "
                  "https://scryfall.com/docs/syntax."))

        self.parser.add_argument(
            "PROCESSED_DATA_DESITNATION",
            type=Path,
            help=("The path to where the file containing the data "
                  "obtained after processing the query response will be created."))

        self.parser.add_argument(
            '-r','--raw-data-destination',
            type=Path,
            default=None,
            help=("enables the option to create a file containing the "
                  "raw data of the query response on the given path."))
        
    def load_config(self):
        args = self.parser.parse_args()
        
        self.query_string = args.QUERY_STRING
        self.processed_dest_path = args.PROCESSED_DATA_DESITNATION.resolve()
        
        if not args.raw_data_destination:
            self.raw_dest_path = None
            return
        
        self.raw_dest_path = args.raw_data_destination.resolve()
