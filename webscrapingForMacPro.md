# Description:
Webscraping using BeautifulSoup, requests to collect price and rating of Apple Mac Pro from Amazon marketplace. Tasks include pulling data from the webpage, storing data to csv file, auto-questing/appending data to the file and setting up email notice to personal email account.


```python
# import libraries 

from bs4 import BeautifulSoup
import requests
import time
import datetime

import smtplib #to send email to yourself
```

## Pull data:


```python
# Connect to Website and pull in data

URL = 'https://www.amazon.com/dp/B09JQSLL92/ref=fs_a_mbt2_us3?_encoding=UTF8&th=1'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1", "Connection":"close", "Upgrade-Insecure-Requests":"1"}

#bring in the data
page = requests.get(URL, headers=headers)

soup1 = BeautifulSoup(page.content, "html.parser")#return as in html parser
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")#beautify the html code

title = soup2.find(id='productTitle').get_text()
print("Product Title:", title.strip())
title_a = title.strip()

price = soup2.find_all("span", class_="a-offscreen", limit=1)
for i in price:
    print ("Price: ", end="")
    print(i.text.strip())
for i in price:
    price_a = i.text.strip()

rating = soup2.find_all("span", class_="a-icon-alt", limit=1)
for r in rating:
    print ("Rating: ", end="")
    print(r.text.strip())
for r in rating:
    rating_a = r.text.strip()



#Other possible ways:
#price = soup2.find_all('div', attrs={'id': "corePriceDisplay_desktop_feature_div"})
#pirce = price.strip()[1:]
#print(price)
#print(soup2)#return all html code
```

    Product Title: 2021 Apple MacBook Pro (14-inch, Apple M1 Pro chip with 8‑core CPU and 14‑core GPU, 16GB RAM, 512GB SSD) - Space Gray
    Price: $1,909.00
    Rating: 4.8 out of 5 stars
    


```python
print(title_a)
print(price_a)
print(rating_a)
```

    2021 Apple MacBook Pro (14-inch, Apple M1 Pro chip with 8‑core CPU and 14‑core GPU, 16GB RAM, 512GB SSD) - Space Gray
    $1,909.00
    4.8 out of 5 stars
    


```python
#strip data to remove speical character or string
price_a = price_a.strip('$')
print(price_a)
rating_a = rating_a.strip(' out of 5 stars')
print(rating_a)
```

    1,909.00
    4.8
    


```python
type(title_a)#string datatype
type(price_a)#string
type(rating_a)#string
```




    str



## Add timestamp for reference:


```python
import datetime
today = datetime.date.today()
print(today)
```

    2022-11-23
    

## Create CSV and impute pulled data into it:


```python
import csv
header = ['Product Title', 'Price', 'Rating', 'Date']
data = [title_a, price_a, rating_a, today]
#type(data) #now it's a list

with open('AmazonWebScraperDF.csv', 'w', newline='',encoding='UTF8') as f: #'w':write; newline='' to have no space in between
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)
```


```python
import pandas as pd
df = pd.read_csv(r'C:/Users/Python/portfolio/AmazonWebScraperDF.csv')
print(df)
```

                                           Product Title     Price  Rating
    0  2021 Apple MacBook Pro (14-inch, Apple M1 Pro ...  1,909.00     4.8
    

## Append data to the csv


```python
with open('AmazonWebScraperDF.csv', 'a+', newline='',encoding='UTF8') as f: #'w':write; newline='' to have no space in between
    writer = csv.writer(f)
    writer.writerow(data)
```

## Auto update the data by set timer


```python
def check_price():
    URL = 'https://www.amazon.com/dp/B09JQSLL92/ref=fs_a_mbt2_us3?_encoding=UTF8&th=1'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1", "Connection":"close", "Upgrade-Insecure-Requests":"1"}

    #bring in the data
    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")#return as in html parser
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")#beautify the html code

    title = soup2.find(id='productTitle').get_text()
    print("Product Title:", title.strip())
    title_a = title.strip()

    price = soup2.find_all("span", class_="a-offscreen", limit=1)
    for i in price:
        price_a = i.text.strip()
        price_a = price_a.strip('$')

    rating = soup2.find_all("span", class_="a-icon-alt", limit=1)
    for r in rating:
        rating_a = r.text.strip()
        rating_a = rating_a.strip(' out of 5 stars')
        
    import datetime
    today = datetime.date.today()
    
    import csv
    header = ['Product Title', 'Price', 'Rating', 'Date']
    data = [title_a, price_a, rating_a, today]
    
    with open('AmazonWebScraperDF.csv', 'a+', newline='',encoding='UTF8') as f: #'w':write; newline='' to have no space in between
        writer = csv.writer(f)
        writer.writerow(data)
    
    if(price_a<1500):
        send_mail()
```


```python
#set checking timer
while(True):
    check_price()
    time.sleep(5)#this goes by second, now it check the price by day
```

    Product Title: 2021 Apple MacBook Pro (14-inch, Apple M1 Pro chip with 8‑core CPU and 14‑core GPU, 16GB RAM, 512GB SSD) - Space Gray
    


```python
import pandas as pd
df = pd.read_csv(r'C:/Users/Python/portfolio/AmazonWebScraperDF.csv')
print(df)
```


```python
def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    #server.starttls()
    server.ehlo()
    server.login('abcdt@gmail.com','xxxxxxxxxxxxxx')
    
    subject = "The Mac you want is below $1500! Now is your chance to buy!"
    body = "Linlin, This is the moment we have been waiting for. Now is your chance to pick up the mac of your dreams. Don't mess it up! Link here: https://www.amazon.com/dp/B09JQSLL92/ref=fs_a_mbt2_us3?_encoding=UTF8&th=1"
   
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(
        'abcdt@gmail.com',
        msg
     
    )
```

Reference:
* Find your user agent: https://httpbin.org/get
* Get the price from CSS class: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
* https://www.youtube.com/watch?v=HiOtQMcI5wg&list=PLubIOKb1GIwOur-YlLOjdTpwvwcIcOjEx&index=6
