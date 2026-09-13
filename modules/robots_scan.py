import requests
from core.colors import Colors as C
from core.config import Config

class RobotsScan:
    name = "Robots.txt & Sitemap Analysis"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🤖 ROBOTS.TXT & SITEMAP{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        results = {"robots": "", "sitemaps": [], "disallowed": [], "allowed": []}
        try:
            resp = requests.get(f"https://{self.domain}/robots.txt", timeout=Config.TIMEOUT, headers=Config.HEADERS)
            if resp.status_code == 200:
                results["robots"] = resp.text
                print(f"  {C.found('robots.txt found!')}\n")
                for line in resp.text.strip().split('\n'):
                    line = line.strip()
                    if line.lower().startswith('disallow:'):
                        path = line.split(':', 1)[1].strip()
                        if path:
                            results["disallowed"].append(path)
                            print(f"    {C.RED}[DISALLOW]{C.RESET} {path}")
                    elif line.lower().startswith('allow:'):
                        path = line.split(':', 1)[1].strip()
                        results["allowed"].append(path)
                        print(f"    {C.GREEN}[ALLOW]{C.RESET}    {path}")
                    elif line.lower().startswith('sitemap:'):
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            s_url = parts[1].strip()
                            results["sitemaps"].append(s_url)
                            print(f"    {C.CYAN}[SITEMAP]{C.RESET}  {s_url}")
                    elif line and not line.startswith('#'):
                        print(f"    {C.DIM}{line}{C.RESET}")

                count = len(results['disallowed'])
                print(f"\n  {C.info(f'Disallowed paths: {count}')}")
            else:
                print(f"  {C.warning(f'robots.txt not found (HTTP {resp.status_code})')}")
        except Exception as e:
            print(f"  {C.error(f'Failed: {e}')}")
        return results
