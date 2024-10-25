import random
import logging
from datetime import datetime


# Configure logging
logger = logging.getLogger('acc_number')
file_handler = logging.FileHandler('log_files/acc_number.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

# bank code
bank_code = "203"


def luhn_checksum(number):
    """Calculate the Luhn checksum for the given number."""

    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))

    return checksum % 10


def generate_luhn_valid_number(number_without_checksum):
    """Generate the number with a valid Luhn checksum."""
    checksum_digit = (10 - luhn_checksum(number_without_checksum * 10)) % 10
    return number_without_checksum * 10 + checksum_digit


def generate_bank_account_number():
    """Generate a valid bank account number with Luhn checksum."""

    logger.info(' generating account number...')
    length = 12
    date = datetime.now()

    # Generate random account body (excluding bank code and checksum digit)
    account_num_body = ''.join([str(random.randint(0, 9)) for _ in range(length - len(bank_code) - 1)])

    # Combine bank code and generated account body
    account_number_without_checksum = int(bank_code + account_num_body)

    # Generate full account number with valid Luhn checksum
    full_account_number = generate_luhn_valid_number(account_number_without_checksum)
    logger.info(f'account number successfully generated on {date}')

    return str(full_account_number)


# # Example usage
# bank_code = "203"  # Example bank code
# account_number = generate_bank_account_number(bank_code)
# print("Generated Luhn-valid Bank Account Number:", account_number)
