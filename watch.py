import requests
from bs4 import BeautifulSoup
import csv
   
URL = "https://eastend.co.jp/watch/en/brands-en/"
r = requests.get(URL)
   
soup = BeautifulSoup(r.content, 'html.parser')
 
quotes=[]  # a list to store quotes
   
table = soup.find('div', attrs = {'class':'list_w06'}) 
# print(table)
for row in table.findAll('li'):
    quote = {}
    
    if(row.find('span',attrs = {'class':'brand_name'}) != None):
        # quote['theme'] = row.find('span',attrs = {'class':'brand_name'}).text.strip()
        # quote['img'] = row.findAll('a')[0].img['src']
        # if(row.find('span',attrs = {'class':'price_on_list'}) != None):
        #     quote['price'] = row.find('span',attrs = {'class':'price_on_list'}).text.strip()
        # else: quote['price'] = 'Unknown price'
        # quote['property'] = row.find('span',attrs = {'class':'color-used'}).text.strip()
        # quote['description'] = row.findAll('a')[1].text.strip().encode('utf-8')
        # quotes.append(quote)
        # print(quote)
        
        if(row.find('p') != None):
            quote['theme'] = row.findAll('span')[1].text.strip()
            quote['img'] = row.findAll('a')[0].img['src']
            quote['price'] = row.findAll('span')[0].text.strip() 
            quote['property'] = row.findAll('span')[2].text.strip() + "," +row.findAll('span')[3].text.strip()
            quote['description'] = row.findAll('a')[1].text.strip().encode('utf-8')
            quotes.append(quote)
            print(quote)
        else:
            quote['theme'] = row.findAll('span')[0].text.strip()
            quote['img'] = row.findAll('a')[0].img['src']
            quote['price'] = 'Unknown price'
            quote['property'] = row.findAll('span')[1].text.strip() +"," + row.findAll('span')[2].text.strip()
            quote['description'] = row.findAll('a')[1].text.strip().encode('utf-8')
            quotes.append(quote)
            print(quote)
    
    

filename = 'inspirational_quotes.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['theme','img','price','property','description'])
    w.writeheader()
    for quote in quotes:
        w.writerow(quote)