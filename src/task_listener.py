from task_config import TaskConfig
from api_client import ApiClient

def handle_tasks_on_init_done(data_task):
    config = TaskConfig()
    setattr(data_task, 'config', config)
    
    config.load_config()
    
    

def handle_tasks_on_config_done(data_task):
    client = ApiClient(data_task)
    setattr(data_task, 'client', client)
    
    client.request_cards()
    
    if data_task.config.raw_dest_path:
        client.save_raw_response()
        
    
        
# def handle_request_data_obtained(events, status_ok, config, client):
    
    
def setup_task_event_handlers(events):
    events.on_init_done += handle_tasks_on_init_done
    events.on_config_done += handle_tasks_on_config_done