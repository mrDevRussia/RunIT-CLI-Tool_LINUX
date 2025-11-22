import os
from pathlib import Path


class FileManager:
    def show_file_structure(self, filepath: str, max_depth: int = 2) -> bool:
        p = Path(filepath).resolve()
        if not p.exists():
            print(f"❌ Path not found: {filepath}")
            return False
        if p.is_file():
            print(p.name)
        else:
            for root, dirs, files in os.walk(p):
                depth = Path(root).relative_to(p).parts
                if len(depth) > max_depth:
                    continue
                print(root)
                for f in files:
                    print(f"  {f}")
        return True

    def edit_file(self, filepath: str, editor: str | None = None) -> bool:
        p = Path(filepath)
        if not p.exists():
            p.touch()
        cmd = editor or os.environ.get('EDITOR') or 'nano'
        os.system(f"{cmd} '{p}'")
        return True

    def go_to_directory(self, directory_path: str) -> bool:
        p = Path(directory_path).resolve()
        if not p.exists() or not p.is_dir():
            print(f"❌ Not a directory: {directory_path}")
            return False
        os.chdir(p)
        print(f"📁 Changed to directory: {p}")
        return True

    def get_current_directory(self) -> str:
        return str(Path.cwd())