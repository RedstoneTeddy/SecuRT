import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import name_settings

import colorama

def encode_file(file_path, password, names: list[name_settings.NameSettings]):
    """
    Encrypts a file using a password and stores it in the data folder.
    
    Args:
        file_path: Path to the file to encrypt
        password: Password string to derive encryption key from
    """
    # Derive key from password
    salt = b'securert'  # Fixed salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))

    print(f"{colorama.Fore.LIGHTGREEN_EX}Encryption key calculated successfully.{colorama.Style.RESET_ALL}")
    
    # Read the original file
    with open(file_path, 'rb') as file:
        original_data = file.read()

    print(f"{colorama.Fore.LIGHTGREEN_EX}File read successfully. Starting encryption...{colorama.Style.RESET_ALL}")
    
    # Encrypt the data
    encrypted_data = key.encrypt(original_data)

    print(f"{colorama.Fore.LIGHTGREEN_EX}File encrypted successfully.{colorama.Style.RESET_ALL}")
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(file_path)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate output filename
    new_file_id: int = name_settings.Calc_new_id(names)
    encrypted_filename = f"encrypted_{new_file_id}"
    encrypted_path = os.path.join(data_dir, encrypted_filename)

    names.append({
        "file_id": new_file_id,
        "name": os.path.basename(file_path),
        "location": ""
    })
    
    # Write encrypted file
    with open(encrypted_path, 'wb') as file:
        file.write(encrypted_data)
    print(f"{colorama.Fore.LIGHTGREEN_EX}Encrypted file saved.{colorama.Style.RESET_ALL}")
    print(f"{colorama.Fore.GREEN}Encryption done.{colorama.Style.RESET_ALL}")