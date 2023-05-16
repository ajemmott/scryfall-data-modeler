from events import Events
from log_listener import setup_log_event_handlers


class EventSystem:
    
    def __init__(self):
        self.events = Events()
        self.status_ok == True
        
        setup_log_event_handlers(self.events)
        
    
    