import logging
import requests
import json
import os
import socket
import azure.functions as func
from opencensus.ext.azure.log_exporter import AzureLogHandler

# Setup logging mechanism
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string=os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING'))
)

# Get time from public API
def query_time():
    response = requests.get(
        url="http://worldclockapi.com/api/json/utc/now"
    )

    if response.status_code == 200:
        time = (json.loads(response.text))['currentDateTime']
        return time
    else:
        raise Exception(f"Failed to query time API. Status code was: {response.status_code}")
        logger.error(f"Error querying API.  Status code: {response.status_code}")

def main(req: func.HttpRequest) -> func.HttpResponse:

    try: 
        wordoftheday = os.getenv('WORD_OF_THE_DAY')
        time = query_time()
        return func.HttpResponse(f"The current time is {time}. And the word of the day is {wordoftheday}")

    except Exception:
        return func.HttpResponse(
            "Failed to run function",
            status_code=400
        )
