import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import name_settings

import colorama

def decode_file(output_path, password, names: list[name_settings.NameSettings], file_id):
    """
    Decrypts an encrypted file using a password and saves it to the specified output path.
    
    Args:
        output_path: Path where the decrypted file will be saved
        password: Password string to derive decryption key from
        names: List of NameSettings objects
        file_id: ID of the encrypted file to decrypt
    """
    # Construct input path from file_id
    input_path = f"data/encrypted_{file_id}"
    
    # Derive key from password (same as encode)
    salt = b'securert'  # Fixed salt (must match encode)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))

    print(f"{colorama.Fore.LIGHTGREEN_EX}Decryption key calculated successfully.{colorama.Style.RESET_ALL}")
    
    # Read the encrypted file
    with open(input_path, 'rb') as file:
        encrypted_data = file.read()

    print(f"{colorama.Fore.LIGHTGREEN_EX}Encrypted file read successfully. Starting decryption...{colorama.Style.RESET_ALL}")
    
    # Decrypt the data
    try:
        decrypted_data = key.decrypt(encrypted_data)
        print(f"{colorama.Fore.LIGHTGREEN_EX}File decrypted successfully.{colorama.Style.RESET_ALL}")
    except Exception as e:
        print(f"{colorama.Fore.RED}Decryption failed. Wrong password or corrupted file.{colorama.Style.RESET_ALL}")
        raise e
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Write decrypted file
    with open(output_path, 'wb') as file:
        file.write(decrypted_data)
    print(f"{colorama.Fore.LIGHTGREEN_EX}Decrypted file saved to: {output_path}{colorama.Style.RESET_ALL}")
    print(f"{colorama.Fore.GREEN}Decryption done.{colorama.Style.RESET_ALL}")
