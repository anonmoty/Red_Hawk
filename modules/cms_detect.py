import requests
from core.colors import Colors as C
from core.config import Config

class CMSDetect:
    name = "CMS Detection"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🏗️ CMS DETECTION{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        results = {"cms": "Unknown", "details": []}

        cms_checks = {
            "WordPress": {
                "paths": ["/wp-login.php", "/wp-admin/", "/wp-content/", "/xmlrpc.php", "/wp-json/"],
                "body": ["wp-content", "wordpress"]
            },
            "Joomla": {
                "paths": ["/administrator/", "/components/", "/modules/", "/templates/"],
                "body": ["joomla", "com_content"]
            },
            "Drupal": {
                "paths": ["/core/misc/drupal.js", "/sites/default/", "/node/1"],
                "body": ["drupal"]
            },
            "Magento": {
                "paths": ["/admin/", "/skin/frontend/", "/js/mage/"],
                "body": ["magento", "mage/"]
            },
            "PrestaShop": {
                "paths": ["/admin-dev/", "/classes/", "/modules/"],
                "body": ["prestashop"]
            },
            "Shopify": {
                "paths": ["/admin/"],
                "body": ["shopify", "cdn.shopify"]
            }
        }

        try:
            main_resp = requests.get(f"https://{self.domain}", timeout=Config.TIMEOUT, headers=Config.HEADERS)
            body = main_resp.text.lower()

            for cms, checks in cms_checks.items():
                score = 0
                details = []

                for sig in checks.get("body", []):
                    if sig in body:
                        score += 2
                        details.append(f"Body match: {sig}")

                for path in checks.get("paths", []):
                    try:
                        resp = requests.get(f"https://{self.domain}{path}", timeout=5, headers=Config.HEADERS, allow_redirects=False)
                        if resp.status_code in [200, 301, 302, 403]:
                            score += 1
                            details.append(f"Path found: {path} ({resp.status_code})")
                    except:
                        pass

                if score >= 2:
                    results["cms"] = cms
                    results["details"] = details
                    print(f"  {C.GREEN}{C.BOLD}[✓] CMS Detected: {cms}{C.RESET}")
                    for d in details:
                        print(f"    {C.DIM}→ {d}{C.RESET}")
                    return results

            print(f"  {C.warning('No known CMS detected or custom-built')}")
        except Exception as e:
            print(f"  {C.error(f'CMS detection failed: {e}')}")
        return results
