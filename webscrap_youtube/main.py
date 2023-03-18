from Tools import *
from Scraper import *
from threading import Thread
from json import load
from os import remove, listdir



def start_threads(proxies:list, urls:list, amountThreads:int, timeout:float) -> int:

    proxies = split_list(proxies, amountThreads)
    urls = split_list(urls, amountThreads)

    thrList = []

    for i in range(amountThreads):
        parser = Parser(proxies=proxies[i], urls=urls[i], timeout=timeout)
        th = Thread(target=parser.main, args=(i,))
        thrList.append(th)
        th.start()

    for th in thrList:
        th.join()
    
    return 0



if __name__ == "__main__":
    urlsName = input("Enter name of file with urls: ")
    print(urlsName)
    proxiesName = input("Enter name of file with proxies: ")
    filter = Filter()
    proxies = filter.parse_proxies(proxiesFile=proxiesName)
    urls = filter.filtrate_urls(urlsFile=urlsName)
    amountThreads = int(input("Enter amount of threads: "))
    timeout = float(input("Enter timeout between requests: "))

    start_threads(proxies=proxies, urls=urls, amountThreads=amountThreads, timeout=timeout)

    delimiter = str(input("Choose your delimiter: "))
    # delimiter = ";"
    saver = Saver(delimiter=delimiter)
    saver.save_data_to_csv()
    saver.save_to_json()

