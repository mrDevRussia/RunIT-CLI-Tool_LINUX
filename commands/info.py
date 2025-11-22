from pathlib import Path
from utils.file_utils import FileUtils


class FileInfo:
    def __init__(self):
        self.file_utils = FileUtils()

    def show_file_info(self, filename: str):
        p = Path(filename).resolve()
        if not p.exists() or not p.is_file():
            print(f"❌ File not found: {filename}")
            return
        stat = p.stat()
        print(f"\n📊 File Information: {p.name}")
        print("=" * 60)
        print(f"   Full Path: {str(p)}")
        print(f"   Size: {self.file_utils.get_file_size(p)} ({stat.st_size} bytes)")
        print(f"   Extension: {p.suffix or 'None'}")
        print(f"   Created: {stat.st_ctime:.0f}")
        print(f"   Modified: {stat.st_mtime:.0f}")