import ssl
import socket
from datetime import datetime
from core.colors import Colors as C

class SSLScan:
    name = "SSL/TLS Certificate Analysis"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🔐 SSL/TLS CERTIFICATE{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        try:
            ctx = ssl.create_default_context()
            conn = ctx.wrap_socket(socket.socket(), server_hostname=self.domain)
            conn.settimeout(10)
            conn.connect((self.domain, 443))
            cert = conn.getpeercert()
            cipher = conn.cipher()
            version = conn.version()
            conn.close()

            result = {}

            # Subject
            subject = dict(x[0] for x in cert.get('subject', []))
            issuer = dict(x[0] for x in cert.get('issuer', []))
            
            result["Common Name"] = subject.get('commonName', 'N/A')
            result["Organization"] = subject.get('organizationName', 'N/A')
            result["Issuer"] = issuer.get('organizationName', 'N/A')
            result["Issuer CN"] = issuer.get('commonName', 'N/A')
            result["Serial Number"] = cert.get('serialNumber', 'N/A')
            result["Version"] = cert.get('version', 'N/A')
            
            # Dates
            not_before = cert.get('notBefore', '')
            not_after = cert.get('notAfter', '')
            result["Valid From"] = not_before
            result["Valid Until"] = not_after

            # Expiry check
            if not_after:
                expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                days_left = (expiry - datetime.utcnow()).days
                result["Days Until Expiry"] = days_left
                if days_left < 30:
                    result["WARNING"] = "Certificate expiring soon!"

            # SANs
            san_list = []
            for type_val in cert.get('subjectAltName', []):
                san_list.append(type_val[1])
            result["SANs"] = san_list[:20]

            # Cipher
            result["TLS Version"] = version
            result["Cipher Suite"] = cipher[0] if cipher else "N/A"
            result["Cipher Bits"] = cipher[2] if cipher else "N/A"

            for k, v in result.items():
                if isinstance(v, list):
                    print(f"  {C.found(f'{k}:')}")
                    for item in v:
                        print(f"    {C.DIM}→ {item}{C.RESET}")
                else:
                    color = C.RED if k == "WARNING" else ""
                    print(f"  {C.found(f'{k:22s}: {color}{v}{C.RESET}')}")

            return result
        except Exception as e:
            print(f"  {C.error(f'SSL scan failed: {e}')}")
            return {"error": str(e)}
