from pathlib import Path


class FileCreator:
    def create_file(self, language: str, filename: str):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.touch()
            print(f"✅ Created {path}")
        else:
            print(f"⚠️ {path} already exists")