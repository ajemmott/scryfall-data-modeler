from task_scheduler import TaskScheduler

def main():
    scheduler = TaskScheduler()
    scheduler.run_event_loop()
    
if __name__ == '__main__':
    main()
