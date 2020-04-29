import logging
import requests
import json
import os


import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:

    # Configure logging format
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    try: 
        response = requests.get(
            url="http://worldclockapi.com/api/json/utc/now"
        )

        if response.status_code == 200:
            time = (json.loads(response.text))['currentDateTime']
            return func.HttpResponse(time)
        else:
            logging.error(f"Error querying API.  Status code: {response.status_code}")

    except Exception:
        return func.HttpResponse(
            "Failed to run function",
            status_code=400
        )
