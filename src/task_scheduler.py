from events import Events
from system_status import SystemStatus

from listeners.worker_module import setup_worker_event_handlers
from listeners.log_module import setup_preprocess_log_event_handlers, setup_postprocess_log_event_handlers
from listeners.io_module import setup_io_event_handlers
from listeners.pandas_module import setup_pandas_event_handlers


from workers.task_configurator import TaskConfigurator
from workers.api_client import ApiClient
from workers.data_processor import DataProcessor

class TaskScheduler:
    
    def __init__(self):
        self.status = SystemStatus()
        
        self.events = Events()
        self.set_event_handlers()
        self.phase_stack = {
            # All trigger events in the worker module
            'CONFIG': self.events.on_init_done,
            'EXTRACT': self.events.on_config_done,
            'TRANSFORM': self.events.on_extract_done,
            'LOAD': self.events.on_transform_done
        }

    def set_event_handlers(self):
        setup_worker_event_handlers(self.events)
        setup_preprocess_log_event_handlers(self.events)
        setup_io_event_handlers(self.events)
        setup_pandas_event_handlers(self.events)
        setup_postprocess_log_event_handlers(self.events)  
    
    def trigger_phase(self, event_caller):
        event_caller(self)
        
    def run_event_loop(self):
        for event_name, event_caller in self.phase_stack.items():
            
            if self.status.test_integrity_compromised():
                break
            
            self.current_phase = event_name
            
            #Triggers events in log module
            self.events.on_phase_change(self)
            
            self.trigger_phase(event_caller)
    
   