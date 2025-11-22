import socket
import http.server
import socketserver
import os
import functools
import threading
import time


class LinuxDeployer:
    def __init__(self):
        self.PORT = 8000
        self.server = None

    def set_port(self, port: int):
        if isinstance(port, int) and 1024 <= port <= 65535:
            self.PORT = port
            print(f"✅ Port changed to {port}")
            return True
        print("❌ Invalid port number. Please use a number between 1024 and 65535")
        return False

    def stop_deployment(self):
        try:
            if self.server:
                try:
                    self.server.shutdown()
                    self.server.server_close()
                    self.server = None
                    print("✅ Local server stopped successfully")
                except Exception as e:
                    print(f"❌ Failed to stop local server: {e}")
            def is_port_free():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    sock.bind(("127.0.0.1", self.PORT))
                    sock.close()
                    return True
                except Exception:
                    return False
            if is_port_free():
                print(f"✅ Port {self.PORT} is now free")
            else:
                print(f"❌ Port {self.PORT} is still in use")
                return False
            return True
        except Exception as e:
            print(f"❌ Error stopping deployment: {str(e)}")
            return False

    def deploy_site(self, site_folder: str):
        if not os.path.exists(site_folder):
            print(f"❌ Folder not found: {site_folder}")
            return False

    def share(self):
        print("⚠️  The share feature is currently not available on RunIT-Linux.")
        print(f"ℹ️  Access your site locally at http://localhost:{self.PORT}")
        return False
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("127.0.0.1", self.PORT))
            sock.close()
        except socket.error:
            print(f"❌ Port {self.PORT} is already in use")
            print("Use 'setport <number>' to try a different port")
            return False
        original_dir = os.getcwd()
        try:
            abs_site_folder = os.path.abspath(site_folder)
            os.chdir(abs_site_folder)
            handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=abs_site_folder)
            self.server = socketserver.TCPServer(("localhost", self.PORT), handler)
            self.server.allow_reuse_address = True
            t = threading.Thread(target=self.server.serve_forever)
            t.daemon = True
            t.start()
            time.sleep(1)
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.connect(("localhost", self.PORT))
                test_socket.close()
                server_url = f"http://localhost:{self.PORT}"
                print(f"✨ Local server started at: {server_url}")
                print(f"📂 Serving files from: {abs_site_folder}")
                os.chdir(original_dir)
                return True
            except socket.error:
                print("❌ Failed to start server")
                self.stop_deployment()
                os.chdir(original_dir)
                return False
        except Exception as e:
            print(f"❌ Server error: {str(e)}")
            self.stop_deployment()
            os.chdir(original_dir)
            return False