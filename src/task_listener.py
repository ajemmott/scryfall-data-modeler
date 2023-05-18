from task_config import TaskConfig
from api_client import ApiClient

def handle_tasks_on_init_done(data_task):
    config = TaskConfig()        
    config.load_config()
    
    setattr(data_task, 'config', config)

def handle_tasks_on_config_done(data_task):
    client = ApiClient(data_task)
    client.request_cards()
    
    if client.parent_task.config.raw_dest_path:
        client.save_raw_response()
        
    setattr(data_task, 'client', client)
        
# def handle_request_data_obtained(events, status_ok, config, client):
    
    
def setup_task_event_handlers(events):
    events.on_init_done += handle_tasks_on_init_done
    events.on_config_done += handle_tasks_on_config_done