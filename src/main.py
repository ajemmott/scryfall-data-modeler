from job_config import JobConfig
from rich import inspect

def main():
    config = JobConfig().load()
    inspect(config)
    
if __name__ == '__main__':
    main()