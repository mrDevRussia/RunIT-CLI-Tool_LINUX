from pathlib import Path


class FileUtils:
    def get_file_size(self, file_path: Path) -> str:
        size = float(file_path.stat().st_size)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"