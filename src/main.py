from event_system import EventSystem
from job_config import JobConfig
from api_client import ApiClient
from rich import inspect



def main():
    event_system = EventSystem()
    config = JobConfig(event_system.events)

    
if __name__ == '__main__':
    main()