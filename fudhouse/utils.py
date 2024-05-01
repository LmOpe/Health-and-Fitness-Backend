import hashlib
import base64

from datetime import datetime

def hash_to_smaller_int(large_int):
    # Convert the large integer to a string before hashing
    large_int_str = str(large_int)
    
    # Compute the SHA-256 hash of the string representation of the large integer
    hashed_bytes = hashlib.sha256(large_int_str.encode()).digest()
    
    # Convert the hashed bytes to an integer
    hashed_int = int.from_bytes(hashed_bytes, byteorder='big')
    
    # Generate a smaller integer by taking the modulo of a large number
    smaller_int = hashed_int % (10 ** 9)  # Restricting to a 9-digit number
    
    return smaller_int


def base64_encode(value):
    # Encode the concatenated string using Base64
    return base64.b64encode(value.encode()).decode()

def date_formatter(date):
    #date = datetime.strptime(date_string, '%d-%m-%Y')

    return date.strftime('%d, %a %Y')