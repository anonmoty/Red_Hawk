import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.colors import Colors as C
from core.config import Config

class PortScan:
    name = "Port Scanner"

    def __init__(self, domain):
        self.domain = domain
        self.common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
            143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
            1433: "MSSQL", 1521: "Oracle", 2049: "NFS", 3306: "MySQL",
            3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
            8080: "HTTP-Proxy", 8443: "HTTPS-Alt", 8888: "Alt-HTTP",
            9090: "WebUI", 9200: "Elasticsearch", 27017: "MongoDB"
        }

    def _scan_port(self, port):
        try:
            ip = socket.gethostbyname(self.domain)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                # Banner grab
                banner = ""
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    s.connect((ip, port))
                    s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = s.recv(1024).decode('utf-8', errors='ignore').strip()[:100]
                    s.close()
                except:
                    pass
                return (port, True, banner)
        except:
            pass
        return (port, False, "")

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🔌 PORT SCANNER (Threaded){C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")

        try:
            ip = socket.gethostbyname(self.domain)
            print(f"  {C.info(f'Target IP: {ip}')}")
        except:
            print(f"  {C.error('Cannot resolve domain')}")
            return {}

        ports = list(self.common_ports.keys())
        results = {"open_ports": [], "ip": ip}
        print(f"  {C.info(f'Scanning {len(ports)} common ports...')}\n")

        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as executor:
            futures = {executor.submit(self._scan_port, p): p for p in ports}
            done = 0
            for future in as_completed(futures):
                done += 1
                C.progress(done, len(ports), "Scanning ports...")
                port, is_open, banner = future.result()
                if is_open:
                    service = self.common_ports.get(port, "Unknown")
                    entry = {"port": port, "service": service, "banner": banner}
                    results["open_ports"].append(entry)
                    print(f"\n    {C.GREEN}[OPEN]{C.RESET} {port:5d}/{service:15s} {C.DIM}{banner[:60]}{C.RESET}")

        print(f"\n  {C.BOLD}{C.GREEN}[✓] Open Ports Found: {len(results['open_ports'])}{C.RESET}")
        return results
