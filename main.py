import sys
from typing import List, Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
import colorama

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
            }
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



    def get_prompt_message(self) -> HTML:
        """Generate the prompt message with styling."""
        return HTML('<prompt>SecureRT&gt;</prompt> ')
    
    def process_command(self, command: str) -> None:
        """Process a single command input."""
        if not command.strip():
            return

        args: list[str] = command.strip().split()
        cmd: str = args[0].lower()

        # Command routing
        commands = {
            "exit": self.cmd_exit,
            "help": self.cmd_help
        }

        if cmd in commands:
            try: 
                commands[cmd](args[1:])
                print("")
            except Exception as e:
                print(f"Error executing command '{cmd}': {e}")
        else:
            print(f"Unknown command: {cmd}. Type 'help' for a list of commands.")
    

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


    def cmd_exit(self, args: List[str]) -> None:
        """Handle the 'exit' command to terminate the application."""
        print("Exiting the application. Goodbye!")
        self.running = False

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
                case _:
                    help_text += f"{colorama.Fore.RED}No help available for unknown command: {cmd}"
        
        else: # General help
            help_text += "Available commands:\n"
            help_text += f"{colorama.Fore.CYAN} help{colorama.Fore.RESET}    - Show this help message (Use 'help <command>' for more details)\n"
            help_text += f"{colorama.Fore.CYAN} exit{colorama.Fore.RESET}    - Exit the application"

        print(help_text)

    


if __name__ == "__main__":
    app = SecureRT_App()
    app.run()



