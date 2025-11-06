import colorama
from typing import List 


def cmd_help(args: List[str]) -> None:
    """Display help information."""
    help_text = ""

    if args: # User wants help for a specific command
        cmd: str = args[0].lower()
        match cmd:
            case "exit" | "quit":
                help_text += f"{colorama.Fore.CYAN}exit{colorama.Fore.RESET} - Exit the application and close SecuRT.\n"
                help_text += f"{colorama.Fore.YELLOW}Alias:{colorama.Fore.RESET} quit\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Safely exits the SecuRT application. If the vault is open, it will\n"
                help_text += "  automatically save and close before exiting.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  exit\n"
                help_text += "  quit"
            
            case "help":
                help_text += f"{colorama.Fore.CYAN}help [command]{colorama.Fore.RESET} - Display help information.\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Shows available commands and their usage. When called with a command\n"
                help_text += "  name, displays detailed help for that specific command.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  help           - Show all available commands\n"
                help_text += "  help <command> - Show detailed help for a specific command\n"
                help_text += f"\n{colorama.Fore.WHITE}Examples:{colorama.Fore.RESET}\n"
                help_text += "  help\n"
                help_text += "  help create\n"
                help_text += "  help cd"
            
            case "open":
                help_text += f"{colorama.Fore.CYAN}open <password>{colorama.Fore.RESET} - Open and decrypt the vault.\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Opens the encrypted vault using the provided password. Loads all\n"
                help_text += "  stored files and folders into memory. The vault must be opened before\n"
                help_text += "  you can create, delete, rename, or navigate folders.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  open <password>\n"
                help_text += f"\n{colorama.Fore.WHITE}Example:{colorama.Fore.RESET}\n"
                help_text += "  open my_secure_password\n"
                help_text += f"\n{colorama.Fore.YELLOW}Note:{colorama.Fore.RESET} If the password is incorrect, vault opening will fail."
            
            case "close":
                help_text += f"{colorama.Fore.CYAN}close{colorama.Fore.RESET} - Save and close the vault.\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Saves all changes to the encrypted vault and closes it. All current\n"
                help_text += "  directory information and loaded data will be cleared from memory.\n"
                help_text += "  You must open the vault again to access your files.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  close\n"
                help_text += f"\n{colorama.Fore.YELLOW}Note:{colorama.Fore.RESET} If saving fails, you'll be asked to confirm before closing."
            
            case "status":
                help_text += f"{colorama.Fore.CYAN}status{colorama.Fore.RESET} - Display current vault status and statistics.\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Shows whether the vault is currently open or closed. If open, displays\n"
                help_text += "  detailed statistics including total entries, folder/file counts, and\n"
                help_text += "  your current directory location.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  status"
            
            case "rename" | "mv":
                help_text += f"{colorama.Fore.CYAN}rename <old_name> <new_name>{colorama.Fore.RESET} - Rename a folder or file.\n"
                help_text += f"{colorama.Fore.YELLOW}Alias:{colorama.Fore.RESET} mv\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Renames a folder or file in the current directory. If renaming a folder,\n"
                help_text += "  all nested files and folders will maintain their paths relative to the\n"
                help_text += "  renamed folder. Changes are automatically saved.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  rename <old_name> <new_name>\n"
                help_text += "  mv <old_name> <new_name>\n"
                help_text += f"\n{colorama.Fore.WHITE}Examples:{colorama.Fore.RESET}\n"
                help_text += "  rename old_folder new_folder\n"
                help_text += "  mv document.txt report.txt\n"
                help_text += f"\n{colorama.Fore.YELLOW}Note:{colorama.Fore.RESET} The new name must not already exist in the current directory."
            
            case "delete" | "rm":
                help_text += f"{colorama.Fore.CYAN}delete <name>{colorama.Fore.RESET} - Delete a folder or file from the vault.\n"
                help_text += f"{colorama.Fore.YELLOW}Alias:{colorama.Fore.RESET} rm\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Permanently deletes a folder or file from the current directory.\n"
                help_text += "  Folders must be empty before they can be deleted. This action cannot\n"
                help_text += "  be undone. Changes are automatically saved.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  delete <name>\n"
                help_text += "  rm <name>\n"
                help_text += f"\n{colorama.Fore.WHITE}Examples:{colorama.Fore.RESET}\n"
                help_text += "  delete my_folder\n"
                help_text += "  rm old_file.txt\n"
                help_text += f"\n{colorama.Fore.RED}Warning:{colorama.Fore.RESET} This action is permanent and cannot be undone!"
            
            case "create" | "mkdir":
                help_text += f"{colorama.Fore.CYAN}create <name>{colorama.Fore.RESET} - Create a new folder in the vault.\n"
                help_text += f"{colorama.Fore.YELLOW}Alias:{colorama.Fore.RESET} mkdir\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Creates a new folder in the current directory. The folder name must\n"
                help_text += "  be unique within the current directory. Use 'cd <folder>' to navigate\n"
                help_text += "  into the newly created folder. Changes are automatically saved.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  create <name>\n"
                help_text += "  mkdir <name>\n"
                help_text += f"\n{colorama.Fore.WHITE}Examples:{colorama.Fore.RESET}\n"
                help_text += "  create documents\n"
                help_text += "  mkdir my_new_folder\n"
                help_text += f"\n{colorama.Fore.YELLOW}Note:{colorama.Fore.RESET} The folder name must not already exist in the current directory."
            
            case "cd":
                help_text += f"{colorama.Fore.CYAN}cd [directory]{colorama.Fore.RESET} - Change or display current directory.\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Navigate between folders in the vault. When called without arguments,\n"
                help_text += "  displays the current directory path. Use '..' to go up one level.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  cd              - Show current directory\n"
                help_text += "  cd <directory>  - Navigate to a folder\n"
                help_text += "  cd ..           - Go up one level\n"
                help_text += f"\n{colorama.Fore.WHITE}Examples:{colorama.Fore.RESET}\n"
                help_text += "  cd\n"
                help_text += "  cd documents\n"
                help_text += "  cd ..\n"
                help_text += f"\n{colorama.Fore.YELLOW}Tip:{colorama.Fore.RESET} Use 'ls' to see available folders in the current directory."
            
            case "ls":
                help_text += f"{colorama.Fore.CYAN}ls{colorama.Fore.RESET} - List contents of current directory.\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Lists all files and folders in the current directory. Folders are\n"
                help_text += "  displayed in yellow with a '/' suffix, while files are shown in white.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  ls\n"
                help_text += f"\n{colorama.Fore.WHITE}Display format:{colorama.Fore.RESET}\n"
                help_text += f"  {colorama.Fore.YELLOW}[Folder] folder_name/{colorama.Fore.RESET}\n"
                help_text += f"  {colorama.Fore.WHITE}         file_name{colorama.Fore.RESET}"
            
            case "clear" | "cls":
                help_text += f"{colorama.Fore.CYAN}clear{colorama.Fore.RESET} - Clear the terminal screen.\n"
                help_text += f"{colorama.Fore.YELLOW}Alias:{colorama.Fore.RESET} cls\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Clears all text from the terminal screen, providing a clean workspace.\n"
                help_text += "  Works on both Windows (cls) and Unix/Linux (clear) systems.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  clear\n"
                help_text += "  cls"
            
            case "encode":
                help_text += f"{colorama.Fore.CYAN}encode <file_path>{colorama.Fore.RESET} - Encrypt and add a file to the vault.\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Encrypts a file from your file system and adds it to the vault in the\n"
                help_text += "  current directory. The original file remains unchanged. The encrypted\n"
                help_text += "  file is stored in the 'data' folder with a unique ID. Changes are\n"
                help_text += "  automatically saved.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  encode <file_path>\n"
                help_text += f"\n{colorama.Fore.WHITE}Examples:{colorama.Fore.RESET}\n"
                help_text += "  encode C:\\Documents\\secret.txt\n"
                help_text += "  encode /home/user/documents/report.pdf\n"
                help_text += "  encode \"./my file.docx\"\n"
                help_text += f"\n{colorama.Fore.WHITE}Requirements:{colorama.Fore.RESET}\n"
                help_text += "  - Vault must be open\n"
                help_text += "  - File must exist and be readable\n"
                help_text += "  - File path can be absolute or relative\n"
                help_text += "  - Filename must not already exist in current directory\n"
                help_text += f"\n{colorama.Fore.YELLOW}Note:{colorama.Fore.RESET} Use quotes around file paths with spaces."
            
            case "decode":
                help_text += f"{colorama.Fore.CYAN}decode <vault_filename> [output_path]{colorama.Fore.RESET} - Decrypt and extract a file from the vault.\n"
                help_text += f"\n{colorama.Fore.WHITE}Description:{colorama.Fore.RESET}\n"
                help_text += "  Decrypts a file from the vault and saves it to your file system. If no\n"
                help_text += "  output path is specified, the file will be saved to the current working\n"
                help_text += "  directory with its original filename. The file in the vault remains\n"
                help_text += "  unchanged. The output path can be absolute or relative and will be\n"
                help_text += "  created if needed.\n"
                help_text += f"\n{colorama.Fore.WHITE}Usage:{colorama.Fore.RESET}\n"
                help_text += "  decode <vault_filename>                 - Extract to current directory\n"
                help_text += "  decode <vault_filename> <output_path>   - Extract to specific path\n"
                help_text += f"\n{colorama.Fore.WHITE}Examples:{colorama.Fore.RESET}\n"
                help_text += "  decode secret.txt\n"
                help_text += "  decode secret.txt C:\\Extracted\\secret.txt\n"
                help_text += "  decode report.pdf /home/user/downloads/report.pdf\n"
                help_text += "  decode \"my file.docx\" \"./extracted file.docx\"\n"
                help_text += f"\n{colorama.Fore.WHITE}Requirements:{colorama.Fore.RESET}\n"
                help_text += "  - Vault must be open\n"
                help_text += "  - File must exist in current directory of vault\n"
                help_text += "  - Vault filename cannot be a folder\n"
                help_text += "  - You will be prompted if output file already exists\n"
                help_text += f"\n{colorama.Fore.YELLOW}Note:{colorama.Fore.RESET} Use quotes around paths with spaces."
            
            case _:
                help_text += f"{colorama.Fore.RED}No help available for unknown command: {cmd}{colorama.Fore.RESET}\n"
                help_text += f"\nType '{colorama.Fore.CYAN}help{colorama.Fore.RESET}' to see all available commands."
    
    else: # General help
        help_text += "Available commands:\n"
        help_text += f"{colorama.Fore.CYAN} help{colorama.Fore.RESET}    - Show this help message (Use 'help <command>' for more details)\n"
        help_text += f"{colorama.Fore.CYAN} exit{colorama.Fore.RESET}    - Exit the application\n"
        help_text += f"{colorama.Fore.CYAN} open {colorama.Fore.RESET}   - Open the vault with the specified password\n"
        help_text += f"{colorama.Fore.CYAN} close{colorama.Fore.RESET}   - Close the vault\n"
        help_text += f"{colorama.Fore.CYAN} status{colorama.Fore.RESET}  - Show whether the vault is open or closed\n"
        help_text += f"{colorama.Fore.CYAN} create{colorama.Fore.RESET}  - Create a new folder in the vault\n"
        help_text += f"{colorama.Fore.CYAN} delete{colorama.Fore.RESET}  - Delete a folder or file from the vault\n"
        help_text += f"{colorama.Fore.CYAN} rename{colorama.Fore.RESET}  - Rename a folder or file in the vault (alias: mv)\n"
        help_text += f"{colorama.Fore.CYAN} cd{colorama.Fore.RESET}      - Change the current directory in the vault\n"
        help_text += f"{colorama.Fore.CYAN} ls{colorama.Fore.RESET}      - List all files and folders in the current directory of the vault\n"
        help_text += f"{colorama.Fore.CYAN} encode{colorama.Fore.RESET}  - Encrypt and add a file to the vault\n"
        help_text += f"{colorama.Fore.CYAN} decode{colorama.Fore.RESET}  - Decrypt and extract a file from the vault\n"
        help_text += f"{colorama.Fore.CYAN} clear{colorama.Fore.RESET}   - Clear the terminal screen (alias: cls)\n"
        help_text += f"\n{colorama.Fore.YELLOW}Command aliases:{colorama.Fore.RESET}\n"
        help_text += "  quit = exit, mkdir = create, rm = delete, mv = rename, cls = clear\n"


    print(help_text)

