# SecuRT — Simple Encrypted Vault

> Small, local CLI vault to encrypt/decrypt files and manage an in-vault directory index.

This project provides a minimal interactive command-line application to store encrypted files in a local vault (the `data/` directory) and manage a small virtual folder structure inside that vault.


Run the app:

```bash
python main.py
```

Type `help` inside the app for a list of commands and `help <command>` for details.


## Security Notice

**This is a learning/demonstration project.** While it uses industry-standard encryption (Fernet/AES-128), it currently has a **critical security limitation**: it uses a fixed salt for key derivation, which weakens security. 

**DO NOT use this for protecting truly sensitive data in production environments.**

For production use, the salt should be randomly generated per vault and stored alongside the encrypted data.


## Basic usage (examples)
- `open` — open the vault; you will be prompted for a password
- `encode <file_path>` — encrypt a file and add it to the vault (keeps original file)
- `decode <vault_filename> [output_path]` — decrypt a vault file; when `output_path` is omitted the file is written into the current working directory
- `create <name>` — create a folder inside the vault
- `delete <name>` — delete a file or empty folder
- `rename <old> <new>` — rename a file or folder
- `cd <folder>` / `ls` / `tree` — navigate and list vault contents
- `status` — show vault state and basic stats
- `close` — save and close the vault (writes encrypted config)

## Features

- **AES-128 encryption** via Fernet (cryptography library)
- **Virtual folder structure** - organize encrypted files in directories
- **Interactive CLI** with tab completion
- **Progress bars** for large file operations (>5MB)
- **Tree view** of vault structure
- **File metadata** with size information

## Development

The repository uses plain Python 3 and these main runtime dependencies:

- `cryptography` — encryption primitives (Fernet, PBKDF2)
- `prompt_toolkit` — interactive CLI and completion
- `colorama` — colored terminal output



Happy encrypting! 👋
