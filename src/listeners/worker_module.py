from workers.task_configurator import TaskConfigurator
from workers.api_client import ApiClient
from workers.data_processor import DataProcessor

def handle_tasks_on_init_done(data_task):
    config = TaskConfigurator(data_task)
    setattr(data_task, 'config', config)
    
    config.load_config()
    
def handle_tasks_on_config_done(data_task):
    client = ApiClient(data_task)
    setattr(data_task, 'client', client)
    
    client.request_cards()
    client.evaluate_request_response()
    
    if data_task.status.logic_indicators['DO_PAGINATION']:
        client.aggregate_response_data()
        
    
        
def handle_tasks_on_extract_done(data_task):
    processor = DataProcessor(data_task)
    setattr(data_task, 'processor', processor)
    
    processor.build_dataframe()
    processor.check_for_dfcs()
    processor.unpack_composite_features()

def handle_tasks_on_transform_done(data_task):
    
    if data_task.status.logic_indicators['DO_PROCESSED_MKDIR']:
        data_task.processor.create_missing_folder()
    
    if data_task.config.raw_dest_path and data_task.status.test_integrity_compromised():
        data_task.client.save_raw_response()
        
    data_task.processor.save_structured_data()
    
def setup_worker_event_handlers(events):
    events.on_init_done += handle_tasks_on_init_done
    events.on_config_done += handle_tasks_on_config_done
    events.on_extract_done += handle_tasks_on_extract_done
    events.on_transform_done += handle_tasks_on_transform_done