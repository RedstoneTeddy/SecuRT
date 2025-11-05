import sys
from typing import List, Optional

from os import path as os_path
from os import chdir as os_chdir
directory = os_path.dirname(os_path.abspath(__file__))
os_chdir(directory) #Small Bugfix, that in some situations, the code_path isn't correct

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
import colorama
import shlex

import name_settings

class SecureRT_App:
    """Main interactive SecureRT_App class."""
    
    def __init__(self):
        self.running: bool = True
        self.config = {
        }

        self.completer = NestedCompleter.from_nested_dict({
            "exit": None,
            "help": {
                "help": None,
                "exit": None
            },
            "open": None,
            "close": None,
            "status": None
        })

        # Custom style for the prompt
        self.prompt_style = Style.from_dict({
            "prompt": "#00aaff bold"
        })

        # Create prompt session
        self.session = PromptSession(
            completer=self.completer,
            style=self.prompt_style,
            complete_while_typing=True
        )

        self.names: list[name_settings.NameSettings] = []
        self.password: str = ""



    def get_prompt_message(self) -> HTML:
        """Generate the prompt message with styling."""
        return HTML('<prompt>SecureRT&gt;</prompt> ')

        
    def run(self):
        """Main application loop."""
        print(f"{colorama.Fore.LIGHTRED_EX}##################")
        print(f"{colorama.Fore.LIGHTRED_EX}#### SecureRT ####")
        print(f"{colorama.Fore.LIGHTRED_EX}##################")
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

        # Command routing
        commands = {
            "exit": self.cmd_exit,
            "help": self.cmd_help,
            "open": self.cmd_open,
            "close": self.cmd_close,
            "status": self.cmd_status
        }

        if cmd in commands:
            try: 
                commands[cmd](args[1:])
                print("")
            except Exception as e:
                print(f"Error executing command '{cmd}': {e}")
        else:
            print(f"Unknown command: {cmd}. Type 'help' for a list of commands.")
    


    def cmd_exit(self, args: List[str]) -> None:
        """Handle the 'exit' command to terminate the application."""
        if self.password != "":
            self.cmd_close([])
        print("Exiting the application. Goodbye!")
        self.running = False

    def cmd_status(self, args: List[str]) -> None:
        """Display if the vault is open or closed."""
        print(f"{colorama.Fore.CYAN}Vault status:{colorama.Style.RESET_ALL}")
        if self.password:
            print(f"{colorama.Fore.GREEN}Vault is OPEN.{colorama.Style.RESET_ALL}")
        else:
            print(f"{colorama.Fore.RED}Vault is CLOSED.{colorama.Style.RESET_ALL}")

    def cmd_close(self, args: List[str]) -> None:
        """Close the vault by clearing the password."""
        if self.password != "":
            name_settings.Store_names(self.names, self.password)
        self.password = ""
        self.names = []
        print(f"{colorama.Fore.YELLOW}Vault has been closed.{colorama.Style.RESET_ALL}")

    def cmd_open(self, args: List[str]) -> None:
        """Open the vault by prompting for a password and loading names."""
        if self.password:
            print(f"{colorama.Fore.YELLOW}Vault is already open.{colorama.Style.RESET_ALL}")
            return
        if len(args) < 1:
            print(f"{colorama.Fore.RED}Please provide a password to open the vault.{colorama.Style.RESET_ALL}")
            return

        self.password = args[0]
        try:
            self.names = name_settings.Load_names(self.password)
            print(f"{colorama.Fore.GREEN}Vault opened successfully with {len(self.names)} entries.{colorama.Style.RESET_ALL}")
        except Exception as e:
            self.password = ""
            self.names = []
            print(f"{colorama.Fore.RED}Failed to open vault: {e}{colorama.Style.RESET_ALL}")


    def cmd_help(self, args: List[str]) -> None:
        """Display help information."""
        help_text = ""

        if args: # User wants help for a specific command
            cmd: str = args[0].lower()
            match cmd:
                case "exit":
                    help_text += f"{colorama.Fore.CYAN}exit{colorama.Fore.RESET} - Exit the application.\n"
                    help_text += "No further arguments."
                case "help":
                    help_text += f"{colorama.Fore.CYAN}help{colorama.Fore.RESET} - Show help information.\n"
                    help_text += "You can call help without any arguments to see all commands.\n"
                    help_text += "You can also get help on specific commands by typing 'help <command>'."
                case "open":
                    help_text += f"{colorama.Fore.CYAN}open <password>{colorama.Fore.RESET} - Open the vault with the specified password.\n"
                    help_text += "Example: open my_secure_password"
                case "close":
                    help_text += f"{colorama.Fore.CYAN}close{colorama.Fore.RESET} - Close the vault.\n"
                    help_text += "No further arguments."
                case "status":
                    help_text += f"{colorama.Fore.CYAN}status{colorama.Fore.RESET} - Show whether the vault is open or closed.\n"
                    help_text += "No further arguments."
                case _:
                    help_text += f"{colorama.Fore.RED}No help available for unknown command: {cmd}"
        
        else: # General help
            help_text += "Available commands:\n"
            help_text += f"{colorama.Fore.CYAN} help{colorama.Fore.RESET}    - Show this help message (Use 'help <command>' for more details)\n"
            help_text += f"{colorama.Fore.CYAN} exit{colorama.Fore.RESET}    - Exit the application\n"
            help_text += f"{colorama.Fore.CYAN} open {colorama.Fore.RESET}   - Open the vault with the specified password\n"
            help_text += f"{colorama.Fore.CYAN} close{colorama.Fore.RESET}   - Close the vault\n"
            help_text += f"{colorama.Fore.CYAN} status{colorama.Fore.RESET}  - Show whether the vault is open or closed"


        print(help_text)

    


if __name__ == "__main__":
    app = SecureRT_App()
    app.run()



