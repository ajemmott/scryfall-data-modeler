import re

def eval_user_input(response):
    
        affirmative_res = re.match(r'^(.[Yy]|Yes|yes|1)$', response)
        negative_res = re.match(r'^(.[Nn]|No|no|0)$', response)
        
        if negative_res:
            return 'negative'
        
        if not affirmative_res:
            return 'uncertain'
        
        return 'affirmative'
        

def handle_io_on_warnings_found(data_task):
    
    while True:
        prompt_response = input("Do want to continue working with this data? (y/n)")
        res = eval_user_input(prompt_response)
        
        if res == 'uncertain':
            print('Please provide a yes/no answer.')
            continue
            
        if res == 'negative':
            data_task.status_ok = False
            break
        
        break
        
    
def setup_io_event_handlers(events):
    events.on_warnings_found += handle_io_on_warnings_found
            
        
        
        
            
    