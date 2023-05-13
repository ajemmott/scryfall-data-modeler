import argparse
from pathlib import Path
from rich import inspect

class JobConfig:

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="""request and store the results of card data queries
                    to scryfall's API""")

        self.parser.add_argument(
            "QUERY_STRING",
            help="""A string containing the keywords to filter card data by.
                    For search reference syntax see
                    https://scryfall.com/docs/syntax"""
        )

        self.parser.add_argument(
            "PROCESSED_DATA_DESITNATION",
            type=Path,
            help="""The path to store the csv file containing the data 
                    obtained after processing the query response"""
        )

        self.parser.add_argument(
            '-r','--raw-output',
            type=Path,
            default=None,
            help="""The path to store the json file containing the raw
                    data in the query response"""
        )
        
        self.load()
        
    def load(self):
        args = self.parser.parse_args()
        inspect(args)
        
        self.query_string = args.QUERY_STRING
        self.processed_dest_path = args.PROCESSED_DATA_DESITNATION
        self.raw_dest_path = args.raw_output
        return self