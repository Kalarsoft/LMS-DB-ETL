# LMS-DB-ETL
An Extract, Transform, Load app to gather book information from public API for a POC LMS project

Environmental Variables:
`GOOGLE_API_KEY` - API Key required for using the Google Books API.
`DB_NAME`        - The name of the SQL database being used
`DB_USER`        - The authorized user for the database
`DB_PASSWORD`    - The Password to access the database
`LOG_FILE`       - The file location for logs to be saved to
`LOGGING_LEVEL`  - The logging level desired for operation. `logging.INFO` is standard,  
                   but `logging.DEBUG` can be used for more insight and `logging.ERROR` if only issues are needed.

## extract.py
The extract.py file contains functions to pull data related to books from different APIs.

## transform.py
Takes the raw JSON stored by extract.py and transforms the entries into a single entry whose keys  
match the column names of the database schema.

## load.py
Takes the JSON file created by transform.py and loads the data into a PostgreSQL database for  
retreival later.

## orchestrator.py
Handles the orchestration of each program being ran one after the other. Ensures each  
executes with no fatal errors before moving on to the next. Also cleans up files created  
by the programs before ending.