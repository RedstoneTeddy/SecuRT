from typing import Literal, Optional, TypedDict

class NameSettings(TypedDict):
    file_id: int
    name: str
    location: str
    is_folder: bool

def Create_new_folder(names: list[NameSettings], folder_name: str, location: str) -> None:
    """Create a new folder entry in the names list."""
    new_folder_id: int = Calc_new_id(names)
    names.append({
        "file_id": new_folder_id,
        "name": folder_name,
        "location": location,
        "is_folder": True
    })

def Get_folder_files(names: list[NameSettings], location: str) -> list[str]:
    """Returns a list of all the names in a specific location"""
    output: list[str] = []
    for element in names:
        if location == element["location"]:
            output.append(element['name'])
    return output

def Get_index(names: list[NameSettings], name: str) -> int:
    i = -1
    for element in names:
        i += 1
        if element["name"] == name:
            return i
    return -1


def Rename_file(names: list[NameSettings], file_id: int, new_name: str) -> bool:
    """Rename a file or folder in the names list by its file_id."""
    for name in names:
        if name['file_id'] == file_id:
            name['name'] = new_name
            return True
    return False

def Check_name_exists(names: list[NameSettings], name: str) -> bool:
    """Check if a name already exists in the specified location."""
    for entry in names:
        if entry['name'] == name:
            return True
    return False


def Calc_new_id(names: list[NameSettings]) -> int:
    """Calculate a new unique file ID based on existing names."""
    if not names:
        return 1
    max_id = max(name['file_id'] for name in names)
    return max_id + 1


def Load_names(password: str) -> list[NameSettings]:
    """
    Load name settings from encrypted config file, decrypting with the provided password.
    
    Args:
        password: Password string to derive decryption key from
        
    Returns:
        List of NameSettings containing file configurations
    """
    import os
    import base64
    import json
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import colorama
    
    # Fixed input path
    input_path = "data/config.dat"
    
    # Check if config file exists
    if not os.path.exists(input_path):
        print(f"{colorama.Fore.YELLOW}Config file not found. Creating empty config.{colorama.Style.RESET_ALL}")
        return []
    
    # Derive key from password (same as encode/decode)
    salt = b'securert'  # Fixed salt (must match encode)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))
    
    # Read the encrypted config file
    with open(input_path, 'rb') as file:
        encrypted_data = file.read()

    
    # Decrypt the data
    try:
        decrypted_data = key.decrypt(encrypted_data)
        print(f"{colorama.Fore.LIGHTGREEN_EX}Config file decrypted successfully.{colorama.Style.RESET_ALL}")
    except Exception as e:
        print(f"{colorama.Fore.RED}Decryption failed. Wrong password or corrupted config file.{colorama.Style.RESET_ALL}")
        raise e
    
    # Parse JSON data
    names = json.loads(decrypted_data.decode('utf-8'))
    print(f"{colorama.Fore.GREEN}Loaded {len(names)} name settings.{colorama.Style.RESET_ALL}")
    
    return names


def Store_names(names: list[NameSettings], password: str) -> None:
    """
    Store name settings to encrypted config file, encrypting with the provided password.
    
    Args:
        names: List of NameSettings to store
        password: Password string to derive encryption key from
    """
    import os
    import base64
    import json
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import colorama
    
    # Fixed output path
    output_path = "data/config.dat"
    
    # Derive key from password (same as encode/decode)
    salt = b'securert'  # Fixed salt (must match encode)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))
    
    # Convert names list to JSON
    json_data = json.dumps(names, indent=2)
    original_data = json_data.encode('utf-8')

    # Encrypt the data
    encrypted_data = key.encrypt(original_data)

    # Create data directory if it doesn't exist
    data_dir = os.path.dirname(output_path)
    if data_dir:
        os.makedirs(data_dir, exist_ok=True)
    
    # Write encrypted config file
    with open(output_path, 'wb') as file:
        file.write(encrypted_data)
    print(f"{colorama.Fore.LIGHTGREEN_EX}Config file saved{colorama.Style.RESET_ALL}")

