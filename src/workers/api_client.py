import json
from requests import get
from time import sleep

class ApiClient:
    def __init__(self, data_task):
        self.parent_task = data_task
    
    def aggregate_next_page(self, new_page_url):
        
        sleep(0.2)
        new_page = get(new_page_url).json()
        
        if not new_page['has_more']:
            return new_page['data']

        next_page = self.aggregate_next_page(new_page['next_page'])
        return new_page['data'] + next_page
    
    def request_cards(self):
        API_ENDPOINT = 'https://api.scryfall.com/cards/search?q='
        request = API_ENDPOINT + self.parent_task.config.query_string
        
        # Triggers events in the log module
        self.parent_task.events.on_request_setup(self.parent_task)
        
        sleep(0.2)
        self.response = get(request)
        self.response_content = self.response.json()
        
        return
    
    def evaluate_request_response(self):
        
        if not self.response.ok:
            self.parent_task.status.set_flag(
                flag_type='integrity',
                flag_name='EXTRACTION_COMPROMISED',
                flag_value=True
            )
            self.response_details = self.response_content['details']
            
            # Triggers events in the log module
            self.parent_task.events.on_bad_request(self.parent_task)
            return
        
        if 'warnings' in self.response_content.keys():
            self.response_warnings =  enumerate(self.response_content['warnings'])
            
            # Triggers events in the io and log modules
            self.parent_task.events.on_warnings_found(self.parent_task)
        
        if self.parent_task.status.test_integrity_compromised():
            return
        
        # Triggers events in the log module
        self.parent_task.events.on_response_ok(self.parent_task)
        
        self.response_data = self.response_content['data']
    
    
        if self.response_content['has_more']:
            
            self.parent_task.status.set_flag(
                flag_type='logic',
                flag_name='DO_PAGINATION',
                flag_value=True
            )
        
        return
            
    def aggregate_response_data(self):
        next_pages = self.aggregate_next_page(self.response_content['next_page'])
        self.response_data += next_pages
            
        return
    
    def save_raw_response(self):
        json_data = json.dumps(self.response_data)
        try:
            with open(self.parent_task.config.raw_dest_path, 'w') as f:
                f.write(json_data)
            
            # Triggers events in the log module
            self.parent_task.events.on_raw_save_succeeded(self.parent_task)
            
        except Exception as e:
            self.parent_task.status.caught_exception = e
            
            # Triggers events in the log module
            self.parent_task.events.on_raw_save_failed(self.parent_task)
        return
        
        
    