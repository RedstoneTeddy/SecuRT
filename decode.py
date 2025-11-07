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
    import sys
    import struct
    
    # Construct input path from file_id
    input_path = f"data/encrypted_{file_id}"
    
    # Check file size for progress indication
    file_size = 0
    if os.path.exists(input_path):
        file_size = os.path.getsize(input_path)
        show_progress = file_size > 5 * 1024 * 1024  # Show for files > 5MB
        
        if show_progress:
            print(f"{colorama.Fore.CYAN}File size: {file_size / (1024*1024):.1f} MB{colorama.Style.RESET_ALL}")
    else:
        show_progress = False
    
    # Progress tracking
    def print_progress(current, total):
        if show_progress and total > 0:
            percentage = int((current / total) * 100)
            bar_length = 30
            filled = int(bar_length * current / total)
            bar = '█' * filled + '░' * (bar_length - filled)
            sys.stdout.write(f"\r{colorama.Fore.CYAN}[{bar}] {percentage}%{colorama.Style.RESET_ALL}")
            sys.stdout.flush()
            if current >= total:
                print()  # New line when complete
    
    # Step 1: Derive key
    print_progress(0, 100)
    salt = b'securert'  # Fixed salt (must match encode)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))
    print_progress(10, 100)
    
    if not show_progress:
        print(f"{colorama.Fore.LIGHTGREEN_EX}Decryption key calculated successfully.{colorama.Style.RESET_ALL}")
    
    # Step 2: Read the encrypted file and process in chunks
    print_progress(10, 100)
    
    if not show_progress:
        print(f"{colorama.Fore.LIGHTGREEN_EX}Starting decryption...{colorama.Style.RESET_ALL}")
    
    try:
        with open(input_path, 'rb') as file:
            # Read the metadata header
            encrypted_data = file.read()
        
        print_progress(20, 100)
        
        # Check if file uses chunked format (has our magic header)
        if encrypted_data.startswith(b'SECURET_CHUNKED:'):
            # Chunked format - decrypt chunk by chunk
            offset = 16  # Skip magic header
            num_chunks = struct.unpack('!I', encrypted_data[offset:offset+4])[0]
            offset += 4
            
            decrypted_chunks = []
            for i in range(num_chunks):
                # Read chunk size
                chunk_size = struct.unpack('!I', encrypted_data[offset:offset+4])[0]
                offset += 4
                
                # Read and decrypt chunk
                encrypted_chunk = encrypted_data[offset:offset+chunk_size]
                offset += chunk_size
                
                decrypted_chunk = key.decrypt(encrypted_chunk)
                decrypted_chunks.append(decrypted_chunk)
                
                # Update progress (20% to 90% for decryption)
                progress = 20 + int((i + 1) / num_chunks * 70)
                print_progress(progress, 100)
            
            decrypted_data = b''.join(decrypted_chunks)
        else:
            # Old format - decrypt as single block
            decrypted_data = key.decrypt(encrypted_data)
            print_progress(90, 100)
        
        if not show_progress:
            print(f"{colorama.Fore.LIGHTGREEN_EX}File decrypted successfully.{colorama.Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{colorama.Fore.RED}Decryption failed. Wrong password or corrupted file.{colorama.Style.RESET_ALL}")
        raise e
    
    # Step 3: Write output file
    print_progress(90, 100)
    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    with open(output_path, 'wb') as file:
        file.write(decrypted_data)
    print_progress(100, 100)
    
    if not show_progress:
        print(f"{colorama.Fore.LIGHTGREEN_EX}Decrypted file saved to: {output_path}{colorama.Style.RESET_ALL}")
    
    print(f"{colorama.Fore.GREEN}Decryption done.{colorama.Style.RESET_ALL}")
