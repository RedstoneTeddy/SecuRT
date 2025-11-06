import sys
from typing import List, Optional

from os import path as os_path
from os import chdir as os_chdir
import os
directory = os_path.dirname(os_path.abspath(__file__))
os_chdir(directory) #Small Bugfix, that in some situations, the code_path isn't correct

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
import colorama
import shlex

import help_menu

import name_settings
import encode
import decode

class SecuRT_App:
    """Main interactive SecuRT_App class."""
    
    def __init__(self):
        self.running: bool = True

        self.config = {

        }

        
        self.names: list[name_settings.NameSettings] = []
        self.password: str = ""

        self.current_dir: str = ""

        self.completer = NestedCompleter.from_nested_dict({})

        # Custom style for the prompt
        self.prompt_style = Style.from_dict({
            "prompt": "#ff7982",
            "prompt2": "#00aaff bold"
        })

        # Create prompt session
        self.session = PromptSession(
            completer=self.completer,
            style=self.prompt_style,
            complete_while_typing=True
        )
        self._update_completer()


    ##########################
    #### Helper Functions ####
    ##########################




    def _require_vault_open(self) -> bool:
        """Check if vault is open, print error if not. Returns True if open, False if closed."""
        if self.password == "":
            print(f"{colorama.Fore.RED}Error: Vault is not open. Use 'open <password>' first.{colorama.Style.RESET_ALL}")
            return False
        return True

    def _update_completer(self) -> None:
        """Update the auto-completion with current folder/file names."""
        if self.password == "":
            # Vault closed - basic commands only
            current_names = {}
        else:
            # Add current directory's files and folders to completion
            current_names = {}
            for entry in self.names:
                if entry['location'] == self.current_dir:
                    current_names[entry['name']] = None
        
        self.completer = NestedCompleter.from_nested_dict({
            "exit": None,
            "quit": None,
            "help": {
                "help": None,
                "exit": None,
                "open": None,
                "close": None,
                "status": None,
                "create": None,
                "delete": None,
                "rename": None,
                "cd": None,
                "ls": None,
                "clear": None,
                "encode": None,
                "decode": None
            },
            "open": None,
            "close": None,
            "status": None,
            "create": None,
            "mkdir": None,
            "delete": current_names,
            "rm": current_names,
            "rename": current_names,
            "mv": current_names,
            "cd": current_names,
            "ls": None,
            "clear": None,
            "cls": None,
            "encode": None,
            "decode": current_names
        })
        self.session.completer = self.completer

    def get_prompt_message(self) -> HTML:
        """Generate the prompt message with styling."""
        if self.password != "":
            return HTML(f"<prompt2>SecuRT ('/{self.current_dir}')&gt;</prompt2> ")
        return HTML('<prompt>SecuRT&gt;</prompt> ')
    

    ###################
    #### Main Loop ####
    ###################

        
    def run(self):
        """Main application loop."""
        print(f"{colorama.Fore.LIGHTRED_EX}################")
        print(f"{colorama.Fore.LIGHTRED_EX}#### SecuRT ####")
        print(f"{colorama.Fore.LIGHTRED_EX}################")
        print(f"{colorama.Fore.WHITE}Type 'help' for available commands")
        print(f"{colorama.Fore.WHITE}Type 'exit' to quit")
        print("")

        # Main loop
        while self.running:
            try:
                command: str = self.session.prompt(self.get_prompt_message())
                self.process_command(command)

            except KeyboardInterrupt:
                print()
                print(f"{colorama.Fore.YELLOW}Use 'exit' to leave the application.")
                continue

            except EOFError:
                print()
                self.cmd_exit([])
                break


    
    def process_command(self, command: str) -> None:
        """Process a single command input."""
        if not command.strip():
            return

        args: list[str] = shlex.split(command.strip())
        cmd: str = args[0].lower()

        # Command routing (with aliases)
        commands = {
            "exit": self.cmd_exit,
            "quit": self.cmd_exit,
            "help": self.cmd_help,
            "open": self.cmd_open,
            "close": self.cmd_close,
            "status": self.cmd_status,
            "create": self.cmd_create,
            "mkdir": self.cmd_create,
            "delete": self.cmd_delete,
            "rm": self.cmd_delete,
            "rename": self.cmd_rename,
            "mv": self.cmd_rename,
            "cd": self.cmd_cd,
            "ls": self.cmd_ls,
            "clear": self.cmd_clear,
            "cls": self.cmd_clear,
            "encode": self.cmd_encode,
            "decode": self.cmd_decode
        }

        if cmd in commands:
            try: 
                commands[cmd](args[1:])
                print("")
            except Exception as e:
                print(f"{colorama.Fore.RED}Error: Failed to execute command '{cmd}' - {e}{colorama.Style.RESET_ALL}")
        else:
            print(f"{colorama.Fore.RED}Error: Unknown command '{cmd}'. Type 'help' for a list of commands.{colorama.Style.RESET_ALL}")
    

    ####################################
    #### Process different commands ####
    ####################################


    def cmd_exit(self, args: List[str]) -> None:
        """Handle the 'exit' command to terminate the application."""
        if self.password != "":
            try:
                self.cmd_close([])
            except Exception as e:
                print(f"{colorama.Fore.RED}Error during vault closure: {e}{colorama.Style.RESET_ALL}")
        print("Exiting the application. Goodbye!")
        self.running = False

    def cmd_status(self, args: List[str]) -> None:
        """Display if the vault is open or closed."""
        print(f"{colorama.Fore.CYAN}Vault status:{colorama.Style.RESET_ALL}")
        if self.password:
            print(f"{colorama.Fore.GREEN}Vault is OPEN.{colorama.Style.RESET_ALL}")
            print(f"  Total entries: {len(self.names)}")
            folder_count = sum(1 for entry in self.names if entry.get('is_folder', False))
            file_count = len(self.names) - folder_count
            print(f"  Folders: {folder_count}, Files: {file_count}")
            print(f"  Current directory: {self.current_dir or '/'}")
        else:
            print(f"{colorama.Fore.RED}Vault is CLOSED.{colorama.Style.RESET_ALL}")

    def cmd_close(self, args: List[str]) -> None:
        """Close the vault by clearing the password."""
        if self.password != "":
            try:
                name_settings.Store_names(self.names, self.password)
            except Exception as e:
                print(f"{colorama.Fore.RED}Error: Failed to save vault - {e}{colorama.Style.RESET_ALL}")
                print(f"{colorama.Fore.YELLOW}Warning: Your changes may not have been saved!{colorama.Style.RESET_ALL}")
                response = input("Do you still want to close the vault? (y/n): ").lower()
                if response != 'y':
                    print(f"{colorama.Fore.CYAN}Vault remains open.{colorama.Style.RESET_ALL}")
                    return
        self.password = ""
        self.names = []
        self.current_dir = ""
        self._update_completer()  # Reset tab completion
        print(f"{colorama.Fore.YELLOW}Vault has been closed.{colorama.Style.RESET_ALL}")

    def cmd_open(self, args: List[str]) -> None:
        """Open the vault by prompting for a password and loading names."""
        if self.password:
            print(f"{colorama.Fore.YELLOW}Vault is already open.{colorama.Style.RESET_ALL}")
            return
        if len(args) < 1:
            print(f"{colorama.Fore.RED}Error: Password required. Usage: open <password>{colorama.Style.RESET_ALL}")
            return

        self.password = args[0]
        try:
            self.names = name_settings.Load_names(self.password)
            self._update_completer()  # Update tab completion with loaded data
            print(f"{colorama.Fore.GREEN}Vault opened successfully with {len(self.names)} entries.{colorama.Style.RESET_ALL}")
        except Exception as e:
            self.password = ""
            self.names = []
            print(f"{colorama.Fore.RED}Error: Failed to open vault - {e}{colorama.Style.RESET_ALL}")

    def cmd_create(self, args: List[str]) -> None:
        """Create a new folder in the vault, at the current directory."""
        if not self._require_vault_open():
            return
        if len(args) < 1:
            print(f"{colorama.Fore.RED}Error: Folder name required. Usage: create <name>{colorama.Style.RESET_ALL}")
            return
        folder_name = args[0]
        
        if name_settings.Check_name_exists(self.names, folder_name):
            print(f"{colorama.Fore.RED}Error: A folder or file with the name '{folder_name}' already exists.{colorama.Style.RESET_ALL}")
            return
        try:
            name_settings.Create_new_folder(self.names, folder_name, self.current_dir)
            name_settings.Store_names(self.names, self.password)
            self._update_completer()  # Update tab completion
            print(f"{colorama.Fore.GREEN}Folder '{folder_name}' created successfully.{colorama.Style.RESET_ALL}")
        except Exception as e:
            print(f"{colorama.Fore.RED}Error: Failed to create folder - {e}{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.YELLOW}Your changes may not be saved. Try 'close' to save manually.{colorama.Style.RESET_ALL}")

    def cmd_delete(self, args: List[str]) -> None:
        """Delete a folder or file from the vault. If a folder, only delete if there do not exist files / folders with that location inside"""
        if not self._require_vault_open():
            return
        if len(args) < 1:
            print(f"{colorama.Fore.RED}Error: Name required. Usage: delete <name>{colorama.Style.RESET_ALL}")
            return
        name_to_delete = args[0]
        
        if not name_settings.Check_name_exists(self.names, name_to_delete):
            print(f"{colorama.Fore.RED}Error: No folder or file with the name '{name_to_delete}' exists in the current directory.{colorama.Style.RESET_ALL}")
            return
        try:
            i: int = -1
            for index, entry in enumerate(self.names):
                if entry['name'] == name_to_delete:
                    i = index
                    break
            if i == -1:
                print(f"{colorama.Fore.RED}Error: No folder or file with the name '{name_to_delete}' exists.{colorama.Style.RESET_ALL}")
                return
            check_location: str = self.current_dir + name_to_delete + "/"
            if self.names[i]['is_folder']:
                for entry in self.names:
                    if entry['location'].startswith(check_location):
                        print(f"{colorama.Fore.RED}Error: Cannot delete folder '{name_to_delete}' - folder is not empty.{colorama.Style.RESET_ALL}")
                        return
            del self.names[i]
            self.current_dir = self.current_dir.replace(name_to_delete + "/", "")
            name_settings.Store_names(self.names, self.password)
            self._update_completer()  # Update tab completion
            print(f"{colorama.Fore.GREEN}'{name_to_delete}' deleted successfully.{colorama.Style.RESET_ALL}")
        except Exception as e:
            print(f"{colorama.Fore.RED}Error: Failed to delete '{name_to_delete}' - {e}{colorama.Style.RESET_ALL}")


    def cmd_rename(self, args: List[str]) -> None:
        """Rename a folder or file in the vault."""
        if not self._require_vault_open():
            return
        if len(args) < 2:
            print(f"{colorama.Fore.RED}Error: Two names required. Usage: rename <old_name> <new_name>{colorama.Style.RESET_ALL}")
            return
        old_name = args[0]
        new_name = args[1]
        
        if not name_settings.Check_name_exists(self.names, old_name):
            print(f"{colorama.Fore.RED}Error: No folder or file with the name '{old_name}' exists.{colorama.Style.RESET_ALL}")
            return
        if name_settings.Check_name_exists(self.names, new_name):
            print(f"{colorama.Fore.RED}Error: A folder or file with the name '{new_name}' already exists.{colorama.Style.RESET_ALL}")
            return
        try:
            file_i: int = name_settings.Get_index(self.names, old_name)
            success: bool = name_settings.Rename_file(self.names, self.names[file_i]['file_id'], new_name)
            if not success:
                print(f"{colorama.Fore.RED}Error: Failed to rename '{old_name}' to '{new_name}'.{colorama.Style.RESET_ALL}")
                return
            if self.names[file_i]['is_folder']:
                old_location: str = self.current_dir + old_name + "/"
                new_location: str = self.current_dir + new_name + "/"
                for entry in self.names:
                    if entry['location'].startswith(old_location):
                        entry['location'] = entry['location'].replace(old_location, new_location, 1)
            self.current_dir: str = self.current_dir.replace(old_name + "/", new_name + "/")
            name_settings.Store_names(self.names, self.password)
            self._update_completer()  # Update tab completion
            print(f"{colorama.Fore.GREEN}Renamed '{old_name}' to '{new_name}' successfully.{colorama.Style.RESET_ALL}")
        except Exception as e:
            print(f"{colorama.Fore.RED}Error: Failed to rename - {e}{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.YELLOW}Your changes may not be saved. Try 'close' to save manually.{colorama.Style.RESET_ALL}")
            

    def cmd_cd(self, args: List[str]) -> None:
        """Change the current directory in the vault. If no argument is given, output the current directory. If argument is == ".." go back once"""
        if not self._require_vault_open():
            return
        if len(args) == 0:
            print(f"{colorama.Fore.CYAN}Current directory: '{self.current_dir}'{colorama.Style.RESET_ALL}")
            return
        target_dir = args[0]
        if target_dir == "..":
            if self.current_dir == "":
                print(f"{colorama.Fore.YELLOW}Already at root directory.{colorama.Style.RESET_ALL}")
                return
            else:
                # Go back one directory
                parts = self.current_dir.strip("/").split("/")
                parts = parts[:-1]  # Remove last part
                self.current_dir = "/".join(parts)
                if self.current_dir != "":
                    self.current_dir += "/"
                self._update_completer()  # Update tab completion
                print(f"{colorama.Fore.GREEN}Moved to directory: '{self.current_dir}'{colorama.Style.RESET_ALL}")
                return
        else:
            # Check if the target directory exists
            full_target = self.current_dir + target_dir + "/"
            exists = False
            for entry in self.names:
                if entry['is_folder'] and entry['location'] == self.current_dir and entry["name"] == target_dir:
                    exists = True
                    break
            if not exists:
                print(f"{colorama.Fore.RED}Error: Directory '{target_dir}' does not exist in the current directory.{colorama.Style.RESET_ALL}")
                return
            self.current_dir = full_target
            self._update_completer()  # Update tab completion
            print(f"{colorama.Fore.GREEN}Moved to directory: '{self.current_dir}'{colorama.Style.RESET_ALL}")


    def cmd_ls(self, args: List[str]) -> None:
        """Outputs all files and folder (specially marked) in the current directory."""
        if not self._require_vault_open():
            return
        display_dir = self.current_dir or "/"
        print(f"{colorama.Fore.CYAN}Contents of directory '{display_dir}':{colorama.Style.RESET_ALL}")
        
        folders = []
        files = []
        
        for entry in self.names:
            if entry['location'] == self.current_dir:
                if entry['is_folder']:
                    folders.append(entry['name'])
                else:
                    # Get file size if possible
                    encrypted_path = f"data/encrypted_{entry['file_id']}"
                    size = ""
                    if os.path.exists(encrypted_path):
                        file_size = os.path.getsize(encrypted_path)
                        if file_size < 1024:
                            size = f"{file_size} B"
                        elif file_size < 1024 * 1024:
                            size = f"{file_size / 1024:.1f} KB"
                        else:
                            size = f"{file_size / (1024 * 1024):.1f} MB"
                    files.append((entry['name'], size))
        
        if not folders and not files:
            print(f"{colorama.Fore.YELLOW}(No files or folders found in this directory){colorama.Style.RESET_ALL}")
            return
        
        # Print folders first
        for folder in sorted(folders):
            print(f"{colorama.Fore.YELLOW}[Folder] {folder}/{colorama.Style.RESET_ALL}")
        
        # Then files with sizes
        for filename, size in sorted(files):
            size_str = f" ({size})" if size else ""
            print(f"{colorama.Fore.WHITE}         {filename}{size_str}{colorama.Style.RESET_ALL}")

    def cmd_clear(self, args: List[str]) -> None:
        """Clear the terminal screen."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def cmd_encode(self, args: List[str]) -> None:
        """Encode (encrypt) a file and add it to the vault."""
        if not self._require_vault_open():
            return
        if len(args) < 1:
            print(f"{colorama.Fore.RED}Error: File path required. Usage: encode <file_path>{colorama.Style.RESET_ALL}")
            return
        
        file_path = args[0]
        abs_path = os.path.abspath(file_path)
        
        # Check if file exists
        if not os.path.exists(abs_path):
            print(f"{colorama.Fore.RED}Error: File does not exist.{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.YELLOW}  Tried path: {abs_path}{colorama.Style.RESET_ALL}")
            return
        
        # Check if file is a directory
        if os.path.isdir(abs_path):
            print(f"{colorama.Fore.RED}Error: Path is a directory, not a file.{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.YELLOW}  Path: {abs_path}{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.CYAN}  Hint: Only files can be encoded, not directories.{colorama.Style.RESET_ALL}")
            return
        
        # Get the filename
        filename = os.path.basename(abs_path)
        
        # Check if filename already exists in current directory
        if name_settings.Check_name_exists(self.names, filename):
            print(f"{colorama.Fore.RED}Error: A file with the name '{filename}' already exists in the current directory.{colorama.Style.RESET_ALL}")
            return
        
        try:
            # Encode the file (use absolute path)
            encode.encode_file(abs_path, self.password, self.names, self.current_dir)
            name_settings.Store_names(self.names, self.password)
            self._update_completer()  # Update tab completion
            print(f"{colorama.Fore.GREEN}File '{filename}' encoded and added to vault successfully.{colorama.Style.RESET_ALL}")
        except Exception as e:
            print(f"{colorama.Fore.RED}Error: Failed to encode file - {e}{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.YELLOW}Your changes may not be saved. Try 'close' to save manually.{colorama.Style.RESET_ALL}")

    def cmd_decode(self, args: List[str]) -> None:
        """Decode (decrypt) a file from the vault and save it to the file system."""
        if not self._require_vault_open():
            return
        if len(args) < 1:
            print(f"{colorama.Fore.RED}Error: Vault filename required. Usage: decode <vault_filename> [output_path]{colorama.Style.RESET_ALL}")
            return
        
        vault_filename = args[0]
        
        # If no output path specified, use current working directory with the same filename
        if len(args) < 2:
            output_path = os.path.join(os.getcwd(), vault_filename)
            print(f"{colorama.Fore.CYAN}No output path specified, using: {output_path}{colorama.Style.RESET_ALL}")
        else:
            output_path = args[1]
        
        # Find the file entry in current location
        file_entry = None
        for entry in self.names:
            if entry['name'] == vault_filename and entry['location'] == self.current_dir:
                file_entry = entry
                break
        
        # Check if file exists in vault at current location
        if file_entry is None:
            print(f"{colorama.Fore.RED}Error: File '{vault_filename}' does not exist in the current directory.{colorama.Style.RESET_ALL}")
            return
        
        # Check if it's a folder
        if file_entry['is_folder']:
            print(f"{colorama.Fore.RED}Error: '{vault_filename}' is a folder. Only files can be decoded.{colorama.Style.RESET_ALL}")
            return
        
        # Check if output path already exists
        if os_path.exists(output_path):
            print(f"{colorama.Fore.YELLOW}Warning: File '{output_path}' already exists.{colorama.Style.RESET_ALL}")
            response = input("Overwrite? (y/n): ").lower()
            if response != 'y':
                print(f"{colorama.Fore.CYAN}Decode cancelled.{colorama.Style.RESET_ALL}")
                return
        
        try:
            # Decode the file
            decode.decode_file(output_path, self.password, self.names, file_entry['file_id'])
            print(f"{colorama.Fore.GREEN}File '{vault_filename}' decoded and saved to '{output_path}' successfully.{colorama.Style.RESET_ALL}")
        except Exception as e:
            print(f"{colorama.Fore.RED}Error: Failed to decode file - {e}{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.YELLOW}The file may be corrupted or the password may have changed.{colorama.Style.RESET_ALL}")


    ###################
    #### Help menu ####
    ###################

    def cmd_help(self, args: List[str]) -> None:
        """Display help information."""
        help_menu.cmd_help(args)




if __name__ == "__main__":
    app = SecuRT_App()
    app.run()



