
from lxml import html
from requests.auth import HTTPDigestAuth
from Tools import Filter, Saver
from json import loads, dump
from regex import findall
from time import sleep
import requests



class Parser:

    filter = Filter()

    def __init__(self, proxies:list, urls:list, timeout:float):
        self.urls = urls
        self.timeout = timeout
        self.proxies = proxies
        self.current_proxy = 0

    def request(self, url:str, ip:str, port:str) -> str:

        proxies = {
            "http" :f"http://yjympjsk:k8n93vqq56qr@{ip}:{port}",
        }

        headers = {
            'authority': 'www.youtube.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            # 'cookie': 'VISITOR_INFO1_LIVE=2MoYgxa2FNU; HSID=A9k73KhR7nSjvx53U; SSID=AKxpGMeJWSRQJP3hH; APISID=RFlWcDVLCYyOSx6c/AOYmJnYcMXh2dFl2z; SAPISID=nXamOcqc0URS4jH5/AxSMJLy-uyqSzSxCw; __Secure-1PAPISID=nXamOcqc0URS4jH5/AxSMJLy-uyqSzSxCw; YSC=X1vEMPR7HEg; GPS=1; __Secure-3PAPISID=nXamOcqc0URS4jH5/AxSMJLy-uyqSzSxCw; LOGIN_INFO=AFmmF2swRAIgBFeYJT7JtxitD4GTV8yUm8UW4Vw3X9NzIj2iUSFDYWcCIBcif8_-6Wqev6rIwIHzbKREuyqXmx1DA7GLtBQZvC42:QUQ3MjNmeENSMjZxUWpSSjB5eTZvZjRfeWxrRF9MazhDeXlqTkl4dlo5SWxXbWdKQWt6Vi1ZR093dXR2ckdWLWJFUmROZmJ6akRZLTZOdUxYWFFCejU3SWpGcnNIOXVsS1c4eWVTbHVmMk5rbTFibUYxYVY0TnNzdDZ0NUM5YlBLdjdiaHZKNVdSUmhvRnQ3MDlYUi01VUpxYzNNUjV5RVRB; SID=UQgQDO_cCJgK7fPOGgliiNSh2C0biYqV8-GstNCUiGVot_DqB605L3D4esyOuw2w4wCbIg.; __Secure-1PSID=UQgQDO_cCJgK7fPOGgliiNSh2C0biYqV8-GstNCUiGVot_Dq5MAP_2pg1CY1HRlSpSkyaA.; __Secure-3PSID=UQgQDO_cCJgK7fPOGgliiNSh2C0biYqV8-GstNCUiGVot_DqpL7tBSTq6QbFnGVduidqJQ.; PREF=tz=Europe.Moscow; SIDCC=AFvIBn-Z5HloarAgPrefk32qaSV1AnOOTasx0eyg3LDLcU0AlReyNwZZIoIw63oz0zsDqu82; __Secure-1PSIDCC=AFvIBn-9bqozKzcuUZ_1Y-CJejziBLLWWoSJfLAmdFecQh3rHNv0sMjzCf-rlcZm85ND9rg8dg; __Secure-3PSIDCC=AFvIBn88Gm9F7uA1g4FgG2fwkbQYDNklJZCkHGCgci4f-5uhG69XNo4Oes22wqxvwj2joMJtBIY',
            'referer': 'https://www.youtube.com/signin_passive',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"110.0.5481.180"',
            'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.180", "Not A(Brand";v="24.0.0.0", "Google Chrome";v="110.0.5481.180"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'service-worker-navigation-preload': 'true',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }

        response = requests.get(url, headers=headers, proxies=proxies, timeout=5)

        return response

    def get_page(self, url:str):
        proxy = self.proxies[self.current_proxy]
        response = self.request(url=url, ip=proxy[0], port=proxy[1])

        if not response.ok:
            self.current_proxy += 1
            self.proxy_rotate(url=url)
        
        print(f"request IP: {proxy[0]}:{proxy[1]} status code: {response.status_code}")
        
        return response.text
    

    def get_json(self, text:str) -> dict:
        tree = html.fromstring(text)

        json = tree.xpath('//script[26]/text()')[0].replace("var ytInitialData = ", "")[:-1]
        return loads(json)
    
    def parse_json(self, jsonData:dict, url:str) -> dict:
        try:
            views = jsonData["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]["viewCount"]["videoViewCountRenderer"]["viewCount"]["simpleText"]
        except:
            views = None
        try:
            channel_name = jsonData["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"]["owner"]["videoOwnerRenderer"]["title"]["runs"][0]["text"]
        except:
            channel_name = None
        try:
            count_subscribers = jsonData["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"]["owner"]["videoOwnerRenderer"]["subscriberCountText"]["simpleText"]
        except:
            count_subscribers = None
        try:
            title = jsonData["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]["title"]["runs"][0]["text"]
        except:
            title = None
        try:
            urls = self.filter.filtrate_list(dataList=findall(r'(https?://[^\s]+)', jsonData["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"]["attributedDescription"]["content"]))
            if len(urls) == 0:
                urls = None
        except:
            urls = None
        try:
            date = jsonData["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]["dateText"]["simpleText"]
        except:
            date = None
        try:
            domains = [domain.split("/")[2] for domain in urls]
            if len(domains) == 0:
                domains = None
        except:
            domains = None

        return {"url": url.strip(), "title": title, "views": views, "date": date, "count_subscribers": count_subscribers, "channel_name": channel_name, "domains": domains, "urls": urls}
    

    def main(self, number:int) -> 0:
        data = []
        try:
            for e, url in enumerate(self.urls, start=1):
                page = self.get_page(url=url)

                sleep(self.timeout)

                json = self.get_json(text=page)
                
                json = self.parse_json(jsonData=json, url=url)
                data.append(json)
                print(f"[INFO] {e}/{len(self.urls)} url: {url}")
            
        
        except Exception as e:
            print('Error:\n', e.traceback.format_exc())
            with open(f"data\data{number}.json", "w", encoding="utf-8") as file:
                dump(data, file, indent=4, ensure_ascii=False)

        finally:
            with open(f"data\data{number}.json", "w", encoding="utf-8") as file:
                dump(data, file, indent=4, ensure_ascii=False)

        return 0
    


if __name__ == "__main__":
    parser = Parser(proxyFile="Webshare 99 proxies.txt")
    parser.main()
    data = loads(open("data.json", "r", encoding="utf-8").read())
    saver = Saver(data=data)
    saver.save_data_to_csv()
    
