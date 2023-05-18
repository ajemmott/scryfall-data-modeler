# sf-command-line-query

## Curently under construction
A tool to perform card data queries to the scryfall API from the command line, structuring and cleaning the response to store it locally as a resource for data analysis.

## Changelog
---
**ajemmott - 2023/05/11**
- Began project
---
**ajemmott - 2023/05/17**
- Enabled functionality to store the raw API response as json.  
    ```
    $<path to script> QUERY_STRING PROCESSED_DATA_DESTINATION_FILE [-r RAW_DATA_DESTINATION_FILE]
    ```
- `PROCESSED_DATA_DESTINATION_FILE` is currently unused.

