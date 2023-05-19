
class DataProcessor:
    
    def __init__(self, data_task):
        self.parent_task = data_task

    def build_dataframe(self):
        self.parent_task.events.on_processor_init(self.parent_task)
    
    def check_for_dfcs(self):
        if any(self.df.layout.isin(['transform', 'modal_dfc'])):
            self.parent_task.events.on_dfcs_found(self.parent_task)
    
    def unpack_composite_features(self):
        self.parent_task.events.on_unpacking_trigger(self.parent_task)