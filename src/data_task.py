from events import Events
from log_listener import setup_log_event_handlers
from task_listener import setup_task_event_handlers

class DataTask:
    
    def __init__(self):
        self.events = Events()
        self.status_ok = True
        setup_log_event_handlers(self.events)
        setup_task_event_handlers(self.events)
        
    def start(self):
        self.event_stack = {
            'CONFIG': self.events.on_init_done,
            'REQUEST': self.events.on_config_done,
        #     'STRUCTURE': self.events.on_request_data_obtained,
        }
        
        for event, function in self.event_stack.items():
            
            if not self.status_ok:
                break
            
            function(self)
            
    
    