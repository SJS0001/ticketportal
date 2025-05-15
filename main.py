import requests, csv, threading, time, sys, random, logging, re, os
from discord_webhook import DiscordWebhook,DiscordEmbed
from colorama import init, Fore

logging.basicConfig(level=logging.INFO, format=Fore.WHITE + '[' + '%(asctime)s' + ']' + ' %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')
init(autoreset=True)
class Auto():
    def __init__(self, email, sektor, qty, koncert):
        self.email = email
        self.sektor = sektor
        self.qty = qty
        self.koncert = koncert

    def changeProxy(self):
        while True:
            try:
                with open('proxies.txt', 'r') as proxies_file:
                    proxy_raw = random.choice(proxies_file.read().split('\n'))
                    break

            except:
                logging.info(f'''{Fore.RED}COULD NOT READ PROXIES...''')
                time.sleep(5)
                sys.exit()

        try:
            proxy_parts = proxy_raw.split(':')
            ip, port, user, password = proxy_parts[0], proxy_parts[1], proxy_parts[2], proxy_parts[3]
            proxy = {'http': f'http://{user}:{password}@{ip}:{port}', 'https': f'http://{user}:{password}@{ip}:{port}'}

        except:
            proxy = {'http': 'http://' + str(proxy_raw), 'https': 'http://' + str(proxy_raw)}

        return proxy

    def cart(self):

        b = os.path.getsize('proxies.txt')
        if b == 0:
            self.useProxy = False
        else:
            self.useProxy = True

        if self.useProxy == True:
            proxies = Auto.changeProxy(self)

            self.r.proxies = proxies

        threadname = threading.current_thread().name
        threadname = str(threadname).replace('Thread-', 'TASK ')
        result = re.sub(r'\(.*?\)', '', threadname).strip()

        self.thread = f"""TICKETPORTAL - {result} - """

        logging.info(f'''{Fore.YELLOW}{self.thread}Starting task...''')

        self.headers = {
            "Host": "www.ticketportal.cz",
            "Origin": "https://www.ticketportal.cz",
            "referer": "https://www.ticketportal.cz/Basket",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        }

        self.r = requests.Session()

        basket2 = True

        if "RANDOM" not in self.sektor:
            self.url = f"https://www.ticketportal.cz/Event/SetNSeats/{self.koncert}/{self.qty}?idsektor={self.sektor}"
        else:
            self.url = f"https://www.ticketportal.cz/Event/SetNSeats/{self.koncert}/{self.qty}"

        while basket2:

            try:
                carts = self.r.get(self.url, headers=self.headers).json()
                self.basket = carts["ReturnedObject"]["NumberOfBasket"]
            except:
                print("ERROR")
                time.sleep(3)
                Auto.changeProxy(self)
                Auto.cart(self)



            if self.basket == 0:
                print("Not instock. Retrying")
                time.sleep(0.5)
                pass
            else:
                self.eventName = carts["ReturnedObject"]["Basket"]["Performances_info"][self.koncert]["Event_name"]
                self.sektorName = carts["ReturnedObject"]["Basket"]["Performance_count"][self.koncert][0]["Sektor"]

                jineID = carts["ReturnedObject"]["Basket"]["Performances_info"][self.koncert]["ID_Podujatie"]
                self.jineID = str(jineID)
                break

        Auto.checkout(self)

    def checkout(self):

        data = {
            "AkciaADD": "",
            f"typ_p_{self.jineID}": "1",
            "MZZlavaNew": "",
            "MZZlavaDel": "",
            "MPksluzbeNew": "",
            "zmazkosik": "0",
            "DelMiesto": "",
            "DelPredstavenie": "",
            "GAeventNameBasket": {self.eventName},
            "optionsRadiosPoistenie": "option2",
            "pickupTypeOption": "7",
            "email_pickup_7": self.email,
            "other_email": "",
            "email_pickup_1": "",
            "heslo_pickup": "",
            "CardpayPayOption": "17",
            "s_garancia": "0.00",
            "termsAccept_TicketportalTermsAccept": True,
            "termsAccept_O2TermsAcceptRequired": True,
            f"termsAccept_{self.koncert}": True,
            "createPayment": ""
        }
        try:
            check = self.r.post("https://www.ticketportal.cz/basket", data=data)
        except:
            Auto.cart(self)
        if "comgate" in check.url:
            print(f"Successful Checkout, počet: {str(self.basket)}")
            self.url = check.url
            Auto.saveCSV(self)
            Auto.webhook(self)
        else:
            print("Checkout failed. Retrying")
            Auto.cart(self)

    def saveCSV(self):
        with open("success.csv", "a", newline="") as cfile:
            fieldnames = ["LINK", "SEKTOR", "EMAIL", "KONCERT", "QTY"]
            write = csv.DictWriter(cfile, delimiter=',', fieldnames=fieldnames)
            write.writerow({'LINK': self.url, 'SEKTOR': self.sektorName, "EMAIL": self.email, "KONCERT": self.koncert, "QTY": self.basket})

    def webhook(self):
        try:
            webhook = DiscordWebhook(
                url="https://discord.com/api/webhooks/610221944574574594/ZNToXzLCBS3WhmNyllGQsi_90m2-_HPRPn2UTzo63c-aemo9wf7BYfRc7jo8nLc6JFEk")
            embed = DiscordEmbed(title='CHECKOUT', color=5885036, url=self.url)
            embed.add_embed_field(name='EVENT NAME', value=self.eventName, inline=True)
            embed.add_embed_field(name='MISTA', value=self.sektorName, inline=True)
            embed.add_embed_field(name='POCET', value=self.qty, inline=True)
            embed.set_footer(text='TICKETPORTAL')
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()
        except:
            print("Error with webhook")


if __name__ == "__main__":
    try:
        with open('tasks.csv', "r", encoding='UTF-8', newline='') as csvfile:
            tasks = csv.DictReader(csvfile, delimiter=',')
            for line in tasks:
                pico = Auto(email=line['EMAIL'], sektor=line["SEKTOR"], qty=line["QTY"])
                t = threading.Thread(target=pico.cart).start()
    except:
        print('''Check your tasks.csv, exiting...''')
        time.sleep(5)
        sys.exit()