import csv
from numpy import array_split
from json import load, dump
from os import listdir, remove


class Filter:


    def parse_initial_urls(self, urlsFile:str) -> list:

        with open(f"{urlsFile}", "r", encoding="utf-16") as file:
            urls = file.readlines()
        
        return urls
    

    def parse_proxies(self, proxiesFile:str) -> list:
        ipPort = []

        with open(f"{proxiesFile}", "r", encoding="utf-8") as file:
            proxies = file.readlines()

            for proxy in proxies:
                ipPort.append(proxy.split(":")[:2])
        
        return ipPort
    

    def filtrate_list(self, dataList:list) -> list:
        filtrated_list = []
        for i in dataList:
            if i in filtrated_list:
                continue
            else:
                filtrated_list.append(i)
        
        return filtrated_list

    
    def filtrate_urls(self, urlsFile:str) -> list:
        urls = self.parse_initial_urls(urlsFile=urlsFile)
        filtered_urls = []
        for url in urls:
            if len(url) == 44 and url not in filtered_urls:
                filtered_urls.append(url)

        return filtered_urls
    

class Saver:

    def __init__(self, delimiter:str):
        self.listJsons = listdir("data")
        self.delimiter = delimiter
    

    def parse_data(self, dataDict:dict) -> int:
        data = []
        
        if dataDict["urls"] == None:
            data.append([dataDict["url"], dataDict["title"], dataDict["views"], dataDict["date"], dataDict["count_subscribers"], dataDict["channel_name"], None, None])
            return data
        else:
            amount_rows = len(dataDict["urls"])

        for row in range(amount_rows):
            if row == 0:
                data.append([dataDict["url"], dataDict["title"], dataDict["views"], dataDict["date"], dataDict["count_subscribers"], dataDict["channel_name"], dataDict["domains"][row], dataDict["urls"][row]])
            else:
                data.append(["", "", "", "", "", "", dataDict["domains"][row], dataDict["urls"][row]])
         

        return data


    def save_data_to_csv(self) -> int:
        headers = ["url", "title", "views", "date", "subscribers", "channel_name", "domains", "full_urls"]
        with open("data.csv", "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, delimiter=self.delimiter)
            writer.writerow(headers)
            for jsonFile in self.listJsons:
                data = load(open(f"data\{jsonFile}", encoding="utf-8"))
                for video in data:
                    rows = self.parse_data(video)
                    writer.writerows(rows)
            
            file.close()
                
        return 0
    
    def save_to_json(self) -> int:
        data = []

        for file in listdir("data"):
            data += load(open("data/" + file, "r", encoding="utf-8"))
        
        with open("data.json", "w", encoding="utf-8") as file:
            dump(data, file, indent=4, ensure_ascii=False)
            file.close()

        for file in listdir("data"):
            remove(f"data\{file}")
        
        return 0
    

def split_list(dataList:list, number: int) -> list:
    result = []
    for i in array_split(dataList, number):
        result.append(list(i))
    
    return result


