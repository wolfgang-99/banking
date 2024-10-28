import imghdr
import hashlib
import time
import random
import string
from werkzeug.utils import secure_filename
import os
from database import upload_img_to_mongodb


# Create a directory to store uploaded images
UPLOAD_FOLDER = 'doc_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def is_image_file(file_path):
    # Check if the file is an image using imghdr
    valid_image_extensions = {'jpeg', 'png', 'jpg'}
    file_type = imghdr.what(file_path)
    return file_type in valid_image_extensions


def generate_reference_number():
    # Get current timestamp in milliseconds
    timestamp = str(int(time.time() * 1000))

    # Generate a random string of 8 alphanumeric characters
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # Concatenate timestamp and random part
    raw_ref = timestamp + random_part

    # Generate a secure hash (SHA-256) for the reference number
    hash_object = hashlib.sha256(raw_ref.encode())
    reference_number = hash_object.hexdigest().upper()[:16]  # Truncate to 16 chars

    return reference_number, raw_ref


def validate_image(uploaded_image, username):
    try:
        image_format = uploaded_image.content_type
        print(image_format)

        # Check if the file is an allowed image format (e.g., JPEG, PNG)
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
        if '.' in uploaded_image.filename and \
                uploaded_image.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            print(f'this the file name {uploaded_image.filename} ')

            # Generate a secure filename for the uploaded file
            filename = secure_filename(uploaded_image.filename)
            print(f'this the secure filename {filename}')

            # Save the image with a unique name in the uploads folder
            full_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_image.save(full_path)
            print(f'this is the the full path with securefilename {full_path}')

            # call the upload image function
            save_to_db = upload_img_to_mongodb(image_file_path=full_path, image_format=image_format, username=username)
            if save_to_db:
                return True
        else:
            return "invalid file format"

    except Exception as e:
        return "An error occurred: " + str(e)
