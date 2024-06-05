import argparse
from pathlib import Path

class TaskConfigurator:

    def __init__(self, data_task):
        self.parent_task = data_task
        self.parser = argparse.ArgumentParser(
            description=("Request, process, and store the results of "
                         "card data queries to scryfall's API."))

        self.parser.add_argument(
            "QUERY_STRING",
            help=("A string containing the keywords to filter card "
                  "data by. For search reference syntax see "
                  "https://scryfall.com/docs/syntax."))

        self.parser.add_argument(
            "PROCESSED_DATA_DESTINATION",
            type=Path,
            help=("The path to where the file containing the data "
                  "obtained after processing the query response will be created."))

        self.parser.add_argument(
            '-r','--raw-data-destination',
            type=Path,
            default=None,
            help=("enables the option to create a file containing the "
                  "raw data of the query response on the given path."))
        
        return
        
    def load_config(self):
        args = self.parser.parse_args()
        self.do_mkdir = False
        self.query_string = args.QUERY_STRING
        self.processed_dest_path = args.PROCESSED_DATA_DESTINATION.resolve()
        
        if not self.processed_dest_path.parent.exists():
            
            # Triggers events in the io module
            self.parent_task.events.on_invalid_destination_path(self.parent_task)
            
            if not self.parent_task.status.logic_indicators['DO_PROCESSED_MKDIR']:
                # Trigger events in the log module
                self.parent_task.events.on_config_failed(self.parent_task)
                return
            # Trigger events in the log module
            self.parent_task.events.on_mkdir_flag_set(self.parent_task)
                
        
                
        if not args.raw_data_destination:
            self.raw_dest_path = None
            return
        
        self.raw_dest_path = args.raw_data_destination.resolve()
        
        return
