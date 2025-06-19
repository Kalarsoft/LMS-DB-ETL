import os
import sys
import extract
import transform
import load
import logging
from datetime import date, datetime

logger = logging.getLogger('orchestrator.py')
logging.basicConfig(filename=os.getenv('LOG_FILE'), level=os.getenv('LOGGING_LEVEL'))

today = date.today()

if __name__ == '__main__':
    try:
        logger.info(f'{datetime.now()}:Starting extract.py')
        extract.start()
    except Exception as err:
        logger.error(f'{datetime.now()}:An error occurred with extraction: {err}')
        sys.exit(1)
    logger.info(f'{datetime.now()}:Extraction completed.')

    try:
        logger.info(f'{datetime.now()}:Starting transform.py')
        transform.start()
    except Exception as err:
        logger.error(f'{datetime.now()}:An error occurred with transformation: {err}')
        sys.exit(1)
    logger.info(f'{datetime.now()}:Transformation completed.')
        
    try:
        logger.info(f'{datetime.now()}:Starting load.py')
        load.start()
    except Exception as err:
        logger.error(f'{datetime.now()}:An error occurred with loading: {err}')
        sys.exit(1)
    logger.info(f'{datetime.now()}:Loading completed.')
    
    os.remove(f'output/raw_google_books_{today}.json')
    os.remove(f'output/raw_open_lib_books_{today}.json')
    os.remove(f'output/transformed_{today}.json')
    logger.info(f'{datetime.now()}:Orchestration complete. ETL Pipeline executed without errors.')
