import requests
from core.colors import Colors as C
from core.config import Config

class SocialScan:
    name = "Social Media Finder"

    def __init__(self, domain):
        self.domain = domain
        self.brand = domain.split('.')[0]

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}📱 SOCIAL MEDIA FINDER{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")

        platforms = {
            "Twitter/X": f"https://twitter.com/{self.brand}",
            "Facebook": f"https://facebook.com/{self.brand}",
            "Instagram": f"https://instagram.com/{self.brand}",
            "LinkedIn": f"https://linkedin.com/company/{self.brand}",
            "GitHub": f"https://github.com/{self.brand}",
            "YouTube": f"https://youtube.com/@{self.brand}",
            "TikTok": f"https://tiktok.com/@{self.brand}",
            "Pinterest": f"https://pinterest.com/{self.brand}",
            "Reddit": f"https://reddit.com/r/{self.brand}",
            "Medium": f"https://medium.com/@{self.brand}",
            "Tumblr": f"https://{self.brand}.tumblr.com",
        }

        found = []
        total = len(platforms)
        done = 0

        for platform, url in platforms.items():
            done += 1
            C.progress(done, total, f"Checking {platform}...")
            try:
                resp = requests.get(url, timeout=8, headers=Config.HEADERS, allow_redirects=True)
                if resp.status_code == 200:
                    found.append({"platform": platform, "url": url})
                    print(f"\n    {C.GREEN}[✓]{C.RESET} {platform:15s}: {url}")
                else:
                    print(f"\n    {C.RED}[✗]{C.RESET} {platform:15s}: Not found")
            except:
                print(f"\n    {C.YELLOW}[?]{C.RESET} {platform:15s}: Timeout/Error")

        print(f"\n  {C.BOLD}{C.GREEN}[✓] Found on {len(found)} platforms{C.RESET}")
        return found
