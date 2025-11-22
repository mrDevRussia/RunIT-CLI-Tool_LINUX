from pathlib import Path
import subprocess


class LinuxFileRunner:
    def __init__(self):
        pass

    def get_interpreter_command(self, file_path: Path):
        extension = file_path.suffix.lower()
        interpreter_map = {
            '.py': ['python3'],
            '.js': ['node'],
            '.html': ['xdg-open'],
            '.css': ['xdg-open'],
            '.php': ['php'],
            '.sh': ['bash'],
            '.c': None,
            '.cpp': None,
            '.java': None,
            '.ts': ['ts-node'],
            '.json': ['xdg-open'],
            '.xml': ['xdg-open'],
            '.txt': ['xdg-open'],
            '.md': ['xdg-open'],
            '.bat': ['bash'],
            '.cmd': ['bash'],
        }
        if extension in interpreter_map:
            command = interpreter_map[extension]
            if command is None:
                return None
            return command + [str(file_path)]
        return None

    def check_interpreter_availability(self, interpreter: str) -> bool:
        try:
            result = subprocess.run([interpreter, '--version'], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except Exception:
            try:
                result = subprocess.run([interpreter, '-v'], capture_output=True, text=True, timeout=5)
                return result.returncode == 0
            except Exception:
                return False

    def handle_compilation_required(self, file_path: Path):
        extension = file_path.suffix.lower()
        info = None
        if extension == '.c':
            info = {'compiler': 'gcc', 'command': f'gcc "{file_path}" -o "{file_path.stem}"', 'run_command': f'./{file_path.stem}'}
        elif extension == '.cpp':
            info = {'compiler': 'g++', 'command': f'g++ "{file_path}" -o "{file_path.stem}"', 'run_command': f'./{file_path.stem}'}
        elif extension == '.java':
            info = {'compiler': 'javac', 'command': f'javac "{file_path}"', 'run_command': f'java "{file_path.stem}"'}
        if not info:
            print("❌ Unsupported compilation type")
            return
        print(f"⚠️  File '{file_path.name}' requires compilation first.")
        print(f"Compiler needed: {info['compiler']}")
        print(f"Compile with: {info['command']}")
        print(f"Then run with: {info['run_command']}")
        if self.check_interpreter_availability(info['compiler']):
            resp = input("Would you like to compile and run now? (y/n): ").lower()
            if resp in ['y', 'yes']:
                try:
                    print(f"🔨 Compiling {file_path.name}...")
                    compile_result = subprocess.run(info['command'], shell=True, capture_output=True, text=True, cwd=file_path.parent)
                    if compile_result.returncode == 0:
                        print("✅ Compilation successful!")
                        run_result = subprocess.run(info['run_command'], shell=True, cwd=file_path.parent)
                        if run_result.returncode == 0:
                            print("✅ Program executed successfully!")
                        else:
                            print(f"❌ Program execution failed with code {run_result.returncode}")
                    else:
                        print("❌ Compilation failed!")
                        if compile_result.stderr:
                            print(compile_result.stderr)
                except Exception as e:
                    print(f"❌ Compilation error: {e}")

    def run_file(self, filename: str):
        try:
            file_path = Path(filename).resolve()
            if not file_path.exists() or not file_path.is_file():
                print(f"❌ File not found: {filename}")
                return
            command = self.get_interpreter_command(file_path)
            if command is None:
                self.handle_compilation_required(file_path)
                return
            interpreter = command[0]
            if not self.check_interpreter_availability(interpreter) and interpreter != 'xdg-open':
                print(f"❌ Interpreter '{interpreter}' not found on system.")
                return
            print(f"🚀 Running {file_path.name}...")
            print("-" * 50)
            result = subprocess.run(
                command,
                cwd=file_path.parent,
                shell=False
            )
            print("-" * 50)
            if result.returncode == 0:
                print(f"✅ {file_path.name} executed successfully!")
            else:
                print(f"❌ {file_path.name} execution failed with code {result.returncode}")
        except KeyboardInterrupt:
            print("\n⚠️  Execution interrupted by user")
        except Exception as e:
            print(f"❌ Error running file: {e}")