import pandas as pd
import processor_utils as utils


def handle_pandas_on_processor_init(data_task):
    data_task.processor.df= pd.DataFrame(data_task.client.response_data)
    
    available_cols = [
        col 
        for col in utils.GAMEPLAY_FEATURES 
        if col in data_task.processor.df.columns]
    
    data_task.processor.df = (
        data_task.processor.df
        .loc[:, available_cols])
    
    data_task.processor.df.info()
    
def handle_pandas_on_dfcs_found(data_task):
    data_task.processor.df = (
        data_task.processor.df
            .apply(
               utils.set_face_order,
               axis='columns')
            .explode(['card_faces','face_type'])
            .apply(
               utils.extract_card_face_features,
               axis='columns',
               features=utils.CARD_FACE_FEATURES)
            .apply(
               utils.set_mdfc_cmc,
               axis='columns')
            .drop(columns='card_faces')
            .reset_index(drop=True))
    
    data_task.processor.df.info()
    
def handle_pandas_on_unpacking_trigger(data_task):
    data_task.processor.df = (
        data_task.processor.df
            .apply(
                utils.extract_image_uris,
                axis='columns')
            .drop(
                columns='image_uris')
            .apply(
                utils.parse_type_line,
                type_map=utils.TYPE_MAP,
                axis='columns')
            .apply(
                utils.parse_colors,
                color_map=utils.COLOR_MAP,
                axis='columns'))
    
    flag_cols = (list(utils.TYPE_MAP.values())
                 + list(utils.COLOR_MAP.values()))
    
    availabe_cols = [
        col
        for col in flag_cols
        if col in data_task.processor.df.columns]
    
    for col in availabe_cols:
        data_task.processor.df[col] = (
            ~ data_task.processor.df[col].isna())
        
    data_task.processor.df.info()
    
def handle_pandas_on_save_data_trigger(data_task):
    try:
        data_task.processor.df.to_csv(
            data_task.config.processed_dest_path,
            index=False)
        data_task.events.on_processed_save_succeeded(data_task)
    except Exception as e:
        data_task.caught_exception = e
        data_task.events.on_processed_save_failed(data_task)

def setup_pandas_event_handlers(events):
    events.on_processor_init += handle_pandas_on_processor_init
    events.on_dfcs_found += handle_pandas_on_dfcs_found
    events.on_unpacking_trigger += handle_pandas_on_unpacking_trigger
    events.on_save_data_trigger += handle_pandas_on_save_data_trigger