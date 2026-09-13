import requests
from core.colors import Colors as C

class WaybackScan:
    name = "Wayback Machine History"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}📜 WAYBACK MACHINE HISTORY{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        results = {"snapshots": [], "urls": []}
        try:
            # Availability
            resp = requests.get(f"https://archive.org/wayback/available?url={self.domain}", timeout=10)
            data = resp.json()
            snapshot = data.get('archived_snapshots', {}).get('closest', {})
            if snapshot:
                snap_url = snapshot.get('url', 'N/A')
                snap_time = snapshot.get('timestamp', 'N/A')
                print(f"  {C.found(f'Latest Snapshot: {snap_url}')}")
                print(f"  {C.found(f'Timestamp: {snap_time}')}")
                results["snapshots"].append(snapshot)

            # URLs from CDX API
            print(f"\n  {C.info('Fetching historical URLs (CDX API)...')}")
            cdx_url = f"https://web.archive.org/cdx/search/cdx?url=*.{self.domain}/*&output=text&fl=original&collapse=urlkey&limit=100"
            resp2 = requests.get(cdx_url, timeout=20)
            if resp2.status_code == 200:
                urls = [u.strip() for u in resp2.text.strip().split('\n') if u.strip()]
                results["urls"] = urls[:100]
                print(f"  {C.found(f'Historical URLs found: {len(urls)}')}")
                for url in urls[:20]:
                    print(f"    {C.DIM}→ {url}{C.RESET}")
                if len(urls) > 20:
                    remaining = len(urls) - 20
                    print(f"    {C.DIM}  ... and {remaining} more{C.RESET}")
        except Exception as e:
            print(f"  {C.error(f'Wayback failed: {e}')}")
        return results
