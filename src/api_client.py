import json
from requests import get
from time import sleep
from rich import inspect
class ApiClient:
    def __init__(self, data_task):
        self.parent_task = data_task
    
    def request_cards(self):
        API_ENDPOINT = 'https://api.scryfall.com/cards/search?q='
        request = API_ENDPOINT + self.parent_task.config.query_string
        
        sleep(0.1)
        self.response = get(request)
        response_content = self.response.json()
        
        if not self.response.ok:
            self.parent_task.status_ok = False
            self.parent_task.events.on_bad_request(self.parent_task)
            return
        
        if 'warnings' in response_content.keys():
            self.response_warnings =  enumerate(response_content['warnings'])
            self.parent_task.events.on_warnings_found(self.parent_task)
        
        self.response_data = response_content['data']
        
        if response_content['has_more']:
            next_pages = self.aggregate_paginated_data(response_content['next_page'])
            self.response_data += next_pages
            
        return
    
    def save_raw_response(self):
        json_data = json.dumps(self.response_data)
        try:
            with open(self.parent_task.config.raw_dest_path, 'w') as f:
                f.write(json_data)
                
        except Exception:
            self.parent_task.events.on_raw_save_failed(self.parent_task)
        return
        
        
    def aggregate_paginated_data(self, new_page_url):
        
        sleep(0.1)
        new_page = get(new_page_url).json()
        
        if not new_page['has_more']:
            return new_page['data']

        next_page = self.aggregate_paginated_data(new_page['next_page'])
        return new_page['data'] + next_page