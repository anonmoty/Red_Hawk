import dns.resolver
from core.colors import Colors as C

class DNSScan:
    name = "DNS Records"

    def __init__(self, domain):
        self.domain = domain
        self.types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'SRV', 'CAA', 'PTR']

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🌐 DNS RECORDS{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        results = {}
        for rtype in self.types:
            try:
                answers = dns.resolver.resolve(self.domain, rtype)
                records = [str(r) for r in answers]
                results[rtype] = records
                print(f"\n  {C.CYAN}[{rtype}]{C.RESET}")
                for rec in records:
                    print(f"    {C.found(rec)}")
            except dns.resolver.NoAnswer:
                pass
            except dns.resolver.NXDOMAIN:
                print(f"  {C.error('Domain does not exist!')}")
                break
            except:
                pass
        if not results:
            print(f"  {C.error('No DNS records found')}")
        return results
