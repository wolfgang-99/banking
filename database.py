import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo import ReturnDocument
import logging
from acc_number import generate_bank_account_number

# Configure logging
logger = logging.getLogger('database')
file_handler = logging.FileHandler('log_files/database.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

# load environmental variable
load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

# Connect to mongodb
client = MongoClient(MONGODB_URL)
db = client['banking_official']


def create_user_account(username, email, password, country):
    try:
        logger.info('creating user data for account...')
        collection = db['login_details']

        # Check if the username already exists in the database
        existing_user = collection.find_one({'username': username})
        if existing_user:
            logger.info("Username already exists. Please choose a different username.")
            return "Username already exists"

        # If the username doesn't exist, generate acc number and insert the new user
        acc_number = generate_bank_account_number()
        submission = {'username': username,
                      'email': email,
                      'password': password,
                      'country': country,
                      'acc_number': acc_number,
                      'balance': 0.00
                      }
        collection.insert_one(submission)
        logger.info(f"user account has been created and recorded")
        return True

    except Exception as e:
        logger.info("An error occurred: " + str(e))
        return "An error occurred: " + str(e)


def authenticate_user(username, password):
    try:
        logger.info('authenticating user for singing...')
        collection = db['login_details']

        # Define the criteria for the username and password
        input_username = username
        input_password = password

        # Find the user by username
        user_login_document = collection.find_one({"username": input_username})

        if user_login_document:
            stored_password = user_login_document["password"]

            if stored_password == input_password:
                logger.info('user logged in ')
                return True
            else:
                logger.info('Login Failed: Incorrect Password')
                return "Login Failed: Incorrect Password"
        else:
            logger.info('Login Failed: User not found')
            return "Login Failed: User not found"
    except Exception as e:
        logger.info("An error occurred: " + str(e))
        return "An error occurred: " + str(e)


def create_user_profile(username, first_name, last_name, sex, image_doc, address, state, zip_code, city, country,
                        balance, acc_num):
    try:
        logger.info('creating user profile...')
        login_collection = db['login_details']

        # Check if the username already exists in the database
        existing_user = login_collection.find_one({'username': username})

        if existing_user:
            # If the username exist create profile
            profile_collection = db['profile_details']
            submission = {'username': username,
                          'first_name': first_name,
                          'last_name': last_name,
                          'sex': sex,
                          'image': image_doc,
                          'address': address,
                          'state': state,
                          'zip_code': zip_code,
                          'city': city,
                          'country': country,
                          'balance': balance,
                          'acc_number': acc_num
                          }

            profile_collection.insert_one(submission)
            logger.info(f"user {username} profile has been created")
            return True

    except Exception as e:
        logger.info("An error occurred: " + str(e))
        return "An error occurred: " + str(e)


def get_profile_data(username):
    try:
        logger.info('getting user profile data...')
        profile_collection = db['profile_details']

        # Check if the username already exists in the database
        existing_user = profile_collection.find_one({'username': username})

        if existing_user:
            profile_doc = {
                'first_name': existing_user.get('first_name'),
                'last_name': existing_user.get('last_name'),
                'sex': existing_user.get('sex'),
                'address': existing_user.get('address'),
                'state': existing_user.get('state'),
                'zip_code': existing_user.get('zip_code'),
                'city': existing_user.get('city'),
                'country': existing_user.get('country'),

            }

            logger.info(f"profile data retrieved")
            return profile_doc
        else:
            logger.info(f'user {username} dose not have profile data')
            return f'user {username} dose not have profile data'

    except Exception as e:
        logger.info("An error occurred: " + str(e))
        return "An error occurred: " + str(e)


def create_kyc_data(username, first_name, last_name, sex, image_doc, address, zip_code, city, state, country):
    try:
        logger.info('creating user kyc data...')
        login_collection = db['login_details']

        # Check if the username already exists in the database
        existing_user = login_collection.find_one({'username': username})

        if existing_user:
            # If the username exist create profile
            kyc_collection = db['kyc_details']
            submission = {'username': username,
                          'first_name': first_name,
                          'last_name': last_name,
                          'sex': sex,
                          'image_ID': image_doc,
                          'address': address,
                          'state': state,
                          'zip_code': zip_code,
                          'city': city,
                          'country': country,
                          }

            kyc_collection.insert_one(submission)
            logger.info(f"kyc data save")
            return True

    except Exception as e:
        logger.info("An error occurred: " + str(e))
        return "An error occurred: " + str(e)


def get_kyc_data(username):
    try:
        logger.info('getting user kyc data...')
        kyc_collection = db['kyc_details']

        # Check if the username already exists in the database
        existing_user = kyc_collection.find_one({'username': username})

        if existing_user:
            kyc_doc = {
                'first_name': existing_user.get('first_name'),
                'last_name': existing_user.get('last_name'),
                'sex': existing_user.get('sex'),
                'address': existing_user.get('address'),
                'state': existing_user.get('state'),
                'zip_code': existing_user.get('zip_code'),
                'city': existing_user.get('city'),
                'country': existing_user.get('country'),

            }

            logger.info(f"kyc data retrieved")
            return kyc_doc
        else:
            logger.info(f'user {username} dose not have kyc data')
            return f'user {username} dose not have kyc data'

    except Exception as e:
        logger.info("An error occurred: " + str(e))
        return "An error occurred: " + str(e)


def save_account_uuid(username, account_uuid):
    try:
        logger.info('creating user data for account...')
        collection = db['account_uuid']

        # Check if the username already exists in the database
        existing_user = collection.find_one({'username': username})
        if existing_user:
            logger.info("Username already exists. Please choose a different username.")
            return "Username already exists"

        # If the username doesn't exist, generate acc number and insert the new user
        acc_number = generate_bank_account_number()
        submission = {'username': username,
                      'account_uuid': account_uuid,
                      }
        collection.insert_one(submission)
        logger.info(f"user currencycloud account has been created")
        return True

    except Exception as e:
        logger.info("An error occurred: " + str(e))
        return "An error occurred: " + str(e)
