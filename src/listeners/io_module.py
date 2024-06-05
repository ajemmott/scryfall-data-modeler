import re

def eval_user_input(response):
    
    negative_res = re.match(r'^([Nn]|No|no|0)$', response)
        
    if negative_res:
        return 'negative'
    
    affirmative_res = re.match(r'^([Yy]|Yes|yes|1)$', response)
    
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
    
def handle_io_on_invalid_destination_path(data_task):
    
    while True:
        prompt_response = input(f'The given path "{data_task.config.processed_dest_path}" cant be found. '
                                f' Would you like to create it? (y/n) ')
        res = eval_user_input(prompt_response)
        
        if res == 'uncertain':
            print('Please provide a yes/no answer.')
            continue
            
        if res == 'negative':
            # data_task.status_ok = False
            data_task.status.set_flag(
                flag_type='integrity',
                flag_name='CONFIGURATION_COMPROMISED',
                flag_value=True
            )
            break
        
        # data_task.config.do_mkdir= True
        data_task.status.set_flag(
                flag_type='logic',
                flag_name='DO_PROCESSED_MKDIR',
                flag_value=True
            )
        
        # data_task.events.on_mkdir_flag_set(data_task)
        
        break

    
def setup_io_event_handlers(events):
    events.on_warnings_found += handle_io_on_warnings_found
    events.on_invalid_destination_path += handle_io_on_invalid_destination_path
            
        
        
        
            
    