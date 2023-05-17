import json
from requests import get

class ApiClient:
    def __init__(self, data_task):
        self.parent_task = data_task
        self.query_string = self.parent_task.config.query_string
        self.raw_dest_path = self.parent_task.config.raw_dest_path
    
    def request_cards(self):
        API_ENDPOINT = 'https://api.scryfall.com/cards/search?q='
        request = API_ENDPOINT + self.query_string
        self.response = get(request)
        self.response_data = self.response.json()
        
        
        if not self.response.ok:
            self.parent_task.status_ok = False
            self.parent_task.events.on_bad_request(self)
            return
        
        if 'warnings' in self.response_data.keys():
            self.response_warnings =  enumerate(self.response_data['warnings'])
            self.parent_task.events.on_warnings_found(self)
            
        return
    
    def save_raw_response(self):
        json_data = json.dumps(self.response_data)
        try:
            with open(self.raw_dest_path, 'w') as f:
                f.write(json_data)
                
        except Exception:
            self.parent_task.events.on_raw_save_failed(self)
        return
        
        
            
