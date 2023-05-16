from loguru import logger
from events import Events

def handle_job_configured(job_config):
        logger.info(f'\n\tPerforming query for {job_config.query_string}, the results will be stored in {job_config.processed_dest_path}')
        
        if job_config.raw_dest_path:
            logger.info("\n\tA copy of the raw query response will be stored in {job_config.raw_dest_path}")   
            
def setup_log_event_handlers(events):
    events.on_job_configured += handle_job_configured