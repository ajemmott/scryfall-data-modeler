from job_config import JobConfig
from rich import inspect

def main():
    config = JobConfig().load()
    
if __name__ == '__main__':
    main()