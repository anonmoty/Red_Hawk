import whois
from core.colors import Colors as C

class WhoisScan:
    name = "WHOIS Lookup"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}📋 WHOIS INFORMATION{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        try:
            w = whois.whois(self.domain)
            data = {}
            fields = {
                "Domain Name": w.domain_name,
                "Registrar": w.registrar,
                "WHOIS Server": w.whois_server,
                "Creation Date": w.creation_date,
                "Expiration Date": w.expiration_date,
                "Updated Date": w.updated_date,
                "Name Servers": w.name_servers,
                "Status": w.status,
                "Organization": w.org,
                "State": w.state,
                "Country": w.country,
                "Emails": w.emails,
                "DNSSEC": w.dnssec
            }
            for key, val in fields.items():
                if val:
                    if isinstance(val, list):
                        val = ", ".join(str(v) for v in val[:5])
                    data[key] = str(val)
                    print(f"  {C.found(f'{key:20s}: {val}')}")
            return data
        except Exception as e:
            print(f"  {C.error(f'WHOIS failed: {e}')}")
            return {"error": str(e)}
