from pathlib import Path


class VirusScanner:
    def scan_file(self, filename: str):
        p = Path(filename)
        if not p.exists():
            print(f"❌ File not found: {filename}")
            return
        content = p.read_text(encoding='utf-8', errors='ignore')
        suspicious = any(x in content for x in ['eval(', 'exec(', '__import__', 'os.system', 'subprocess.Popen'])
        if suspicious:
            print("🔴 Potentially suspicious patterns detected")
        else:
            print("✅ No suspicious patterns found")