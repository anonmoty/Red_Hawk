import json
import os
from datetime import datetime
from core.config import Config
from core.colors import Colors as C

class Reporter:
    def __init__(self, domain):
        self.domain = domain
        self.results = {}
        self.start_time = datetime.now()
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    def add(self, module_name, data):
        self.results[module_name] = data

    def save_json(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(Config.OUTPUT_DIR, f"{self.domain}_{ts}.json")
        report = {
            "tool": Config.TOOL_NAME,
            "version": Config.VERSION,
            "target": self.domain,
            "scan_start": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "scan_end": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "results": self.results
        }
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n  {C.success(f'JSON Report: {filepath}')}")
        return filepath

    def save_html(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(Config.OUTPUT_DIR, f"{self.domain}_{ts}.html")
        html = f"""<!DOCTYPE html>
<html><head>
<title>RedHawk Report - {self.domain}</title>
<style>
body {{ font-family: 'Courier New', monospace; background: #0a0e17; color: #00ff88; padding: 20px; }}
h1 {{ color: #ff4444; text-align: center; border-bottom: 2px solid #ff4444; padding-bottom: 10px; }}
h2 {{ color: #00d4ff; margin-top: 30px; border-left: 4px solid #00d4ff; padding-left: 10px; }}
.info {{ color: #ffd700; margin: 5px 0; }}
.card {{ background: #111827; border: 1px solid #1e3a5f; border-radius: 8px; padding: 15px; margin: 10px 0; }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
td, th {{ border: 1px solid #1e3a5f; padding: 8px; text-align: left; }}
th {{ background: #1e3a5f; color: #fff; }}
</style></head><body>
<h1>RED HAWK OSINT REPORT</h1>
<div class="card">
<p class="info">Target: {self.domain}</p>
<p class="info">Scan Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
<p class="info">Version: {Config.VERSION}</p>
</div>"""

        for module, data in self.results.items():
            html += f"<h2>{module}</h2><div class='card'><pre>{json.dumps(data, indent=2, default=str)}</pre></div>"

        html += "</body></html>"
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"  {C.success(f'HTML Report: {filepath}')}")
        return filepath

def save_txt(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(Config.OUTPUT_DIR, f"{self.domain}_{ts}.txt")
        with open(filepath, 'w') as f:
            f.write(f"RED HAWK v{Config.VERSION} - OSINT REPORT\n")
            f.write(f"Target: {self.domain}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            for module, data in self.results.items():
                f.write(f"\n{'='*40}\n{module}\n{'='*40}\n")
                f.write(json.dumps(data, indent=2, default=str))
                f.write("\n")
        print(f"  {C.success(f'TXT Report: {filepath}')}")
        return filepath
