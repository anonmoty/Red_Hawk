import requests
import re
from bs4 import BeautifulSoup
from core.colors import Colors as C
from core.config import Config

class EmailHarvest:
    name = "Email Harvester"

    def __init__(self, domain):
        self.domain = domain
        self.emails = set()

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}📧 EMAIL HARVESTER{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")

        # Method 1: Website scrape
        print(f"  {C.info('Method 1: Website Scraping')}")
        for scheme in ['https', 'http']:
            try:
                resp = requests.get(f"{scheme}://{self.domain}", timeout=Config.TIMEOUT, headers=Config.HEADERS)
                found = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resp.text)
                for email in found:
                    self.emails.add(email.lower())
                break
            except:
                continue

        # Method 2: Common pages
        print(f"  {C.info('Method 2: Common Pages')}")
        pages = ['/contact', '/about', '/impressum', '/team', '/privacy', '/support']
        for page in pages:
            try:
                resp = requests.get(f"https://{self.domain}{page}", timeout=5, headers=Config.HEADERS)
                found = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resp.text)
                for email in found:
                    self.emails.add(email.lower())
            except:
                pass

        # Method 3: Google dork simulation via search
        print(f"  {C.info('Method 3: Pattern Guessing')}")
        common = ['info', 'admin', 'contact', 'support', 'hello',
                  'sales', 'hr', 'career', 'press', 'office']
        for prefix in common:
            self.emails.add(f"{prefix}@{self.domain}")

        emails_list = sorted(list(self.emails))
        print(f"\n  {C.CYAN}Found/Generated Emails:{C.RESET}")
        for email in emails_list:
            print(f"    {C.found(email)}")

        print(f"\n  {C.BOLD}{C.GREEN}[✓] Total: {len(emails_list)}{C.RESET}")
        return emails_list
