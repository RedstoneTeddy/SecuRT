import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import name_settings

import colorama

def encode_file(file_path, password, names: list[name_settings.NameSettings], location: str = ""):
    """
    Encrypts a file using a password and stores it in the data folder.
    
    Args:
        file_path: Path to the file to encrypt
        password: Password string to derive encryption key from
        names: List of NameSettings to add the new file entry to
        location: Location (directory path) where the file should be stored in the vault
    """
    import sys
    import struct
    
    # Check file size for progress indication
    file_size = os.path.getsize(file_path)
    show_progress = file_size > 5 * 1024 * 1024  # Show for files > 5MB
    
    if show_progress:
        print(f"{colorama.Fore.CYAN}File size: {file_size / (1024*1024):.1f} MB{colorama.Style.RESET_ALL}")
    
    # Progress tracking
    def print_progress(current, total):
        if show_progress and total > 0:
            percentage = int((current / total) * 100)
            bar_length = 30
            filled = int(bar_length * current / total)
            bar = '█' * filled + '░' * (bar_length - filled)
            sys.stdout.write(f"\r{colorama.Fore.CYAN}[{bar}] {percentage}%")
            sys.stdout.flush()
            if current >= total:
                print()  # New line when complete
    
    # Step 1: Derive key
    print_progress(0, 100)
    salt = b'securert'  # Fixed salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))
    print_progress(10, 100)
    
    if not show_progress:
        print(f"{colorama.Fore.LIGHTGREEN_EX}Encryption key calculated successfully.{colorama.Style.RESET_ALL}")
    
    # Step 2: Read and encrypt the file in chunks
    print_progress(10, 100)
    with open(file_path, 'rb') as file:
        original_data = file.read()
    print_progress(20, 100)
    
    if not show_progress:
        print(f"{colorama.Fore.LIGHTGREEN_EX}File read successfully. Starting encryption...{colorama.Style.RESET_ALL}")
    
    # For large files, encrypt in chunks to show progress
    chunk_size = 10 * 1024 * 1024  # 10 MB chunks
    if len(original_data) > chunk_size:
        # Chunked encryption with progress
        encrypted_chunks = []
        num_chunks = (len(original_data) + chunk_size - 1) // chunk_size
        
        for i in range(num_chunks):
            start = i * chunk_size
            end = min(start + chunk_size, len(original_data))
            chunk = original_data[start:end]
            
            encrypted_chunk = key.encrypt(chunk)
            encrypted_chunks.append(encrypted_chunk)
            
            # Update progress (20% to 90% for encryption)
            progress = 20 + int((i + 1) / num_chunks * 70)
            print_progress(progress, 100)
        
        # Combine chunks with metadata for decryption
        # Format: MAGIC(16) + NUM_CHUNKS(4) + [CHUNK_SIZE(4) + CHUNK_DATA] * N
        output_data = b'SECURET_CHUNKED:'  # Magic header
        output_data += struct.pack('!I', len(encrypted_chunks))  # Number of chunks
        
        for chunk in encrypted_chunks:
            output_data += struct.pack('!I', len(chunk))  # Chunk size
            output_data += chunk  # Chunk data
        
        encrypted_data = output_data
    else:
        # Small file - encrypt as single block
        encrypted_data = key.encrypt(original_data)
        print_progress(90, 100)
    
    if not show_progress:
        print(f"{colorama.Fore.LIGHTGREEN_EX}File encrypted successfully.{colorama.Style.RESET_ALL}")
    
    # Step 3: Save to vault
    print_progress(90, 100)
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    
    new_file_id: int = name_settings.Calc_new_id(names)
    encrypted_filename = f"encrypted_{new_file_id}"
    encrypted_path = os.path.join(data_dir, encrypted_filename)

    names.append({
        "file_id": new_file_id,
        "name": os.path.basename(file_path),
        "location": location,
        "is_folder": False
    })
    
    with open(encrypted_path, 'wb') as file:
        file.write(encrypted_data)
    print_progress(100, 100)
    
    if not show_progress:
        print(f"{colorama.Fore.LIGHTGREEN_EX}Encrypted file saved.{colorama.Style.RESET_ALL}")
    
    print(f"{colorama.Fore.GREEN}Encryption done.{colorama.Style.RESET_ALL}")