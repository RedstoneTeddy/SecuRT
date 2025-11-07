# SecuRT — Simple Encrypted Vault

> Small, local CLI vault to encrypt/decrypt files and manage an in-vault directory index.

This project provides a minimal interactive command-line application to store encrypted files in a local vault (the `data/` directory) and manage a small virtual folder structure inside that vault.


Run the app:

```powershell
python main.py
```

Type `help` inside the app for a list of commands and `help <command>` for details.

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

## Implementation notes & caveats

- Encrypted blobs are stored under the repository `data/` directory, named `encrypted_<id>`.
- The vault index (file/folder metadata) is encrypted and saved to `data/config.dat`.
- Large files are handled using a chunked format (`SECURET_CHUNKED:`) so the app can encrypt/decrypt in pieces and display progress.
- Currently the prototype uses a fixed salt for key derivation in several places; this weakens security for real-world use. For production you should switch to a per-vault random salt stored alongside the encrypted config.

## Development

The repository uses plain Python 3 and these main runtime dependencies:

- `cryptography` — encryption primitives (Fernet, PBKDF2)
- `prompt_toolkit` — interactive CLI and completion
- `colorama` — colored terminal output



Happy encrypting! 👋
