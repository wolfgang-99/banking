import imghdr
import hashlib
import time
import random
import string


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


