import requests
from core.colors import Colors as C
from core.config import Config

class FirewallDetect:
    name = "WAF / Firewall Detection"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🛡️ WAF / FIREWALL DETECTION{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        waf_detected = []
        try:
            resp = requests.get(f"https://{self.domain}", timeout=Config.TIMEOUT, headers=Config.HEADERS)
            headers = resp.headers
            body = resp.text.lower()

            waf_signatures = {
                "Cloudflare": {"headers": ["cf-ray", "cf-cache-status", "server: cloudflare"]},
                "AWS WAF": {"headers": ["x-amzn-requestid", "x-amz-cf-id"]},
                "Akamai": {"headers": ["x-akamai-transformed", "akamai"]},
                "Sucuri": {"headers": ["x-sucuri-id", "sucuri"], "body": ["sucuri"]},
                "Imperva/Incapsula": {"headers": ["x-iinfo", "incap_ses"]},
                "F5 BIG-IP": {"headers": ["x-wa-info", "bigipserver"]},
                "ModSecurity": {"headers": ["mod_security", "modsecurity"]},
                "DenyAll": {"headers": ["denyall"]},
                "Barracuda": {"headers": ["barra_counter_session"]},
                "Wordfence": {"body": ["wordfence"]},
                "AWS Shield": {"headers": ["x-amz-apigw-id"]},
                "Google Cloud Armor": {"headers": ["x-cloud-trace-context"]},
                "Fastly": {"headers": ["x-served-by", "fastly"]},
                "StackPath": {"headers": ["x-sp-"]},
            }

            headers_str = str(headers).lower()
            for waf, sigs in waf_signatures.items():
                detected = False
                for h in sigs.get("headers", []):
                    if h in headers_str:
                        detected = True
                        break
                for b in sigs.get("body", []):
                    if b in body:
                        detected = True
                        break
                if detected:
                    waf_detected.append(waf)
                    print(f"  {C.RED}[!] WAF Detected: {waf}{C.RESET}")

            if not waf_detected:
                print(f"  {C.GREEN}[✓] No WAF/Firewall detected{C.RESET}")
            else:
                print(f"\n  {C.BOLD}Total WAFs: {len(waf_detected)}{C.RESET}")

        except Exception as e:
            print(f"  {C.error(f'WAF detection failed: {e}')}")

        return waf_detected
