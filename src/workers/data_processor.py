
class DataProcessor:
    
    def __init__(self, data_task):
        self.parent_task = data_task

    def build_dataframe(self):

        
        # Triggers events in the pandas module
        self.parent_task.events.on_processor_init(self.parent_task)
        return
    
    def check_for_dfcs(self):
        
        if any(self.df.layout.isin(['transform', 'modal_dfc'])):
            
            # Triggers events in the pandas module
            self.parent_task.events.on_dfcs_found(self.parent_task)
        return
    
    def unpack_composite_features(self):
        
        # Triggers events in the pandas module
        self.parent_task.events.on_unpacking_trigger(self.parent_task)
        return
    
    def save_structured_data(self):
        
        # Triggers events in the pandas module
        self.parent_task.events.on_save_data_trigger(self.parent_task)
        
        if self.parent_task.status.logic_indicators['DO_REPORT_SAVE_FAILED']:
            
            # Triggers events in the log module
            self.parent_task.events.on_processed_save_failed(self.parent_task)
            return
        
        # Triggers events in the log module
        self.parent_task.events.on_processed_save_succeeded(self.parent_task)
        return
    
    def create_missing_folder(self):
        try:
            self.parent_task.config.processed_dest_path.mkdir(parents=True)
        
        except Exception as e:
            self.parent_task.status.caught_exception = e
        
            self.parent_task.status.set_flag(
                flag_type='logic',
                flag_name='DO_REPORT_MKDIR_FAILED',
                flag_value=True)
            
        
        