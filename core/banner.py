import os
import random
from datetime import datetime
from core.colors import Colors as C

os.system('clear')

BANNERS = [
    f"""
{C.RED}{C.BOLD}
    ██████╗ ███████╗██████╗     ██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
    ██╔══██╗██╔════╝██╔══██╗    ██║  ██║██╔══██╗██║    ██║██║ ██╔╝
    ██████╔╝█████╗  ██║  ██║    ███████║███████║██║ █╗ ██║█████╔╝
    ██╔══██╗██╔══╝  ██║  ██║    ██╔══██║██╔══██║██║███╗██║██╔═██╗
    ██║  ██║███████╗██████╔╝    ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗
    ╚═╝  ╚═╝╚══════╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝
{C.RESET}""",
    f"""
{C.RED}{C.BOLD}
     ______          __   __  __               __  
    / ____/___  ____/ /  / / / /___ __      __/ /__
   / /_  / __ \\/ __  /  / /_/ / __ `/ | /| / / //_/
  / __/ / /_/ / /_/ /  / __  / /_/ /| |/ |/ / ,<   
 /_/ ___\\____/\\__,_/  /_/ /_/\\__,_/ |__/|__/_/|_|  
    / __ \\/ ___/  _/ | / /_  __/                    
   / / / /\\__ \\/ //  |/ / / /                       
  / /_/ /___/ / // /|  / / /                        
  \\____//____/___/_/ |_/ /_/  v3.0{C.RESET}"""
]

def show_banner():
    line = "─" * 55
    banner = random.choice(BANNERS)
    print(banner)
    print(f"    {C.CYAN}{line}{C.RESET}")
    print(f"    {C.BOLD}{C.WHITE}  OSINT Reconnaissance Framework v3.0{C.RESET}")
    print(f"    {C.GREEN}  20+ Modules | Multi-Threaded | Auto-Report{C.RESET}")
    print(f"    {C.MAGENTA}  Developer: Maxod anonmoty 🔰{C.RESET}")
    print(f"    {C.YELLOW}  ⚠  Authorized & Educational Use Only{C.RESET}")
    print(f"    {C.DIM}  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{C.RESET}")
    print(f"    {C.CYAN}{line}{C.RESET}")
