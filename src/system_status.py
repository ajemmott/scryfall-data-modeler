
class SystemStatus:
    
    def __init__(self):
        self.integrity_indicators = {
            'CONFIGURATION_COMPROMISED': False,
            'EXTRACTION_COMPROMISED': False,
            'TRANSFORMATION_COMPROMISED': False,
            'LOAD_COMPROMISED': False,
        }
        
        self.logic_indicators = {
            'DO_PROCESSED_MKDIR': False,
            'DO_PAGINATION': False,
            'DO_REPORT_SAVE_FAILED': False,
        }
        
    def test_integrity_compromised(self):
        return any(
            [flag_value 
             for flag_name, flag_value 
             in self.integrity_indicators.items()])
        
    def set_flag(self, flag_type, flag_name, flag_value):
        if flag_type == 'integrity':
            self.integrity_indicators[flag_name] = flag_value
        
        if flag_type == 'logic':
            self.logic_indicators[flag_name] = flag_value
            
    