import requests
import logging
import os
from dotenv import load_dotenv
from server import generate_reference_number

# Configure logging
logger = logging.getLogger('api')
file_handler = logging.FileHandler('log_files/api.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

# load environmental variable
load_dotenv()
api_key = os.getenv("api_key").strip()
login_id = os.getenv("login_id").strip()

# Log the length of the api_key for debugging
logger.info(f"API key length: {len(api_key) if api_key else 'None'}")
logger.info(f"Login ID: {login_id}")


def api_login():
    # Check if api_key and login_id are valid
    if not api_key or len(api_key) != 64:
        logger.error("Invalid or missing API key")
    if not login_id:
        logger.error("Missing login ID")

    # Define the base URL and endpoint
    url = "https://devapi.currencycloud.com/v2/authenticate/api"

    payload = {
        'api_key': api_key,
        'login_id': login_id
    }

    # Make the POST request
    response = requests.post(url, data=payload)

    # Check the response
    if response.status_code == 200:
        logger.info("Authentication successful!")
        res = response.json()
        auth_token = res['auth_token']
        return auth_token
    else:
        logger.error(f"Failed to authenticate api login details. Status code: {response.status_code}")
        logger.error("Response: " + response.text)
        return False


def api_logout(auth_token):

    # Define the base URL and endpoint
    url = "https://devapi.currencycloud.com/v2/authenticate/close_session"

    headers = {
        'X-Auth-Token': auth_token
    }

    # Make the POST request
    response = requests.post(url, headers=headers)
    # Check the response
    if response.status_code == 200:
        logger.info("Session closed successfully!")
        return True
    else:
        logger.error(f"Failed to close session. Status code: {response.status_code}")
        logger.error("Response: " + response.text)
        return f"error {response.text} with satus code {response.status_code}"


def check_personal_balance(auth_token, currency):
    # Define the base URL and endpoint
    url = f"https://devapi.currencycloud.com/v2/balances/{currency}"

    headers = {
        'X-Auth-Token': auth_token
    }

    # Make the POST request
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        logger.info("Gotten balance successfully!")
        res = response.json()
        return res
    else:
        logger.error(f"Failed to retrieve account balance. Status code: {response.status_code}")
        logger.error("Response: " + response.text)
        return f"error {response.text} with satus code {response.status_code}"


def check_all_personal_balance(auth_token):
    # Define the base URL and endpoint
    url = f"https://devapi.currencycloud.com/v2/balances/find"

    headers = {
        'X-Auth-Token': auth_token
    }

    # Make the POST request
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        logger.info("Gotten list of balance successfully!")
        res = response.json()
        return res
    else:
        logger.error(f"Failed to retrieve list of account balance. Status code: {response.status_code}")
        logger.error("Response: " + response.text)
        return f"error {response.text} with satus code {response.status_code}"


def check_costumer_balance(auth_token, currency, costumer_uuid):
    # Define the base URL and endpoint
    url = f"https://devapi.currencycloud.com/v2/balances/{currency}?on_behalf_of={costumer_uuid}"

    headers = {
        'X-Auth-Token': auth_token
    }

    # Make the POST request
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        logger.info(f"Gotten costumer({costumer_uuid}) list of balance successfully!")
        res = response.json()
        return res
    else:
        logger.error(f"Failed to retrieve list of account({costumer_uuid}) "
                     f"balance. Status code: {response.status_code}")
        logger.error("Response: " + response.text)
        return f"error {response.text} with satus code {response.status_code}"


def check_all_costumer_balance(auth_token, costumer_uuid):
    # Define the base URL and endpoint
    url = f"https://devapi.currencycloud.com/v2/balances/find?on_behalf_of={costumer_uuid}"

    headers = {
        'X-Auth-Token': auth_token
    }

    # Make the POST request
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        logger.info(f"Gotten costumer({costumer_uuid}) list of balance successfully!")
        res = response.json()
        return res
    else:
        logger.error(f"Failed to retrieve list of account({costumer_uuid}) "
                     f"balance. Status code: {response.status_code}")
        logger.error("Response: " + response.text)
        return f"error {response.text} with satus code {response.status_code}"


def create_sub_account(auth_token, data):
    # Define the base URL and endpoint
    url = "https://devapi.currencycloud.com/v2/accounts/create"

    ref, raw = generate_reference_number()
    data.update({'status': 'enabled',
                 'your_reference': ref
                 })
    payload = data

    headers = {
        'X-Auth-Token': auth_token
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=payload)

    # Check the response
    if response.status_code == 200:
        logger.info("sub_account creation successful!")
        res = response.json()
        return res
    else:
        logger.error(f"Failed to create sub_account . Status code: {response.status_code}")
        logger.error("Response: " + response.text)


##############
account_name = 'Jimmy Burritos'
legal_entity_type = 'company'
street = '123 Main Street'
city = 'Denver'
country = 'us'
postal_code = '80209'
state_or_province = 'CO'
identification_type = 'incorporation_number'
identification_value = '123456789'

auth = api_login()
payload = {
        'account_name': account_name,
        'legal_entity_type': legal_entity_type,
        'street': street,
        'city': city,
        'country': country,
        'postal_code': postal_code,
        'state_or_province': state_or_province,
        'identification_type': identification_type,
        'identification_value': identification_value


    }


