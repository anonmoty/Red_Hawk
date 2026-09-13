import requests
from core.colors import Colors as C
from core.config import Config

class TechDetect:
    name = "Technology Detection"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}⚙️ TECHNOLOGY DETECTION{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        detected = []
        try:
            resp = requests.get(f"https://{self.domain}", timeout=Config.TIMEOUT,
                              headers=Config.HEADERS, allow_redirects=True)
            headers = {k.lower(): v.lower() for k, v in resp.headers.items()}
            body = resp.text.lower()

            signatures = {
                "Web Servers": {
                    "Nginx": ["nginx"],
                    "Apache": ["apache"],
                    "IIS": ["microsoft-iis"],
                    "LiteSpeed": ["litespeed"],
                    "Cloudflare": ["cloudflare", "cf-ray"],
                    "AWS CloudFront": ["cloudfront"],
                    "Fastly": ["fastly"],
                    "Varnish": ["varnish"]
                },
                "CMS / Frameworks": {
                    "WordPress": ["wp-content", "wp-includes", "wordpress"],
                    "Joomla": ["joomla", "com_content", "/media/system/"],
                    "Drupal": ["drupal", "sites/default/files"],
                    "Shopify": ["shopify", "cdn.shopify"],
                    "Wix": ["wix.com", "parastorage"],
                    "Squarespace": ["squarespace"],
                    "Magento": ["magento", "mage/"],
                    "Ghost": ["ghost.org"]
                },
                "JS Frameworks": {
                    "React": ["react", "reactdom", "_reactroot"],
                    "Angular": ["ng-app", "ng-controller", "angular.js"],
                    "Vue.js": ["vue.js", "v-bind", "v-model"],
                    "jQuery": ["jquery"],
                    "Next.js": ["__next", "_next/"],
                    "Nuxt.js": ["__nuxt"],
                    "Svelte": ["svelte"]
                },
                "Backend": {
                    "PHP": ["x-powered-by: php", ".php"],
                    "ASP.NET": ["asp.net", "x-aspnet-version"],
                    "Django": ["csrftoken", "django"],
                    "Flask": ["werkzeug"],
                    "Ruby on Rails": ["x-powered-by: phusion", "rails"],
                    "Express.js": ["x-powered-by: express"],
                    "Laravel": ["laravel_session"]
                },
                "Analytics & CDN": {
                    "Google Analytics": ["google-analytics", "gtag(", "ga.js"],
                    "Google Tag Manager": ["googletagmanager"],
                    "Facebook Pixel": ["facebook.com/tr", "fbevents"],
                    "Cloudflare CDN": ["cdnjs.cloudflare"],
                    "jsDelivr": ["cdn.jsdelivr.net"],
                    "unpkg": ["unpkg.com"]
                },
                "Security": {
                    "reCAPTCHA": ["recaptcha", "google.com/recaptcha"],
                    "hCaptcha": ["hcaptcha"],
                    "Sucuri WAF": ["sucuri"],
                    "Wordfence": ["wordfence"]
                }
            }

            for category, techs in signatures.items():
                cat_found = []
                for tech, sigs in techs.items():
                    for sig in sigs:
                        if sig in body or sig in str(headers):
                            cat_found.append(tech)
                            break
                if cat_found:
                    print(f"\n  {C.CYAN}[{category}]{C.RESET}")
                    for t in cat_found:
                        detected.append({"category": category, "tech": t})
                        print(f"    {C.found(t)}")

            if not detected:
                print(f"  {C.warning('No technologies detected')}")
            else:
                print(f"\n  {C.BOLD}{C.GREEN}[✓] Total Technologies: {len(detected)}{C.RESET}")

        except Exception as e:
            print(f"  {C.error(f'Tech detection failed: {e}')}")
        return detected

