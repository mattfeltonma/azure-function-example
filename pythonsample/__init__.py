import logging
import requests
import json
import os
import socket
import azure.functions as func
from opencensus.ext.azure.log_exporter import AzureLogHandler
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

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
        logging.info('Successfully queried public API')
        return time
    else:
        raise Exception(f"Failed to query time API. Status code was: {response.status_code}")
        logger.error(f"Error querying API.  Status code: {response.status_code}")

# Get Key Vault secret
def get_secret():

    VAULT_NAME = os.getenv('KEY_VAULT_NAME')
    KEY_VAULT_SECRET_NAME = os.getenv('KEY_VAULT_SECRET_NAME')
    credential = DefaultAzureCredential(
        managed_identity_client_id = os.getenv('MSI_CLIENT_ID')
    )
    secret_client = SecretClient(vault_url=f"https://{VAULT_NAME}.vault.azure.net/", credential=credential)
    secret = secret_client.get_secret(f"{KEY_VAULT_SECRET_NAME}")
    return secret.value
    
def main(req: func.HttpRequest) -> func.HttpResponse:

    try: 
        wordoftheday = get_secret()
        time = query_time()
        return func.HttpResponse(f"The current time is {time} and the word of the day is {wordoftheday}")

    except Exception:
        return func.HttpResponse(
            "Failed to run function",
            status_code=400
        )
