import requests
import socket
from core.colors import Colors as C

class GeoIPScan:
    name = "IP Geolocation"

    def __init__(self, domain):
        self.domain = domain

    def run(self):
        print(f"\n{C.BLUE}{'═'*55}{C.RESET}")
        print(f"  {C.BOLD}{C.RED}🌍 IP GEOLOCATION{C.RESET}")
        print(f"{C.BLUE}{'═'*55}{C.RESET}")
        try:
            ip = socket.gethostbyname(self.domain)
            print(f"  {C.info(f'Resolved IP: {ip}')}")

            apis = [
                f"http://ip-api.com/json/{ip}",
                f"https://ipapi.co/{ip}/json/"
            ]

            for api_url in apis:
                try:
                    resp = requests.get(api_url, timeout=10)
                    data = resp.json()
                    if data.get('status') == 'fail':
                        continue

                    result = {
                        "IP": ip,
                        "Country": data.get('country') or data.get('country_name'),
                        "Region": data.get('regionName') or data.get('region'),
                        "City": data.get('city'),
                        "ZIP": data.get('zip') or data.get('postal'),
                        "Latitude": data.get('lat') or data.get('latitude'),
                        "Longitude": data.get('lon') or data.get('longitude'),
                        "ISP": data.get('isp') or data.get('org'),
                        "Organization": data.get('org') or data.get('asn'),
                        "AS": data.get('as') or data.get('asn'),
                        "Timezone": data.get('timezone')
                    }

                    for k, v in result.items():
                        if v:
                            print(f"  {C.found(f'{k:15s}: {v}')}")

                    maps_url = f"https://www.google.com/maps/@{result.get('Latitude')},{result.get('Longitude')},15z"
                    print(f"\n  {C.info(f'Google Maps: {maps_url}')}")
                    return result
                except:
                    continue
        except Exception as e:
            print(f"  {C.error(f'GeoIP failed: {e}')}")
        return {}
