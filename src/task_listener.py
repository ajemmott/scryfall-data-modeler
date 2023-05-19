from task_config import TaskConfig
from api_client import ApiClient
from data_processor import DataProcessor

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
        
def handle_tasks_on_request_done(data_task):
    processor = DataProcessor(data_task)
    setattr(data_task, 'processor', processor)
    
    processor.build_dataframe()
    processor.check_for_dfcs()
    processor.unpack_composite_features()
    
    
def setup_task_event_handlers(events):
    events.on_init_done += handle_tasks_on_init_done
    events.on_config_done += handle_tasks_on_config_done
    events.on_request_done += handle_tasks_on_request_done