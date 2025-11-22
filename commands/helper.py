class HelpDisplay:
    def show_general_help(self):
        print("RunIT-Linux: type 'help <command>' or 'version'.")

    def show_command_help(self, command: str):
        print(f"Help for '{command}' is not available in this build.")