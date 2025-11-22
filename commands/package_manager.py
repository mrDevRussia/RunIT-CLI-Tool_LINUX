from pathlib import Path


class PackageManager:
    def __init__(self):
        self.current_version = "1.3.2"
        self.registry = {"packages": {}}

    def get_version(self) -> str:
        return self.current_version

    def list_packages(self):
        print("\n📦 RunIT Package Registry")
        print("="*50)
        print("\n🔧 Core Tool:")
        print(f"   RunIT v{self.current_version}")
        print("\n📚 Installed Packages:")
        if not self.registry["packages"]:
            print("   None")
        else:
            for name, info in self.registry["packages"].items():
                status = "✅ Installed" if info.get("installed") else "⚪ Available"
                print(f"   {name} - {status}")

    def install_package(self, package_name: str) -> bool:
        print(f"⚠️ Package installation not configured in RunIT-Linux standalone.")
        return False

    def update_package(self, package_name: str) -> bool:
        print(f"⚠️ Package update not configured in RunIT-Linux standalone.")
        return False

    def get_installed_packages(self) -> dict:
        return {}

    def is_package_installed(self, package_name: str) -> bool:
        return False

    def test_installation(self) -> bool:
        print("🧪 Package system test is not available in this standalone build.")
        return True