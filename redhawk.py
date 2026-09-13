#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║    RED HAWK v3.0 - OSINT Framework       ║
║    Educational & Authorized Use Only     ║
╚══════════════════════════════════════════╝
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.banner import show_banner
from core.colors import Colors as C
from core.reporter import Reporter

# Import all modules
from modules.whois_scan import WhoisScan
from modules.dns_scan import DNSScan
from modules.subdomain_scan import SubdomainScan
from modules.header_scan import HeaderScan
from modules.geoip_scan import GeoIPScan
from modules.tech_detect import TechDetect
from modules.port_scan import PortScan
from modules.ssl_scan import SSLScan
from modules.email_harvest import EmailHarvest
from modules.wayback_scan import WaybackScan
from modules.cms_detect import CMSDetect
from modules.firewall_detect import FirewallDetect
from modules.social_scan import SocialScan
from modules.link_crawler import LinkCrawler
from modules.robots_scan import RobotsScan
from modules.cors_scan import CORSScan
from modules.clickjack_scan import ClickjackScan
from modules.reverse_ip import ReverseIP

MODULES = {
    "1": ("WHOIS Lookup", WhoisScan),
    "2": ("DNS Records", DNSScan),
    "3": ("Subdomain Enumeration", SubdomainScan),
    "4": ("HTTP Headers & Security", HeaderScan),
    "5": ("IP Geolocation", GeoIPScan),
    "6": ("Technology Detection", TechDetect),
    "7": ("Port Scanner", PortScan),
    "8": ("SSL/TLS Certificate", SSLScan),
    "9": ("Email Harvester", EmailHarvest),
    "10": ("Wayback Machine", WaybackScan),
    "11": ("CMS Detection", CMSDetect),
    "12": ("WAF / Firewall Detection", FirewallDetect),
    "13": ("Social Media Finder", SocialScan),
    "14": ("Link Crawler", LinkCrawler),
    "15": ("Robots.txt & Sitemap", RobotsScan),
    "16": ("CORS Misconfiguration", CORSScan),
    "17": ("Clickjacking Test", ClickjackScan),
    "18": ("Reverse IP Lookup", ReverseIP),
}

def print_menu():
    print(f"""
{C.BLUE}{'═'*55}{C.RESET}
  {C.BOLD}{C.WHITE}MAIN MENU — SELECT MODULE{C.RESET}
{C.BLUE}{'═'*55}{C.RESET}

  {C.CYAN}╔══ RECONNAISSANCE ══════════════════╗{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[1]{C.RESET}  WHOIS Lookup                  {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[2]{C.RESET}  DNS Records                   {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[3]{C.RESET}  Subdomain Enumeration         {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[4]{C.RESET}  HTTP Headers & Security Audit {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[5]{C.RESET}  IP Geolocation                {C.CYAN}║{C.RESET}
  {C.CYAN}╠══ SCANNING ════════════════════════╣{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[6]{C.RESET}  Technology Detection          {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[7]{C.RESET}  Port Scanner (Threaded)       {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[8]{C.RESET}  SSL/TLS Certificate           {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[9]{C.RESET}  Email Harvester               {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[10]{C.RESET} Wayback Machine History       {C.CYAN}║{C.RESET}
  {C.CYAN}╠══ DETECTION ═══════════════════════╣{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[11]{C.RESET} CMS Detection                 {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[12]{C.RESET} WAF / Firewall Detection      {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[13]{C.RESET} Social Media Finder           {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[14]{C.RESET} Link Crawler                  {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[15]{C.RESET} Robots.txt & Sitemap          {C.CYAN}║{C.RESET}
  {C.CYAN}╠══ VULNERABILITY ═══════════════════╣{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[16]{C.RESET} CORS Misconfiguration         {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[17]{C.RESET} Clickjacking Test             {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.GREEN}[18]{C.RESET} Reverse IP Lookup             {C.CYAN}║{C.RESET}
  {C.CYAN}╠══ FULL & REPORTS ══════════════════╣{C.RESET}
  {C.CYAN}║{C.RESET} {C.RED}[99]{C.RESET} {C.BOLD}FULL SCAN (All 18 Modules){C.RESET}  {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.YELLOW}[88]{C.RESET} Save Reports (JSON+HTML+TXT)  {C.CYAN}║{C.RESET}
  {C.CYAN}║{C.RESET} {C.WHITE}[0]{C.RESET}  Exit                          {C.CYAN}║{C.RESET}
  {C.CYAN}╚═════════════════════════════════════╝{C.RESET}
""")

def get_domain():
    domain = input(f"\n  {C.YELLOW}🎯 Target Domain: {C.RESET}").strip()
    if not domain:
        print(f"  {C.error('Domain cannot be empty!')}")
        return None
    domain = domain.replace("http://", "").replace("https://", "").split("/")[0]
    print(f"  {C.info(f'Target set: {domain}')}")
    return domain

def run_module(module_class, domain):
    start = time.time()
    scanner = module_class(domain)
    result = scanner.run()
    elapsed = time.time() - start
    print(f"\n  {C.DIM}⏱ Completed in {elapsed:.2f}s{C.RESET}")
    return result

def full_scan(domain):
    print(f"\n{C.RED}{C.BOLD}{'█'*55}")
    print(f"  FULL RECONNAISSANCE SCAN INITIATED")
    print(f"  Target: {domain}")
    print(f"  Modules: {len(MODULES)}")
    print(f"{'█'*55}{C.RESET}\n")

    reporter = Reporter(domain)
    total = len(MODULES)

    for i, (key, (name, cls)) in enumerate(MODULES.items(), 1):
        print(f"\n{C.MAGENTA}{'─'*55}")
        print(f"  Module [{i}/{total}]: {name}")
        print(f"{'─'*55}{C.RESET}")
        try:
            result = run_module(cls, domain)
            reporter.add(name, result)
        except Exception as e:
            print(f"  {C.error(f'Module failed: {e}')}")
            reporter.add(name, {"error": str(e)})
        time.sleep(0.5)

    print(f"\n{C.GREEN}{C.BOLD}{'█'*55}")
    print(f"  FULL SCAN COMPLETE!")
    print(f"{'█'*55}{C.RESET}")

    return reporter

def main():
    show_banner()
    last_reporter = None

    while True:
        print_menu()
        choice = input(f"  {C.RED}{C.BOLD}REDHAWK ❯ {C.RESET}").strip()

        if choice == '0':
            print(f"\n  {C.RED}[!] Exiting RedHawk. Stay Ethical! 🛡️{C.RESET}\n")
            sys.exit(0)

        elif choice == '99':
            domain = get_domain()
            if domain:
                last_reporter = full_scan(domain)
                # Auto-save
                last_reporter.save_json()
                last_reporter.save_html()
                last_reporter.save_txt()

        elif choice == '88':
            if last_reporter:
                last_reporter.save_json()
                last_reporter.save_html()
                last_reporter.save_txt()
            else:
                print(f"  {C.error('Run a Full Scan first (Option 99)')}")

        elif choice in MODULES:
            domain = get_domain()
            if domain:
                name, cls = MODULES[choice]
                run_module(cls, domain)

        else:
            print(f"  {C.error('Invalid option!')}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.RED}[!] Interrupted. Exiting...{C.RESET}\n")
        sys.exit(0)
