import pandas as pd
import card_logic


def handle_pandas_on_processor_init(data_task):
    data_task.processor.df= pd.DataFrame(data_task.client.response_data)
    
    available_cols = [
        col 
        for col in card_logic.GAMEPLAY_FEATURES 
        if col in data_task.processor.df.columns]
    
    data_task.processor.df = (
        data_task.processor.df
        .loc[:, available_cols])
    
    data_task.processor.df.info()
    
def handle_pandas_on_dfcs_found(data_task):
    data_task.processor.df = (
        data_task.processor.df
            .apply(
               card_logic.set_face_order,
               axis='columns')
            .explode(['card_faces','is_castable_face','is_front_face'])
            .apply(
               card_logic.extract_card_face_features,
               axis='columns',
               features=card_logic.CARD_FACE_FEATURES)
            .apply(
               card_logic.set_mdfc_cmc,
               axis='columns')
            .drop(columns='card_faces')
            .reset_index(drop=True))
    
    data_task.processor.df.info()
    
def handle_pandas_on_unpacking_trigger(data_task):
    data_task.processor.df = (
        data_task.processor.df
            .apply(
                card_logic.extract_image_uris,
                axis='columns')
            .drop(
                columns='image_uris')
            .apply(
                card_logic.parse_type_line,
                type_map=card_logic.TYPE_MAP,
                axis='columns'))
    
    data_task.processor.df.loc[:,'colors'] = data_task.processor.df['colors'].fillna(0)

    data_task.processor.df = (
        data_task.processor.df
            .apply(
                card_logic.parse_colors,
                color_map=card_logic.COLOR_MAP,
                axis='columns'))
    
    data_task.processor.df.info()
    
def handle_pandas_on_save_data_trigger(data_task):
    try:
        data_task.processor.df.to_csv(
            data_task.config.processed_dest_path,
            index=False)
        # data_task.events.on_processed_save_succeeded(data_task)
        
    except Exception as e:
        data_task.status.caught_exception = e
        
        data_task.status.set_flag(
                flag_type='logic',
                flag_name='DO_REPORT_SAVE_FAILED',
                flag_value=True
            )
        

def setup_pandas_event_handlers(events):
    events.on_processor_init += handle_pandas_on_processor_init
    events.on_dfcs_found += handle_pandas_on_dfcs_found
    events.on_unpacking_trigger += handle_pandas_on_unpacking_trigger
    events.on_save_data_trigger += handle_pandas_on_save_data_trigger