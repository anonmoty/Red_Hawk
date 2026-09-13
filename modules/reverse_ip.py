import requests
import socket
from core.colors import Colors as C

class ReverseIP:
    name = "Reverse IP Lookup"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🔄 REVERSE IP LOOKUP{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        results = []
        try:
            ip = socket.gethostbyname(self.domain)
            print(f"  {C.info(f'IP: {ip}')}")

            resp = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=15)
            if resp.status_code == 200 and "error" not in resp.text.lower():
                domains = [d.strip() for d in resp.text.strip().split('\n') if d.strip()]
                results = domains
                print(f"  {C.found(f'Domains on same IP: {len(domains)}')}\n")
                for d in domains[:30]:
                    print(f"    {C.DIM}→ {d}{C.RESET}")
                if len(domains) > 30:
                    remaining = len(domains) - 30
                    print(f"    {C.DIM}  ... and {remaining} more{C.RESET}")
            else:
                print(f"  {C.warning('No results or API limit reached')}")
        except Exception as e:
            print(f"  {C.error(f'Reverse IP failed: {e}')}")
        return results
