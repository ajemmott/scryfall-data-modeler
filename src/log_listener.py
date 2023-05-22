from loguru import logger

def handle_log_on_config_done(data_task):
    logger.info(f'\n\tPerforming query for {data_task.config.query_string}, the results will be stored in {data_task.config.processed_dest_path}')
        
    if data_task.config.raw_dest_path:
        logger.info(f"\n\tA copy of the raw query response will be stored in {data_task.config.raw_dest_path.resolve()}")   

def handle_log_on_bad_request(data_task):
    logger.error(f"\n\tRequest failed. The following details were given by the API \"{data_task.client.response_data['details']}\".")

def handle_log_on_warnings_found(data_task):
    for index, warning in data_task.client.response_warnings:
        logger.warning(f'\n\t{index + 1}: {warning}')
        
def handle_log_on_raw_save_failed(data_task):
    logger.error(f'\n\tCould not write a file to store the raw response data on given path {data_task.config.raw_dest_path}')

def handle_log_on_processed_save_failed(data_task):
    logger.error(f'\n\tCould not write a file to store the raw response data on given path {data_task.config.processed_dest_path}')

def handle_log_on_raw_save_succeeded(data_task):
    logger.success(f'\n\tFile with raw json response data successfully created on given path {data_task.config.raw_dest_path}')

def handle_log_on_processed_save_succeeded(data_task):
    logger.success(f'\n\tFile with the processed csv data successfully created on given path {data_task.config.processed_dest_path}')

    
def setup_preprocess_log_event_handlers(events):
    events.on_config_done += handle_log_on_config_done

    
def setup_postprocess_log_event_handlers(events):
    events.on_bad_request += handle_log_on_bad_request
    events.on_warnings_found += handle_log_on_warnings_found
    events.on_raw_save_failed += handle_log_on_raw_save_failed
    events.on_processed_save_succe += handle_log_on_processed_save_failed
    events.on_raw_save_succeeded += handle_log_on_raw_save_succeeded
    events.on_processed_save_succeeded += handle_log_on_processed_save_succeeded