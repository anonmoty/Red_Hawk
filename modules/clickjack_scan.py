import requests
from core.colors import Colors as C
from core.config import Config

class ClickjackScan:
    name = "Clickjacking Vulnerability Test"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🖱️ CLICKJACKING TEST{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        result = {"vulnerable": False}
        try:
            resp = requests.get(f"https://{self.domain}", timeout=Config.TIMEOUT, headers=Config.HEADERS)
            xfo = resp.headers.get('X-Frame-Options', '')
            csp = resp.headers.get('Content-Security-Policy', '')

            frame_ancestors = 'frame-ancestors' in csp.lower() if csp else False

            xfo_display = xfo if xfo else "NOT SET"
            fa_display = "Present" if frame_ancestors else "NOT SET"

            print(f"  {C.info(f'X-Frame-Options: {xfo_display}')}")
            print(f"  {C.info(f'CSP frame-ancestors: {fa_display}')}")

            if not xfo and not frame_ancestors:
                result["vulnerable"] = True
                print(f"\n  {C.RED}{C.BOLD}[!] VULNERABLE TO CLICKJACKING!{C.RESET}")
                print(f"  {C.DIM}No X-Frame-Options or CSP frame-ancestors header found{C.RESET}")

                poc = f"<!-- Clickjacking PoC -->\n<html><head><title>Clickjacking PoC</title></head><body>\n<h2>Clickjacking Test - {self.domain}</h2>\n<iframe src=\"https://{self.domain}\" width=\"100%\" height=\"600\" style=\"opacity:0.5;\"></iframe>\n</body></html>"
                result["poc"] = poc
                print(f"\n  {C.info('PoC HTML generated in report')}")
            else:
                print(f"\n  {C.GREEN}[✓] Protected against clickjacking{C.RESET}")

        except Exception as e:
            print(f"  {C.error(f'Test failed: {e}')}")
        return result
