#!/usr/bin/env python3
import sys
import os
import shlex
import json
from pathlib import Path

# Ensure RunIT-Linux is on the import path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from commands import (
    FileCreator,
    VirusScanner,
    FileSearcher,
    FileInfo,
    HelpDisplay,
    AIAssistant,
    PackageManager,
    FileManager,
    Converter,
    P2PMessenger,
)
from utils.logger import Logger

# Linux-specific adapters
from linux_runner import LinuxFileRunner
from linux_deployer import LinuxDeployer
from sysinfo import SystemInfo


class RunITLinuxCLI:
    def __init__(self):
        self.logger = Logger()
        # Use Linux-specific runner and deployer
        self.runner = LinuxFileRunner()
        self.creator = FileCreator()
        self.scanner = VirusScanner()
        self.searcher = FileSearcher()
        self.info = FileInfo()
        self.helper = HelpDisplay()
        self.ai_assistant = AIAssistant()
        self.package_manager = PackageManager()
        self.file_manager = FileManager()
        self.deployer = LinuxDeployer()
        self.converter = Converter()
        self.p2pmsg = P2PMessenger()
        self.sysinfo = SystemInfo()
        self.running = True

        self.commands = {
            'run': self.cmd_run,
            'create': self.cmd_create,
            'search': self.cmd_search,
            'scan': self.cmd_scan,
            'info': self.cmd_info,
            'help': self.cmd_help,
            'runai': self.cmd_runai,
            'clear': self.cmd_clear,
            'exit': self.cmd_exit,
            'quit': self.cmd_exit,
            'install': self.cmd_install,
            'update': self.cmd_update,
            'show': self.cmd_show,
            'edit': self.cmd_edit,
            'go': self.cmd_go,
            'version': self.cmd_version,
            'test': self.cmd_test,
            'preview': self.cmd_preview,
            'deploy': self.cmd_deploy,
            'stopdeploy': self.cmd_stopdeploy,
            'share': self.cmd_share,
            'setport': lambda args: self.deployer.set_port(int(args[0])) if args and args[0].isdigit() else print("❌ Please provide a valid port number (e.g. 'setport 8080')"),
            'convert': self.cmd_convert,
            'restart': self.cmd_restart,
            'uninstall': self.cmd_uninstall,
            'adm': self.cmd_adm,
            'kill': self.cmd_kill,
            'p2pmsg': self.cmd_p2pmsg,
            'cid': self.cmd_cid,
            'systeminfo': self.cmd_systeminfo,
        }

        self._load_package_commands()

    def _load_package_commands(self):
        installed_packages = self.package_manager.get_installed_packages()
        for package_name, package_info in installed_packages.items():
            if package_info.get('installed') and package_info.get('install_path'):
                try:
                    package_path = os.path.abspath(package_info['install_path'])
                    if package_path not in sys.path:
                        sys.path.insert(0, package_path)
                    module_name = package_info['main_file'].replace('.py', '')
                    if module_name in sys.modules:
                        del sys.modules[module_name]
                    try:
                        package_module = __import__(module_name)
                    except ImportError:
                        continue
                    if hasattr(package_module, 'handle_command'):
                        pkg_info_path = os.path.join(package_path, 'package_info.json')
                        if os.path.exists(pkg_info_path):
                            with open(pkg_info_path) as f:
                                pkg_info = json.load(f)
                            for cmd_name in pkg_info.get('commands', {}).keys():
                                def create_handler(cmd, mod):
                                    def handler(args):
                                        try:
                                            return mod.handle_command(cmd, args)
                                        except Exception:
                                            return False
                                    return handler
                                self.commands[cmd_name] = create_handler(cmd_name, package_module)
                except Exception:
                    continue

    def display_banner(self):
        banner = (
            "\n"
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║                         RunIT v1.3.2                         ║\n"
            "║                   Smart Terminal Assistant                   ║\n"
            "║                         Linux Edition                        ║\n"
            "╠══════════════════════════════════════════════════════════════╣\n"
            "║  Type 'help' for commands | Type 'version' for packages      ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n"
        )
        print(banner)
        self.logger.info("RunIT Linux CLI started")

    def parse_command(self, input_line):
        try:
            parts = shlex.split(input_line.strip())
            if not parts:
                return None, []
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            return command, args
        except ValueError:
            return None, []

    def cmd_run(self, args):
        if not args:
            print("❌ Error: Please specify a filename to run")
            print("Usage: run <filename>")
            return
        self.runner.run_file(args[0])

    def cmd_create(self, args):
        if len(args) < 2:
            print("❌ Error: Please specify language and filename")
            print("Usage: create <language> <filename>")
            return
        self.creator.create_file(args[0].lower(), args[1])

    def cmd_search(self, args):
        if len(args) < 2:
            print("❌ Error: Please specify keyword and filename")
            print("Usage: search <keyword> <filename>")
            return
        self.searcher.search_in_file(args[0], args[1])

    def cmd_scan(self, args):
        if not args:
            print("❌ Error: Please specify a filename to scan")
            print("Usage: scan <filename>")
            return
        self.scanner.scan_file(args[0])

    def cmd_info(self, args):
        if not args:
            print("❌ Error: Please specify a filename")
            print("Usage: info <filename>")
            return
        self.info.show_file_info(args[0])

    def cmd_help(self, args):
        if args and args[0] in self.commands:
            if args[0] == 'runai':
                self.ai_assistant.show_ai_help()
            else:
                self.helper.show_command_help(args[0])
        else:
            self.helper.show_general_help()

    def cmd_runai(self, args):
        if not args:
            print("❌ Error: Please provide a question or topic")
            print("Usage: runai <question>")
            return
        query = ' '.join(args)
        if query.startswith('file:'):
            filename = query[5:].strip()
            self.ai_assistant.help_with_file(filename)
        else:
            response = self.ai_assistant.get_code_assistance(query)
            self.ai_assistant.format_ai_response(response)

    def cmd_deploy(self, args):
        if not args:
            print("❌ Error: Please specify a folder to deploy")
            print("Usage: deploy <folder>")
            return
        folder_path = args[0]
        if not os.path.isdir(folder_path):
            print(f"❌ Error: '{folder_path}' is not a valid directory")
            return
        self.deployer.deploy_site(folder_path)

    def cmd_stopdeploy(self, args):
        self.deployer.stop_deployment()

    def cmd_share(self, args):
        try:
            if hasattr(self.deployer, 'generate_public_url'):
                return self.deployer.generate_public_url()
            return self.deployer.share()
        except Exception as e:
            print(f"❌ Share failed: {e}")

    def cmd_clear(self, args):
        os.system('clear')
        self.display_banner()

    def cmd_exit(self, args):
        print("👋 Thanks for using RunIT (Linux)! Goodbye!")
        self.logger.info("RunIT Linux CLI session ended")
        self.running = False

    def cmd_install(self, args):
        if not args:
            print("❌ Please specify a package to install")
            print("Usage: install <package_name>")
            return
        package_name = args[0]
        if self.package_manager.install_package(package_name):
            print(f"✅ Successfully installed {package_name}")
        else:
            print(f"❌ Failed to install {package_name}. Check logs for details.")

    def cmd_update(self, args):
        if not args:
            print("❌ Error: Please specify what to update")
            print("Usage: update <package_name@latest> or update RunIT@latest")
            return
        self.package_manager.update_package(args[0])

    def cmd_show(self, args):
        if not args:
            print("❌ Error: Please specify a file or directory to show")
            print("Usage: show <filename_or_directory>")
            return
        self.file_manager.show_file_structure(args[0])

    def cmd_edit(self, args):
        if not args:
            print("❌ Error: Please specify a file to edit")
            print("Usage: edit <filename> [editor]")
            return
        filepath = args[0]
        editor = args[1] if len(args) > 1 else None
        self.file_manager.edit_file(filepath, editor)

    def cmd_go(self, args):
        if not args:
            print("❌ Error: Please specify a directory path")
            print("Usage: go <directory_path>")
            return
        self.file_manager.go_to_directory(args[0])

    def cmd_version(self, args):
        version = self.package_manager.get_version()
        print(f"🚀 RunIT CLI Tool Version {version} (Linux Edition)")
        print("Smart Terminal Assistant for Linux")
        print("\n📦 Package Status:")
        self.package_manager.list_packages()

    def cmd_convert(self, args):
        if len(args) != 2:
            print("❌ Usage: convert <source_file> <target_language>")
            print("Supported conversions:")
            for conversion, details in self.converter.get_supported_conversions().items():
                source, target = details
                print(f"  • {source} → {target}")
            return
        source_file = args[0]
        target_language = args[1].lower()
        if not os.path.exists(source_file):
            print(f"❌ Source file '{source_file}' not found")
            return
        converted_code = self.converter.convert_code(source_file, target_language)
        if converted_code:
            ext_map = {'python': 'py', 'javascript': 'js', 'markdown': 'md'}
            target_ext = ext_map.get(target_language, target_language)
            output_file = f"{os.path.splitext(source_file)[0]}.{target_ext}"
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(converted_code)
                print(f"✅ Code converted successfully! Output saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error saving converted code: {str(e)}")
        else:
            print("❌ Code conversion failed. Please check the supported conversions and try again.")

    def cmd_test(self, args):
        print("🧪 Testing RunIT (Linux) functionality...")
        print("="*40)
        print("✅ Core CLI system: OK")
        try:
            current_dir = self.file_manager.get_current_directory()
            print(f"✅ File system access: OK (Current: {current_dir})")
        except Exception as e:
            print(f"❌ File system access: FAILED ({e})")
        print("🎉 RunIT test completed!")

    def cmd_preview(self, args):
        if not args:
            print("❌ Error: Please specify an HTML file to preview")
            print("Usage: preview <filename.html>")
            return
        try:
            sys.path.insert(0, str(Path("packages/preview_RunIT")))
            import importlib.util
            spec = importlib.util.spec_from_file_location("preview", Path("packages/preview_RunIT/preview.py"))
            if spec and spec.loader:
                preview_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(preview_module)
                preview_module.main(args)
            else:
                raise ImportError("Preview module not found")
        except Exception as e:
            print("❌ Preview package not installed or not working")
            print("   Install it with: install preview_RunIT@latest")
            self.logger.error(f"Preview command failed: {e}")

    def cmd_restart(self, args):
        self.logger.info("Restarting RunIT (Linux)...")
        print("🔄 Restarting RunIT...")
        try:
            executable = sys.executable
            script = os.path.abspath(__file__)
            import subprocess
            subprocess.Popen([executable, script] + sys.argv[1:])
            sys.exit(0)
        except Exception as e:
            self.logger.error(f"Failed to restart: {str(e)}")
            print(f"❌ Failed to restart: {str(e)}")
            self.running = True
            return False
        return True

    def cmd_uninstall(self, args):
        self.logger.info("Uninstalling RunIT (Linux)...")
        print("⚠️ Are you sure you want to uninstall RunIT (Linux)?")
        print("   Type 'yes' to confirm or anything else to cancel:")
        confirmation = input("> ").strip().lower()
        if confirmation != "yes":
            print("✅ Uninstallation cancelled.")
            return False
        install_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            uninstall_script = os.path.join(install_dir, 'uninstall.sh')
            with open(uninstall_script, 'w') as f:
                f.write("#!/usr/bin/env bash\n")
                f.write("sleep 1\n")
                f.write(f"rm -rf \"{install_dir}\"\n")
            os.chmod(uninstall_script, 0o755)
            import subprocess
            subprocess.Popen(['bash', uninstall_script])
            self.running = False
            return True
        except Exception as e:
            self.logger.error(f"Failed to uninstall: {str(e)}")
            print(f"❌ Failed to uninstall: {str(e)}")
            return False

    def cmd_p2pmsg(self, args):
        try:
            self.p2pmsg.start(args)
        except Exception as e:
            self.logger.error(f"p2pmsg error: {e}")
            print(f"❌ p2pmsg error: {e}")

    def cmd_adm(self, args):
        if not self.package_manager.is_package_installed("IDER_RunIT"):
            print("❌ Advanced Developer Mode requires the IDER package.")
            print("   Run: install IDER")
            return False
        return False

    def cmd_kill(self, args):
        if not self.package_manager.is_package_installed("kill_RunIT"):
            print("❌ Process termination requires the kill package.")
            print("   Run: install kill")
            return False
        return False

    def cmd_cid(self, args):
        from commands.security import generate_device_client_id, CLIENT_ID_PATH
        try:
            if CLIENT_ID_PATH.exists():
                with open(CLIENT_ID_PATH, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                    cid = obj.get('client_id')
                    if cid:
                        print(f"🆔 Client ID: {cid}")
                        return
            print("This will generate a persistent Client ID based on your device and network info.")
            agree = input("Do you agree? (yes/no): ").strip().lower()
            if agree not in ['y', 'yes']:
                print("❌ Generation cancelled.")
                return
            cid = generate_device_client_id()
            print(f"✅ Client ID generated: {cid}")
        except Exception as e:
            self.logger.error(f"cid error: {e}")
            print(f"❌ cid error: {e}")

    def cmd_systeminfo(self, args):
        self.sysinfo.show()

    def run_command(self, command, args):
        if command in self.commands:
            try:
                self.commands[command](args)
            except Exception as e:
                self.logger.error(f"Error executing command '{command}': {e}")
                print(f"❌ An error occurred while executing '{command}': {e}")
        else:
            print(f"❌ Unknown command: '{command}'")
            print("Type 'help' to see available commands")

    def run(self):
        self.display_banner()
        while self.running:
            try:
                user_input = input("RunIT-Linux> ").strip()
                if not user_input:
                    continue
                command, args = self.parse_command(user_input)
                if command:
                    self.run_command(command, args)
            except KeyboardInterrupt:
                print("\n👋 Interrupted by user. Goodbye!")
                self.logger.info("RunIT Linux CLI interrupted by user")
                break
            except EOFError:
                print("\n👋 Session ended. Goodbye!")
                self.logger.info("RunIT Linux CLI session ended via EOF")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {e}")
                print(f"❌ An unexpected error occurred: {e}")


def main():
    cli = RunITLinuxCLI()
    cli.run()


if __name__ == "__main__":
    main()