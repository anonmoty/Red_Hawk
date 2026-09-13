import requests
from core.colors import Colors as C
from core.config import Config

class CORSScan:
    name = "CORS Misconfiguration Check"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🔗 CORS MISCONFIGURATION{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        results = {"vulnerable": False, "tests": []}

        test_origins = [
            "https://evil.com",
            "https://attacker.com",
            f"https://{self.domain}.evil.com",
            "null",
            f"https://sub.{self.domain}"
        ]

        for origin in test_origins:
            try:
                headers = dict(Config.HEADERS)
                headers['Origin'] = origin
                resp = requests.get(f"https://{self.domain}", headers=headers, timeout=Config.TIMEOUT)
                acao = resp.headers.get('Access-Control-Allow-Origin', '')
                acac = resp.headers.get('Access-Control-Allow-Credentials', '')

                test_result = {"origin": origin, "acao": acao, "acac": acac, "vulnerable": False}

                if acao == origin or acao == '*':
                    test_result["vulnerable"] = True
                    results["vulnerable"] = True
                    print(f"  {C.RED}[VULNERABLE]{C.RESET} Origin: {origin}")
                    print(f"    {C.DIM}ACAO: {acao}, ACAC: {acac}{C.RESET}")
                else:
                    print(f"  {C.GREEN}[SAFE]{C.RESET}       Origin: {origin}")

                results["tests"].append(test_result)
            except:
                pass

        if results["vulnerable"]:
            print(f"\n  {C.RED}{C.BOLD}[!] CORS Misconfiguration Detected!{C.RESET}")
        else:
            print(f"\n  {C.GREEN}[✓] No CORS issues found{C.RESET}")
        return results
