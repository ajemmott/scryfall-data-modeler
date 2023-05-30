from loguru import logger
from io import StringIO

def handle_log_on_request_setup(data_task):
    output = StringIO()
    output.write(f'Performing query for \"{data_task.config.query_string}\".')
    
    if data_task.config.raw_dest_path:
        output.write(' A raw copy of the response data will be stored.')
        
    logger.info(output.getvalue())


def handle_log_on_bad_request(data_task):
    logger.error(f'Request failed. The following details were given by the '
                 f'API: \n\n\t\"{data_task.client.response_details}\".')

def handle_log_on_warnings_found(data_task):
    output = StringIO()
    output.write('Query successful. The following warnings were noted on the '
                 'query response:')
    
    for index, warning in data_task.client.response_warnings:
        output.write(f'\n\t{index + 1}: {warning}')
    
    logger.warning(output.getvalue())
    
def handle_log_on_response_ok(data_task):
    logger.success('Query successful. No warnings were given on the query'
                   'response.')
        
def handle_log_on_raw_save_failed(data_task):
    logger.error(f'Could not write a file to store the raw response data '
                 f'on given path {data_task.config.raw_dest_path}. '
                 f'{data_task.caught_exception}.')

def handle_log_on_processed_save_failed(data_task):
    logger.error(f'Could not write a file to store the raw response data '
                 f'on given path {data_task.config.processed_dest_path}. '
                 f'{data_task.caught_exception}.')

def handle_log_on_raw_save_succeeded(data_task):
    logger.success(f'File with raw json response data successfully created '
                   f'on given path {data_task.config.raw_dest_path}')

def handle_log_on_processed_save_succeeded(data_task):
    logger.success(f'File with the processed csv data successfully created '
                   f'on given path {data_task.config.processed_dest_path}')

def setup_preprocess_log_event_handlers(events):
    events.on_request_setup += handle_log_on_request_setup
    events.on_bad_request += handle_log_on_bad_request
    events.on_warnings_found += handle_log_on_warnings_found

    
def setup_postprocess_log_event_handlers(events):
    events.on_response_ok += handle_log_on_response_ok
    events.on_raw_save_failed += handle_log_on_raw_save_failed
    events.on_processed_save_succeded += handle_log_on_processed_save_failed
    events.on_raw_save_succeeded += handle_log_on_raw_save_succeeded
    events.on_processed_save_succeeded += handle_log_on_processed_save_succeeded