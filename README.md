# LMS-DB-ETL
An Extract, Transform, Load app to gather book information from public APIs for a POC LMS project

Environmental Variables:  
`GOOGLE_API_KEY` - API Key required for using the Google Books API.  
`DB_NAME`        - The name of the SQL database being used.  
`DB_USER`        - The authorized user for the database.  
`DB_PASSWORD`    - The Password to access the database.  
`LOG_FILE`       - The file location for logs to be saved to.  

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

## config/title.txt
A file with a list of book titles. Titles do not need to be in order, however each title
needs to be on its own line and any special characters should be escaped.

## How To Use
1) Create a virtual environment (optional, but best practice)
2) Use Pip to install all required packages 
```python
pip install -r requirements
```
3) Run the Orchestrator:
```python
python src/orchestrator.py
```
OR
```python
python3 src/orchestrator.py
```