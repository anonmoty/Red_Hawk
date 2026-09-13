import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from core.colors import Colors as C
from core.config import Config

class LinkCrawler:
    name = "Link Extractor / Crawler"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🕷️ LINK CRAWLER{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        results = {"internal": [], "external": [], "resources": []}
        try:
            resp = requests.get(f"https://{self.domain}", timeout=Config.TIMEOUT, headers=Config.HEADERS)
            soup = BeautifulSoup(resp.text, 'html.parser')

            for tag in soup.find_all('a', href=True):
                href = urljoin(f"https://{self.domain}", tag['href'])
                parsed = urlparse(href)
                if self.domain in parsed.netloc:
                    if href not in results["internal"]:
                        results["internal"].append(href)
                elif parsed.scheme in ['http', 'https']:
                    if href not in results["external"]:
                        results["external"].append(href)

            for tag in soup.find_all(['script', 'link', 'img']):
                src = tag.get('src') or tag.get('href', '')
                if src:
                    full_url = urljoin(f"https://{self.domain}", src)
                    if full_url not in results["resources"]:
                        results["resources"].append(full_url)

            forms = soup.find_all('form')

            print(f"\n  {C.CYAN}Internal Links ({len(results['internal'])}):{C.RESET}")
            for link in results["internal"][:15]:
                print(f"    {C.DIM}→ {link}{C.RESET}")

            print(f"\n  {C.CYAN}External Links ({len(results['external'])}):{C.RESET}")
            for link in results["external"][:10]:
                print(f"    {C.DIM}→ {link}{C.RESET}")

            print(f"\n  {C.CYAN}Resources ({len(results['resources'])}):{C.RESET}")
            for res in results["resources"][:10]:
                print(f"    {C.DIM}→ {res}{C.RESET}")

            print(f"\n  {C.info(f'Forms found: {len(forms)}')}")
            total_links = len(results['internal']) + len(results['external'])
            print(f"  {C.BOLD}{C.GREEN}[✓] Total links: {total_links}{C.RESET}")

        except Exception as e:
            print(f"  {C.error(f'Crawl failed: {e}')}")
        return results
