from flask import Flask, request, jsonify, session
from datetime import timedelta
from database import *
from acc_number import generate_bank_account_number
from api import *
from database import *
import logging
from flask_cors import CORS
from server import is_image_file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("main.log"), logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.permanent_session_lifetime = timedelta(hours=3)
app.secret_key = os.getenv("secret_key")


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the banking API "}), 200


@app.route('/sign_up', methods=['POST'])
def create_user():
    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        country = request.form['country']

        logger.info('getting user sign_up data ....')
        if not username or not email or not password or not country:
            return jsonify({"error": "Missing required fields"}), 400

        create_acc = create_user_account(username=username, email=email, password=password, country=country)
        if create_acc:
            logger.info(f"user account ({username}) has been created ")
            return jsonify(f"user account ({username}) has been created and recorded"), 200

        else:
            logger.info(f"error: {create_acc}")
            return jsonify(create_acc), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/sign_in", methods=['POST'])
def login_in():
    try:
        username = request.form['username']
        password = request.form['password']

        logger.info('getting user sign_in data ....')
        if not username or not password:
            return jsonify({"error": "Missing required fields"}), 400

        login_in = authenticate_user(username=username, password=password)

        if login_in:
            logger.info(f"user account ({username}) logged in successful")
            return jsonify(f"user account ({username})  logged in successful"), 200
        else:
            logger.info(f"error: {login_in}")
            return jsonify(login_in), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route("/create profile", methods=['POST'])
def create_user_profile():
    if 'image' not in request.files:
        return jsonify({'error': 'Non file part to image'}), 400

    # Extracting the fields from the form data
    username = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    sex = request.form['sex']
    image = request.files['image']
    address = request.form['address']
    state = request.form['state']
    zip_code = request.form['zip_code']
    city = request.form['city']
    country = request.form['country']

    logger.info('getting user profile data ....')
    if not all([username, first_name, last_name, sex, address, state, zip_code, city]):
        return jsonify({"error": "Missing required fields"}), 400

    if image.filename == '':
        return jsonify({'error': 'Non selected image file'}), 400

    # Save image temporarily to check its type
    file_path = f"temp/{image.filename}"
    try:
        # Save the image to disk
        with open(file_path, 'wb') as f:
            f.write(image.read())

        # Validate if the uploaded image is an image
        if not is_image_file(file_path):
            os.remove(file_path)
            return jsonify({'error': 'The uploaded file is not a valid image'}), 400

        # image has been validated; now upload using its path
        try:

            balance = 0.0  # initialize acc balance
            acc_num = generate_bank_account_number()  # create acc number

            create_profile = create_user_profile(username=username, first_name=first_name, last_name=last_name, sex=sex,
                                                 image_doc=file_path, address=address, state=state, zip_code=zip_code,
                                                 city=city, country=country, balance=balance, acc_num=acc_num)

            if create_profile:
                logger.info(f'user {username} profile created')
                return jsonify(f'user {username} profile created'), 200
            else:
                logger.info(create_profile)
                return jsonify(create_profile), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            # Ensure the file is removed even if an error occurs
            if os.path.exists(file_path):
                os.remove(file_path)

    except Exception as e:
        # Handle any errors, ensuring file cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': str(e)}), 500


@app.route('/get_profile_data/<username>', methods=['GET'])
def get_profile(username):
    try:
        profile_data = get_profile_data(username=username)

        if profile_data:
            logger.info(f'user {username} profile data retrieved')
            return jsonify(profile_data), 200
        else:
            logger.info(profile_data)
            return jsonify(profile_data), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/submit_kyc', methods=['POST'])
def create_kyc():
    if 'image' not in request.files:
        return jsonify({'error': 'Non file part to image'}), 400

    username = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    sex = request.form['sex']
    image = request.files['image']
    address = request.form['address']
    state = request.form['state']
    zip_code = request.form['zip_code']
    city = request.form['city']
    country = request.form['country']

    logger.info('getting user kyc data ....')
    if not all([username, first_name, last_name, sex, address, state, zip_code, city]):
        return jsonify({"error": "Missing required fields"}), 400

    if image.filename == '':
        return jsonify({'error': 'Non selected image file'}), 400

    # Save image temporarily to check its type
    file_path = f"temp/{image.filename}"
    try:

        # Save the image to disk
        with open(file_path, 'wb') as f:
            f.write(image.read())

        # Validate if the uploaded image is an image
        if not is_image_file(file_path):
            os.remove(file_path)
            return jsonify({'error': 'The uploaded file is not a valid image'}), 400

        # image has been validated; now upload using its path
        try:
            kyc = create_kyc_data(username=username, first_name=first_name, last_name=last_name, sex=sex,
                                  image_doc=image, address=address, state=state, zip_code=zip_code, city=city,
                                  country=country)

            if kyc:
                logger.info(f'user {username} kyc saved')
                return jsonify(f'user {username} kyc saved'), 200
            else:
                logger.info(kyc)
                return jsonify(kyc), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            # Ensure the file is removed even if an error occurs
            if os.path.exists(file_path):
                os.remove(file_path)

    except Exception as e:
        # Handle any errors, ensuring file cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': str(e)}), 500


@app.route('/get_kyc_data/<username>', methods=['GET'])
def get_kyc(username):
    try:
        kyc_data = get_kyc_data(username=username)

        if kyc_data:
            logger.info(f'user {username} kyc data retrieved')
            return jsonify(kyc_data), 200
        else:
            logger.info(kyc_data)
            return jsonify(kyc_data), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/create_sub_account/<username>', methods=['POST'])
def create_sub_acc(username):
    try:
        auth = api_login()
        if auth:

            account_name = request.form['account_name']
            legal_entity_type = request.form['legal_entity_type']
            street = request.form['street']
            city = request.form['city']
            country =request.form['country']
            postal_code =request.form['postal_code']
            state_or_province =request.form['state_or_province']
            identification_type =request.form['identification_type']
            identification_value = request.form['identification_value']

            if not all([account_name, legal_entity_type, street, city, country, postal_code,state_or_province,
                        identification_value, identification_type]):
                return jsonify({"error": "Missing required fields"}), 400

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
            create = create_sub_account(auth_token=auth, data=payload)
            if create:
                acc_uuid = create['id']
                save_acc_uuid = save_account_uuid(username, account_uuid=acc_uuid)
                if save_acc_uuid:
                    api_logout(auth_token=auth)
                    return jsonify('sub account created with account_uuid save'), 200
                else:
                    api_logout(auth_token=auth)
                    return jsonify(f"error in saving acc_uuid {save_acc_uuid}")
            else:
                return jsonify(create)

        else:
            return f"Failed to authenticate currencycloud api login details."

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
if __name__ == '__main__':
    app.run(debug=True)