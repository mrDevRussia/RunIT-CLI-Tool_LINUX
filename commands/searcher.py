from pathlib import Path


class FileSearcher:
    def search_in_file(self, keyword: str, filename: str):
        p = Path(filename)
        if not p.exists():
            print(f"❌ File not found: {filename}")
            return
        count = 0
        with p.open('r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                if keyword in line:
                    count += 1
                    print(f"{i:5}: {line.rstrip()}")
        print(f"\n🔎 Matches: {count}")