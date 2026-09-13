import dns.resolver
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.colors import Colors as C
from core.config import Config

class SubdomainScan:
    name = "Subdomain Enumeration"

    def __init__(self, domain):
        self.domain = domain
        self.found = []
        self.wordlist_path = os.path.join(Config.WORDLIST_DIR, "subdomains.txt")

    def _check_dns(self, sub):
        target = f"{sub}.{self.domain}"
        try:
            dns.resolver.resolve(target, 'A')
            return target
        except:
            return None

    def _bruteforce(self):
        print(f"\n  {C.info('Method 1: DNS Brute Force (Threaded)')}")
        wordlist = []
        if os.path.exists(self.wordlist_path):
            with open(self.wordlist_path) as f:
                wordlist = [l.strip() for l in f if l.strip()]
        else:
            wordlist = ['www','mail','ftp','admin','blog','dev','api','test',
                       'staging','shop','app','cdn','portal','docs','status',
                       'login','webmail','smtp','pop','imap','ns1','ns2','mx',
                       'vpn','proxy','git','jenkins','ci','db','cloud','server',
                       'panel','dashboard','forum','wiki','support','media',
                       'static','assets','images','mobile','m','beta','alpha',
                       'demo','sandbox','uat','prod','monitoring','grafana',
                       'elastic','kibana','redis','kafka','rabbitmq','docker']

        print(f"  {C.info(f'Wordlist: {len(wordlist)} entries')}")
        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as executor:
            futures = {executor.submit(self._check_dns, sub): sub for sub in wordlist}
            done = 0
            for future in as_completed(futures):
                done += 1
                C.progress(done, len(wordlist), "Brute forcing...")
                result = future.result()
                if result and result not in self.found:
                    self.found.append(result)
                    print(f"\n    {C.found(result)}")

    def _crtsh(self):
        print(f"\n  {C.info('Method 2: Certificate Transparency (crt.sh)')}")
        try:
            resp = requests.get(f"https://crt.sh/?q=%25.{self.domain}&output=json", timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                for entry in data:
                    names = entry.get('name_value', '').split('\n')
                    for name in names:
                        name = name.strip().lower()
                        if name.endswith(self.domain) and '*' not in name and name not in self.found:
                            self.found.append(name)
                            print(f"    {C.found(name)}")
        except Exception as e:
            print(f"  {C.error(f'crt.sh failed: {e}')}")

    def _hackertarget(self):
        print(f"\n  {C.info('Method 3: HackerTarget API')}")
        try:
            resp = requests.get(f"https://api.hackertarget.com/hostsearch/?q={self.domain}", timeout=15)
            if resp.status_code == 200 and "error" not in resp.text.lower():
                for line in resp.text.strip().split('\n'):
                    host = line.split(',')[0].strip()
                    if host and host not in self.found:
                        self.found.append(host)
                        print(f"    {C.found(host)}")
        except Exception as e:
            print(f"  {C.error(f'HackerTarget failed: {e}')}")

    def _rapiddns(self):
        print(f"\n  {C.info('Method 4: RapidDNS')}")
        try:
            from bs4 import BeautifulSoup
            resp = requests.get(f"https://rapiddns.io/subdomain/{self.domain}", timeout=15, headers=Config.HEADERS)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'lxml')
                table = soup.find('table')
                if table:
                    for row in table.find_all('tr')[1:]:
                        cells = row.find_all('td')
                        if cells:
                            sub = cells[0].text.strip().lower()
                            if sub.endswith(self.domain) and sub not in self.found:
                                self.found.append(sub)
                                print(f"    {C.found(sub)}")
        except Exception as e:
            print(f"  {C.error(f'RapidDNS failed: {e}')}")

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🔍 SUBDOMAIN ENUMERATION{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")

        self._bruteforce()
        self._crtsh()
        self._hackertarget()
        self._rapiddns()

        # Remove duplicates
        self.found = list(set(self.found))
        self.found.sort()

        print(f"\n  {C.BOLD}{C.GREEN}[✓] Total Unique Subdomains: {len(self.found)}{C.RESET}")
        return self.found
