import argparse
from pathlib import Path
from loguru import logger

class JobConfig:

    def __init__(self):
        self.build_parser()        
        self.load_config()
    
    def build_parser(self):
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
            help=("The path to store the csv file containing the data "
                  "obtained after processing the query response"))

        self.parser.add_argument(
            '-r','--raw-output',
            type=Path,
            default=None,
            help=("The path to store the json file containing the "
                  "raw data in the query response"))
        
    def load_config(self):
        args = self.parser.parse_args()
        
        
        self.query_string = args.QUERY_STRING
        logger.info(f'Found query string [{self.query_string}]')
        
        self.processed_dest_path = args.PROCESSED_DATA_DESITNATION
        logger.info(f'Found destination path {self.processed_dest_path}')
        
        self.raw_dest_path = args.raw_output
        
        if self.raw_dest_path:
            logger.info(
                ("A copy of the raw query response will be stored "
                f"in {self.raw_dest_path}"))
        
        return