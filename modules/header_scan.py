import requests
from core.colors import Colors as C
from core.config import Config

class HeaderScan:
    name = "HTTP Headers & Security Audit"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🔒 HTTP HEADERS & SECURITY AUDIT{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        results = {"headers": {}, "security_score": 0, "issues": []}

        for scheme in ['https', 'http']:
            try:
                url = f"{scheme}://{self.domain}"
                resp = requests.get(url, timeout=Config.TIMEOUT, headers=Config.HEADERS, allow_redirects=True)

                print(f"\n  {C.info(f'URL: {resp.url}')}")
                print(f"  {C.info(f'Status: {resp.status_code}')}")
                print(f"  {C.info(f'Size: {len(resp.content)} bytes')}")
                print(f"  {C.info(f'Redirect Chain: {len(resp.history)} redirects')}")

                print(f"\n  {C.CYAN}Response Headers:{C.RESET}")
                for k, v in resp.headers.items():
                    results["headers"][k] = v
                    print(f"    {C.DIM}{k:35s}{C.RESET}: {v[:80]}")

                # Security Audit
                score = 0
                max_score = 8
                security_headers = {
                    "Strict-Transport-Security": ("HSTS", "Forces HTTPS connections"),
                    "X-Content-Type-Options": ("XCTO", "Prevents MIME sniffing"),
                    "X-Frame-Options": ("XFO", "Clickjacking protection"),
                    "X-XSS-Protection": ("XXSS", "XSS filter"),
                    "Content-Security-Policy": ("CSP", "Injection protection"),
                    "Referrer-Policy": ("RP", "Controls referrer info"),
                    "Permissions-Policy": ("PP", "Feature restrictions"),
                    "X-Permitted-Cross-Domain-Policies": ("XPCDP", "Flash/PDF policy")
                }

                print(f"\n  {C.CYAN}Security Headers Audit:{C.RESET}")
                for header, (abbr, desc) in security_headers.items():
                    if header.lower() in [h.lower() for h in resp.headers]:
                        score += 1
                        print(f"    {C.GREEN}[✓]{C.RESET} {header}")
                    else:
                        results["issues"].append(f"Missing: {header} ({desc})")
                        print(f"    {C.RED}[✗]{C.RESET} {header} - {C.DIM}{desc}{C.RESET}")

                results["security_score"] = f"{score}/{max_score} ({int(score/max_score*100)}%)"
                grade = "A+" if score >= 7 else "A" if score >= 6 else "B" if score >= 4 else "C" if score >= 2 else "F"
                color = C.GREEN if score >= 6 else C.YELLOW if score >= 4 else C.RED
                print(f"\n  {C.BOLD}Security Score: {color}{results['security_score']} (Grade: {grade}){C.RESET}")
                return results
            except:
                continue

        print(f"  {C.error('Could not connect to target')}")
        return results
