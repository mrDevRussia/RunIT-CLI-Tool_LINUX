import platform
import os
import socket
import subprocess

try:
    import psutil
except Exception:
    psutil = None


class SystemInfo:
    def _read_os_release(self):
        data = {}
        try:
            with open('/etc/os-release') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        k, v = line.split('=', 1)
                        data[k] = v.strip('"')
        except Exception:
            pass
        return data

    def _default_gateway(self):
        try:
            out = subprocess.check_output(['ip', 'route'], text=True)
            for line in out.splitlines():
                if line.startswith('default via'):
                    parts = line.split()
                    return parts[2]
        except Exception:
            return ''

    def show(self):
        osr = self._read_os_release()
        dist = osr.get('PRETTY_NAME') or osr.get('NAME') or 'Unknown Linux'
        print("\n🖥️  System Information")
        print("=" * 40)
        print(f"OS: {dist}")
        print(f"Kernel: {platform.release()}")
        print(f"Python: {platform.python_version()}")
        print(f"Hostname: {socket.gethostname()}")
        cpu = platform.processor() or platform.machine()
        print(f"CPU: {cpu}")
        if psutil:
            print(f"CPU Cores: {psutil.cpu_count(logical=True)}")
            vm = psutil.virtual_memory()
            print(f"Memory: {round(vm.total/1024/1024/1024, 2)} GB")
            ni = psutil.net_if_addrs()
            print("Interfaces:")
            shown = 0
            for name, addrs in ni.items():
                ips = [a.address for a in addrs if a.family == socket.AF_INET]
                if ips:
                    print(f"  {name}: {', '.join(ips)}")
                    shown += 1
            if not shown:
                print("  No IPv4 interfaces detected")
        gw = self._default_gateway()
        if gw:
            print(f"Default Gateway: {gw}")